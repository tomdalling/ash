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
        '''Returns a sequence of child INode objects, or None if the node is a
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
            j['children'] = [c.jsonDict() for c in children]

        return j


class CommandNode(INode):

    def __init__(self, verb, noun):
        assert isinstance(verb, VerbNode)
        assert isinstance(noun, NounNode)

        self.verb = verb
        self.noun = noun

    def children(self):
        return (self.verb, self.noun)

    def __str__(self):
        return str(self.verb) + ' ' + str(self.noun)


class StatementNode(INode):

    def __init__(self, subject, verb, objekt):
        assert isinstance(subject, NounNode)
        assert isinstance(verb, VerbNode)
        assert isinstance(objekt, NounNode)

        self.subject = subject
        self.verb = verb
        self.objekt = objekt

    def children(self):
        return (self.subject, self.verb, self.objekt)

    def __str__(self):
        return ' '.join((str(self.subject), str(self.verb), str(self.objekt)))


class QuestionNode(INode):
    PARTICLE = 'ke'

    def __init__(self, statement):
        assert isinstance(statement, StatementNode)
        self.statement = statement

    def children(self):
        return (self.statement,)

    def __str__(self):
        return self.PARTICLE + ' ' + str(self.statement)


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
        return (self.possessee, self.possessor)

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
    ALL_PRONOUNS = frozenset(('Shi', 'Shae', 'Shinen', 'Shanen'))

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
                return TokenizationError('End of token stream')

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
        while self.text[self.pos] in self.ALPHABET:
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
    except ParseError:
        tokens.pop(restore=True)
        return False
    else:
        tokens.pop(restore=False)
        return node

def parse_clause(tokens):
    tokens.push()
    first_word = tokens.next()
    tokens.pop()

    if first_word == QuestionNode.PARTICLE:
        return parse_question(tokens)

    statement = try_parse(parse_statement, tokens)
    if statement:
        return statement

    command = try_parse(command_statement, tokens)
    if command:
        return command

    raise ParseError("Failed to parse clause")

def parse_command(tokens):
    verb = parse_verb(tokens)
    noun = parse_noun(tokens)
    return CommandNode(verb, noun)

def parse_statement(tokens):
    subject = parse_noun(tokens)
    verb = parse_verb(tokens)
    objekt = parse_noun(tokens)
    return StatementNode(subject, verb, objekt)

def parse_question(tokens):
    if tokens.next() != QuestionNode.PARTICLE:
        raise ParseError('Question does not begin with correct particle')

    statement = parse_statement(tokens)
    return QuestionNode(statement)

def parse_verb(tokens):
    verb = tokens.next()
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
    word = tokens.next()

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
    if tokens.next() == PossessiveNounNode.PARTICLE:
        tokens.pop(restore=False)
        owner = parse_noun(tokens)
        return PossessiveNounNode(possessor=owner, possessee=noun)
    else:
        tokens.pop(restore=True)
        return noun

if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
    else:
        with open(sys.argv[1]) as f:
            t = Tokenizer(f.read())
            ast = parse(t)
            print json.dumps(ast.jsonDict(), sort_keys=True, indent=4)
