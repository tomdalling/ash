from abc import ABCMeta, abstractmethod
import pdb
import string
import sys
import json
import re


class INode(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def children(self):
        '''Returns a dict of child INode objects, or None if the node is a
        leaf.
        '''
        return None;

    @abstractmethod
    def __str__(self):
        '''Un-parse the node back into a string'''
        return ''

    def humanClassName(self):
        name = type(self).__name__
        assert name.endswith('Node')
        name = name[:-4]
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>", name)

    def jsonDict(self):
        '''Return a dict suitable for JSON encoding'''
        j = {
            '_type': self.humanClassName(),
            '_text': str(self)
        }

        children = self.children()
        if children is not None:
            json_children = dict()
            for name, child in children.iteritems():
                json_children[name] = child.jsonDict()
            j['children'] = json_children

        return j


class CommandNode(INode):

    def __init__(self, verb, noun):
        assert isinstance(verb, VerbNode)
        assert isinstance(noun, NounNode)

        self.verb = verb
        self.noun = noun

    def children(self):
        return {
            'verb':self.verb,
            'object':self.noun
        }

    def __str__(self):
        return str(self.verb) + ' ' + str(self.noun)


class StatementNode(INode):

    def __init__(self, subject, verb, objekt=None, adjuncts=[]):
        assert isinstance(subject, NounNode)
        assert isinstance(verb, VerbNode)
        assert objekt is None or isinstance(objekt, NounNode)
        for adj in adjuncts:
            assert isinstance(adj, AdjunctNode)

        self.subject = subject
        self.verb = verb
        self.objekt = objekt
        self.adjuncts = adjuncts

    def children(self):
        children = {
            'subject': self.subject,
            'verb': self.verb
        }

        if self.objekt is not None:
            children['object'] = self.objekt

        if len(self.adjuncts) > 0:
            idx = 1
            for adj in self.adjuncts:
                children['adjunct' + str(idx)] = adj
                idx += 1

        return children

    def __str__(self):
        s = str(self.subject) + ' ' + str(self.verb)

        if self.objekt is not None:
            s += ' ' + str(self.objekt)

        for adj in self.adjuncts:
            s += ' ' + str(adj)

        return s

class QuestionNode(INode):
    PARTICLE = 'ke'

    def __init__(self, statement):
        assert isinstance(statement, StatementNode)
        self.statement = statement

    def children(self):
        return {'statment': self.statement}

    def __str__(self):
        return self.PARTICLE + ' ' + str(self.statement)


class AdjunctNode(INode):
    pass


class TemporalAdjunctNode(AdjunctNode):
    TWORDS = {
        'BEFORE': 'timet',
        'DURING': 'time',
        'AFTER': 'timem'
    }

    def __init__(self, temporality, noun):
        assert temporality in self.TWORDS
        assert isinstance(noun, NounNode)

        self.temporality = temporality
        self.noun = noun

    def children(self):
        return {'noun': self.noun}

    def __str__(self):
        return self.TWORDS[self.temporality] + ' ' + str(self.noun)

    def jsonDict(self):
        j = super(AdjunctNode, self).jsonDict()
        j['temporality'] = self.temporality
        return j


class InstrumentalAdjunctNode(AdjunctNode):
    INCLUSIVE_TWORD = 'tem'  # with
    EXCLUSIVE_TWORD = 'temna'  # without

    def __init__(self, inclusive, noun):
        assert isinstance(noun, NounNode)

        self.inclusive = bool(inclusive)
        self.noun = noun

    def children(self):
        return {'noun': self.noun}

    def __str__(self):
        tword = (self.INCLUSIVE_TWORD if self.inclusive else self.EXCLUSIVE_TWORD)
        return tword + ' ' + str(self.noun)

    def jsonDict(self):
        j = super(AdjunctNode, self).jsonDict()
        j['inclusive'] = self.inclusive
        return j


class NounNode(INode):
    pass


class PossessiveNounNode(NounNode):
    PARTICLE = 'ko'

    def __init__(self, possessor, possessee):
        assert isinstance(possessor, NounNode)
        assert isinstance(possessee, NounNode)

        self.possessor = possessor
        self.possessee = possessee

    def children(self):
        return {
            'possessee': self.possessee,
            'possessor': self.possessor
        }

    def __str__(self):
        return ' '.join((str(self.possessee), self.PARTICLE, str(self.possessor)))


class ProperNounNode(NounNode):
    PREFIX = "Sha'"

    def __init__(self, word):
        assert word.startswith(self.PREFIX)
        assert word[len(self.PREFIX)].isupper()
        self.word = word

    def children(self):
        return None

    def __str__(self):
        return self.word


class PronounNode(NounNode):
    ALL_PRONOUNS = frozenset(('Shi', 'Shae', 'Shinen', 'Shaenen'))

    def __init__(self, word):
        assert word in self.ALL_PRONOUNS
        self.word = word

    def children(self):
        return None

    def __str__(self):
        return self.word


class CommonNounNode(NounNode):
    PREFIX = 's'

    def __init__(self, word):
        assert word.startswith(self.PREFIX)
        self.word = word

    def children(self):
        return None

    def __str__(self):
        return self.word


class VerbNode(INode):
    PREFIX = 'v'
    NEGATION_PREFIX = 'na'
    TENSES = {
        'PAST': 'et',
        'PRESENT': 'e',
        'FUTURE': 'em',
    }

    def __init__(self, base, tense, negated=False):
        assert tense in self.TENSES
        assert base.startswith(self.PREFIX)
        self.base = base
        self.tense = tense
        self.negated = negated

    def children(self):
        return None

    def __str__(self):
        return ''.join((
            (self.NEGATION_PREFIX if self.negated else ''),
            self.base,
            self.TENSES[self.tense]
        ))

    def jsonDict(self):
        j = super(VerbNode, self).jsonDict()
        j['base'] = self.base
        j['tense'] = self.tense
        j['negated'] = self.negated
        return j


class TokenizationError(Exception):
    pass


class StopTokenIteration(StopIteration):
    pass


class Tokenizer(object):
    '''Breaks a string to word and punctuation tokens.'''
    ALPHABET = frozenset(string.ascii_letters + "'")
    PUNCTUATION = frozenset('.')
    WHITESPACE = frozenset(string.whitespace)

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.pos_stack = []

    def __iter__(self):
        return self

    def next(self):
        while True:
            if self.pos >= len(self.text):
                raise StopTokenIteration()

            ch = self.text[self.pos]
            self.pos += 1

            if ch in self.ALPHABET:
                self.pos -= 1
                return self.next_word()
            elif ch in self.WHITESPACE:
                pass
            elif ch in self.PUNCTUATION:
                return ch
            else:
                raise TokenizationError()

    def next_word(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] in self.ALPHABET:
            self.pos += 1
        return self.text[start:self.pos]

    def push(self):
        self.pos_stack.append(self.pos)

    def pop(self, restore=True):
        assert len(self.pos_stack) > 0
        pos = self.pos_stack.pop()
        if restore:
            self.pos = pos


class ParseError(Exception):
    pass


def parse(tokens):
    '''Parses text into its AST'''
    return parse_clause(tokens)

def try_parse(parse_method, tokens):
    tokens.push()
    try:
        node = parse_method(tokens)
    except (ParseError, StopTokenIteration):
        tokens.pop(restore=True)
        return None
    else:
        tokens.pop(restore=False)
        return node

def parse_clause(tokens):
    tokens.push()
    first_word = next(tokens, None)
    tokens.pop()

    if first_word is None:
        raise ParseError('Clause has no words')

    if first_word == QuestionNode.PARTICLE:
        return parse_question(tokens)

    statement = try_parse(parse_statement, tokens)
    if statement is not None:
        return statement

    command = try_parse(command_statement, tokens)
    if command is not None:
        return command

    raise ParseError('Failed to parse clause')

def parse_command(tokens):
    verb = parse_verb(tokens)
    noun = parse_noun(tokens)
    return CommandNode(verb, noun)

def parse_statement(tokens):
    subject = parse_noun(tokens)
    verb = parse_verb(tokens)
    objekt = try_parse(parse_noun, tokens)

    adjuncts = []
    while True:
        adj = try_parse(parse_adjunct, tokens)
        if adj is None:
            break
        else:
            adjuncts.append(adj)

    return StatementNode(subject, verb, objekt, adjuncts)

def parse_question(tokens):
    if next(tokens) != QuestionNode.PARTICLE:
        raise ParseError('Question does not begin with correct particle')

    statement = parse_statement(tokens)
    return QuestionNode(statement)

def parse_adjunct(tokens):
    tword = next(tokens)
    if not tword.startswith('t'):
        raise ParseError('Adjunct does not start with t-word')

    # check if TemporalAdjunctNode
    for temporality, temporal_tword in TemporalAdjunctNode.TWORDS.iteritems():
        if tword == temporal_tword:
            noun = parse_noun(tokens)
            return TemporalAdjunctNode(temporality, noun)

    # check if InstrumentalAdjunctNode
    if tword == InstrumentalAdjunctNode.INCLUSIVE_TWORD:
        noun = parse_noun(tokens)
        return InstrumentalAdjunctNode(inclusive=True, noun=noun)
    if tword == InstrumentalAdjunctNode.EXCLUSIVE_TWORD:
        noun = parse_noun(tokens)
        return InstrumentalAdjunctNode(inclusive=False, noun=noun)

    # unrecognised tword
    raise ParseError('Unrecognised t-word: ' + str(tword))


def parse_verb(tokens):
    verb = next(tokens)
    for tense, suffix in VerbNode.TENSES.iteritems():
        if verb.endswith(suffix):
            root = verb[:-len(suffix)]
            negated = False
            if verb.startswith(VerbNode.NEGATION_PREFIX):
                negated = True
                root = root[len(VerbNode.NEGATION_PREFIX):]
            return VerbNode(root, tense, negated)

    raise ParseError("couldn't determine tense of verb: " + verb)

def parse_noun(tokens):
    word = next(tokens)

    #noun word
    noun = None
    if word in PronounNode.ALL_PRONOUNS:
        noun = PronounNode(word)
    elif word.startswith(ProperNounNode.PREFIX):
        noun = ProperNounNode(word)
    elif word.startswith(CommonNounNode.PREFIX):
        noun = CommonNounNode(word)
    else:
        raise ParseError("Can't determine the type of the noun: " + word)

    #optional possessive case
    tokens.push()
    if next(tokens, None) == PossessiveNounNode.PARTICLE:
        tokens.pop(restore=False)
        owner = parse_noun(tokens)
        return PossessiveNounNode(possessor=owner, possessee=noun)
    else:
        tokens.pop(restore=True)
        return noun

if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        (failure_count, test_count) = doctest.testmod()
        sys.exit(failure_count)

    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            else:
                t = Tokenizer(line)
                ast = parse(t)
                if next(t, None) is not None:
                    raise ParseError('Unparsed tokens remaining')
                else:
                    print json.dumps(ast.jsonDict(), sort_keys=True, indent=4)
