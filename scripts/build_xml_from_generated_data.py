#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from collections import namedtuple

OutputData = namedtuple('OutputData', 'id srcid outputs')

EMPTY_SENTENCE = '[EMPTY]'


def main():
    args = parse_user_arguments() 

    source = []
    for line in args.source:
        source.append(line.strip())
    
    reference = []
    for line in args.reference:
        reference.append(line.strip())

    systems = read_system_outputs(args.data)

    print '<set id="{}" source-language="{}" target-language="{}">' \
        .format(args.data.name, args.source_lang, args.target_lang)

    for i, data in enumerate(systems):
        docid = os.path.basename(args.data.name) if not args.id else args.id
        print '  <seg id="{0}" doc-id="{1}-{0}" src-id="{2}">' \
            .format(i, docid, data.srcid)

        source_before = source[data.srcid - 1] if data.srcid != 0 else ''
        source_after = source[data.srcid + 1] if data.srcid + 1 < len(source) else ''

        print '    <sourcebefore>{}</sourcebefore>'.format(source_before)
        print '    <source>{}</source>'.format(source[data.srcid])
        print '    <sourceafter>{}</sourceafter>'.format(source_after)

        if i <= len(reference) - 1:
            print '    <reference>{}</reference>'.format(reference[data.srcid])

        for system, sentence in data.outputs.iteritems():
            print '    <translation system="{}">{}</translation>' \
                .format(system, sentence)
        print '  </seg>'
    print '</set>'

def read_system_outputs(file):
    data = []
    outputs = {}
    id, srcid = None, None

    line_num = 0

    for line in file:
        fields = line.strip().split("\t")
        line_num += 1

        if len(fields) == 4:
            id, _, srcid, prob = fields
        elif len(fields) == 2:
            sentence, systems = fields
            outputs[systems] = sentence
        elif len(fields) == 1:
            if fields[0] == '':
                data.append(OutputData(int(id), int(srcid), outputs))
                outputs = {}
            else:
                systems = fields[0]
                outputs[systems] = EMPTY_SENTENCE 
                print >> sys.stderr, "warning: found empty translation for " \
                  "system='{}' in sentence id='{}', source id='{}'" \
                  .format(systems, id, srcid)
        else:
            print >> sys.stderr, "error: unrecognized line {}".format(line_num)

    return data

def parse_user_arguments():
    parser = argparse.ArgumentParser(description="Converts data generated " \
        "for Error Correction Ranking Task to XML format.")

    parser.add_argument("source", type=file, help="source language file")
    parser.add_argument("data", type=file, help="generated data to evaluate")
    parser.add_argument("reference", type=file, nargs="?", 
        help="reference language file")
    parser.add_argument("-source", type=str, default="err", dest="source_lang", 
        help="the source language")
    parser.add_argument("-target", type=str, default="cor", dest="target_lang", 
        help="the target language")
    parser.add_argument("-id", type=str, default="", 
        help="ID name to use for the system name")

    return parser.parse_args()

if __name__ == "__main__":
    main()
