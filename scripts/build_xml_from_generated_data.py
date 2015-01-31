#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from collections import namedtuple

OutputData = namedtuple('OutputData', 'id srcid outputs')

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
        print '  <seg id="{0}" doc-id="{1}-{0}" src-id="{2}">' \
            .format(i, args.id, data.srcid)

        if data.srcid != 0:
            print '    <sourcebefore>{}</sourcebefore>'.format(source[data.srcid - 1])
        print '    <source>{}</source>'.format(source[data.srcid])
        if data.srcid + 1 < len(source):
            print '    <sourceafter>{}</sourceafter>'.format(source[data.srcid + 1])

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

    for line in file:
        fields = line.strip().split("\t")
        if len(fields) == 4:
            id, _, srcid, prob = fields
        elif len(fields) == 2:
            sentence, systems = fields
            outputs[systems] = sentence
        else:
            data.append(OutputData(int(id), int(srcid), outputs))
            outputs = {}

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
    parser.add_argument("-id", type=str, default="none", 
        help="ID name to use for the system name")

    return parser.parse_args()

if __name__ == "__main__":
    main()
