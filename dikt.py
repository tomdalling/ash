#!/usr/bin/env python

import json
import sys
import fnmatch
import textwrap


class Dikt(object):
    WORD_TYPES = frozenset(('noun', 'verb', 'pronoun', 'particle'))

    def __init__(self):
        self.dikt = {}

    def __iter__(self):
        return self.dikt.iteritems()

    def lookup(self, word):
        if word in self.dikt:
            return self.dikt[word]
        else:
            return None

    def add(self, word, word_type, short_def, long_def=None):
        assert len(word) > 0
        assert word_type in self.WORD_TYPES
        assert word not in self.dikt
        entry = {'type': word_type, 'def': short_def}
        if long_def:
            entry['long_def'] = long_def
        self.dikt[word] = entry

    def remove(self, word):
        assert word in self.dikt
        del self.dikt[word]

    def save(self, to_file):
        json.dump(self.dikt, to_file)

    def load(self, from_file):
        self.dikt =json.load(from_file)


def print_entry(word, entry):
    top_line = '{0} ({1}) - {2}'.format(word, entry['type'], entry['def'])
    print top_line
    if 'long_def' in entry and entry['long_def']:
        for line in entry['long_def'].splitlines():
            print '    ' + line
        print

def lookup_word(dikt, word):
    entry = dikt.lookup(word)
    if entry is None:
        print 'No entry found for word "{0}"'.format(word)
    else:
        print_entry(word, entry)

def remove_word(dikt, word):
    if dikt.lookup(word) is None:
        print 'Word not found in dictionary: ' + word
    else:
        dikt.remove(word)
        print 'Removed word from dictionary: ' + word

def add_entry(dikt, word, word_type, short_def, long_def):
    if len(word) == 0:
        print 'Word is too small: ' + word
        return

    if dikt.lookup(word) is not None:
        print 'Word already exists.'
        lookup_word(dikt, word)
        return

    if word_type not in Dikt.WORD_TYPES:
        print 'Invalid word type: ' + word_type
        print 'Valid types are: ' + ', '.join(dikt.WORD_TYPES)
        return

    if len(short_def) <= 1:
        print 'Short definition too short: ' + definition
        return

    dikt.add(word, word_type, short_def, long_def)
    print 'Added new word to dictionary: ' + word
    lookup_word(dikt, word)

def find_translation(dikt, english):
    print 'Searching for "{0}" in definitions...'.format(english)
    num_found = 0
    for word, entry in dikt:
        if english in entry['def']:
            num_found += 1
            print_entry(word, entry)
    print '{0} entries found'.format(num_found)

def list_all(dikt):
    for word, entry in dikt:
        print_entry(word, entry)

def print_help():
    print textwrap.dedent('''
        Usage:

            {cmd} <word>
                Finds entry for <word>.

            {cmd} <text>
                Find entrys that contain <text> in the definition.

            {cmd} rm <word>
                Removes <word> from the dictionary.

            {cmd} add <word> <type> <short_definition> [--]
                Adds <word> to the dictionary. If "--" is the last arg,
                reads a longer definition from the standard input. <type>
                must be one of the following:

                    {word_types}

            {cmd} list_all
                Finds every word in the dictionary.
        '''.format(cmd=sys.argv[0],
                   word_types=', '.join(Dikt.WORD_TYPES)))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print_help()
        sys.exit()

    dikt = Dikt()
    needs_save = False
    with open('dictionary.json', 'rb') as f:
        dikt.load(f)

    cmd = sys.argv[1]
    if cmd == 'add':
        if sys.argv[-1] == '--':
            long_def = sys.stdin.read()
        else:
            long_def = None
        add_entry(dikt, sys.argv[2], sys.argv[3], sys.argv[4], long_def)
        needs_save = True
    elif cmd == 'rm':
        remove_word(dikt, sys.argv[2])
        needs_save = True
    elif cmd == 'search':
        find_translation(dikt, sys.argv[2])
    elif cmd == 'list_all':
        list_all(dikt)
    else:
        lookup_word(dikt, sys.argv[1])

    if needs_save:
        print 'Saving dictionary...'
        with open('dictionary.json', 'wb') as f:
            dikt.save(f)
