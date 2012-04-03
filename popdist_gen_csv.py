#!/usr/bin/env python
#
# Copyright 2012 Marco Schmalz <marco@schess.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import getopt, re, sys


def merge_tables(input_text, nl='\n', sep='\t', quot=None):
    table_title = re.search('\n(\w*)\W*\|.*\n-+\n', input_text).groups()[0]
    text_chunks = re.split('\n\w*\W*\|.*\n-+\n', input_text)[1:]
    line_chunks = map(lambda text: text.splitlines(), text_chunks)
    col_titles  = map(lambda line: line.split('|')[0].strip(), line_chunks[0])
    matrices    = map(lambda chunk: map(lambda line: line.split('|')[1].split(),
                                        chunk), line_chunks)
    matrix      = map(lambda line: reduce(lambda l, r: l+r, line), 
                      zip(*matrices))
    lines       = [ [ table_title ] + col_titles ] + \
                  map(lambda (i, line): [ col_titles[i] ] + line, 
                      enumerate(matrix))
    if quot:
        lines   = map(lambda line: map(lambda val: quot+val+quot, line), lines)
    output_text = nl.join(map(lambda line: sep.join(line), lines))
    return output_text


def usage(out=sys.stderr):
    text = """Usage: python %(progname)s [OPTIONS] INPUTFILE OUTPUTFILE
Merge fragemented popdist output tables into a single CVS file.

Options:
 -s, --separator=SEP  field separator in output file (default is TAB)
 -q, --quotes         put double quotes around field values (default is none)
 -u, --unix           use UNIX line breaks (CR) (default)
 -w, --windows        use Windows line breaks (CRLF)
 -h, --help           print this message and exit

When INPUTFILE or OUTPUTFILE are -, standard input or standard output are used
respectively.

For popdist see http://genetics.agrsci.dk/~bernt/popgen/
"""
    out.write(text % { 'progname': sys.argv[0] })

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hs:quw', ['--help', '--separator',
                                        '--quotes', '--unix', '--windows'])
    except getopt.GetoptError:
        usage()
        exit(1)
    if len(args) != 2:
        usage()
        exit(2)
    sep = '\t'
    nl = '\n'
    quot = None
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(sys.stdout)
            sys.exit()
        if o in ('-s', '--separator'):
            sep = a
        if o in ('-q', '--quotes'):
            quot = '"'
        if o in ('-u', '--unix'):
            nl = '\n'
        if o in ('-w', '--windows'):
            nl = '\n\r'

    src = sys.stdin if args[0] == '-' else open(args[0])
    dst = sys.stdout if args[1] == '-' else file(args[1], 'w')
    in_txt = src.read().strip()
    out_txt = merge_tables(in_txt, nl, sep, quot)
    dst.write(out_txt)
    dst.flush()

if __name__ == '__main__':
    main(sys.argv[1:])
