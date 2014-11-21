import re
from difflib import ndiff, restore

class DiffFinder:

    def edited_tokens(self, old_tokens, new_tokens):
        try:
            raw_diff = ndiff(old_tokens, new_tokens)
        except:
            return []

        edits = []
        for edit, start, end in self.__diff_tokens(raw_diff):
            old_edit = ' '.join(restore(edit, 1))
            new_edit = ' '.join(restore(edit, 2))
            edits.append( (old_edit, new_edit, start, end) )

        return edits
    
    def __diff_tokens(self, raw_diff):
        diffs = self.__clean_diff(raw_diff)
        actions = self.__diff_actions(diffs)

        results = []
        pos_shift = 0
        for start, end, mlen, plen in self.__edition_indexes(actions):
            start_pos = start - pos_shift
            end_pos = start_pos + mlen
            pos_shift += plen
            results.append( (diffs[start:end], start_pos, end_pos) )
        
        return results

    def __edition_indexes(self, actions):
        indexes = []         
        for match in re.finditer(r'(-+)?(\++)|(-+)(\++)?', actions):
            mlen = max(match.end(1) - match.start(1), 
                       match.end(3) - match.start(3))
            plen = max(match.end(2) - match.start(2),
                       match.end(4) - match.start(4))
            indexes.append( (match.start(0), match.end(0), mlen, plen) )

        return indexes

    def __clean_diff(self, diff):
        try:
            return [line for line in list(diff) if not line.startswith('?')]
        except:
            return []

    def __diff_actions(self, diffs):
        return ''.join([line[0] for line in diffs])
