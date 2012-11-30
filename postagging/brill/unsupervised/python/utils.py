#coding: utf-8

import sys
from StringIO import StringIO
import re
from sets import Set, ImmutableSet
from collections import namedtuple


CONTEXT = ('w-1', 't-1', 'w+1', 't+1')
NUMB_AMB = 0
NUMB_TOKENS = 0


def read_corpus(input):
    ss = []
    for sent in input.split('/sent')[:]:
        tokens = []
        sent = sent.lstrip('sent\n').rstrip('\n').split('\n')
        if sent == ['']:
            continue
        for ltoken in sent:
            ltoken = ltoken.decode('utf-8')
            t = Token(ltoken)
            tokens.append(t)
        s = Sentence(tokens)
        ss.append(s)
    c = Corpus(ss)
    return c


def write_corpus(corpus, outstream): #corpus is instance of Corpus()
    for sent in corpus:
        for token in sent:
            outstream.write(token.display() + '\n')


def split_into_sent(text):
    return text.split('/sent')


def get_pos_tags(line):
    line = line.split('\t')
    grammar = line[2:]
    pos_tags = []
    pos_tags_str = StringIO()
    for item in grammar:
        pos = item.split(' ')[0]
        if pos not in pos_tags:
            pos_tags.append(pos)
    pos_tags.sort()
    for tag in pos_tags:
            pos_tags_str.write(tag + '_')
    return pos_tags_str.getvalue().lstrip('_').rstrip('_')


def get_list_words_pos(corpus, ignore_numbers=True):
    result_dict = {}
    tvars = 0
    for sent in split_into_sent(corpus):
        tokens = process_table(sent)
        tokens.insert(0, 'sent')
        tokens.append('/sent')
        word_2, tag_2 = 'sent', 'sent'
        word_1, tag_1 = tokens[1][0], tokens[1][1]
        for token in tokens[1:-1]:
            tag = token[1]
            if ignore_numbers and token[0].isdigit():
                word = '_N_'
            else:
                word = token[0]
            if tag_1 in result_dict.keys():
                tag_entry = result_dict[tag_1]
                if tag_2 in tag_entry['t-1'].keys():
                    tag_entry['t-1'][tag_2] += 1
                else:
                    tag_entry['t-1'][tag_2] = 1
                if word_2 in tag_entry['w-1'].keys():
                    tag_entry['w-1'][word_2] += 1
                else:
                    tag_entry['w-1'][word_2] = 1
                if tag in tag_entry['t+1'].keys():
                    tag_entry['t+1'][tag] += 1
                else:
                    tag_entry['t+1'][tag] = 1
                if word in tag_entry['w+1'].keys():
                    tag_entry['w+1'][word] += 1
                else:
                    tag_entry['w+1'][word] = 1
                if 'freq' in tag_entry.keys():
                    tag_entry['freq'] += 1
                else:
                    tag_entry['freq'] = 1
            else:
                result_dict[tag_1] = dict(zip(('t-1', 'w-1', 't+1', 'w+1', 'freq'), \
                                              ({tag_2: 1}, {word_2: 1}, {tag: 1}, {word: 1}, 1)))
            tag_2, tag_1, word_2, word_1 = tag_1, tag, word_1, word
    return result_dict


def after_iter():
    return NUMB_AMB, NUMB_TOKENS


def process_table(sentence):
    to_return_list = []
    for line in sentence.split('\n'):
        #line.decode('utf-8')
        if 'sent' not in line:
            pos_tags_str = get_pos_tags(line)
            try:
                to_return_list.append((line[1], pos_tags_str))
            except:
                pass
        else:
            pass
    return to_return_list


def numb_amb_tokens(tokens):
    n = 0
    amb = 0
    vars = 0
    for token in tokens:
        tvars = len(token[1].split('_'))
        if tvars > 1:
            amb += 1
        vars += tvars
        n += 1
    #print amb, n
    return amb, n, vars


def numb_amb_corpus(corpus, numb_amb=0, numb_tokens=0, counter=numb_amb_tokens):
    tvars = 0
    for sent in split_into_sent(corpus):
        tokens = process_table(sent)
        if counter is not None:
            counts = counter(tokens)
            numb_amb += counts[0]
            numb_tokens += counts[1]
            tvars += counts[2]
    return numb_tokens, numb_amb, tvars


class Rule(object):

    def __init__(self, tagset, tag, context_type, context):
        self.tagset = tagset
        self.context = context
        self.tag = tag
        self.context_type = context_type
        for item in zip(CONTEXT, ('previous word', 'previous tag',
                                   'next word', 'next tag')):
            if context_type == item[0]:
                self.context_type = item[1]

    def display(self):
        return 'Change tag from %s to %s if %s is %s' % (self.tagset, self.tag, self.context_type, self.context)


class Corpus(set):

    def __init__(self, sentences):
        for i in range(len(sentences)):
            sent = Sentence(sentences.pop(0))
            sentences.append(sent)
        self.sents = sentences
        self.update(sentences)


class Sentence(tuple):

    def __init__(self, tokens):
        self._data = tokens
        tt = []
        tt.append('sent')
        try:
            for i in range(len(tokens)):
                t = tokens.pop(0)
                tt.append(t)
        except:
            pass
        tt.append('sent')
        self.tokens = tt


class Token(tuple):

    def __init__(self, token):
        self.text = token.split('\t')[1]
        self.tagset = TagSet(token.split('\t')[2:])

    def gettext(self):
        return self.text

    def gettagset(self):
        return self.tagset

    def getPOStags(self):
        return self.tagset.getPOStag()
    
    def display(self):
        return '\t'.join((self.text, self.tagset.display()))


class TagSet(set):

    def __init__(self, tags):
        self.set = []
        for tag in tags:
            self.set.append(Tag(tag).text)
    
    def display(self):
        return '\t'.join(self.set)

    def getPOStag(self):
        pos = []
        for tag in self.set:
            if tag.isPOStag():
                pos.append(tag.text)
        return '_'.join(pos)


class Tag(object):

    def __init__(self, tag):
        self.text = tag

    def isPOStag(self):
        pattern = re.compile('^[A-Z]{4}$', re.UNICODE)
        if pattern.search(self.text) is not None:
            return True
        else:
            return False


class TagStat(dict):

    def __init__(self):
        self.stat = dict(zip(CONTEXT, ([] for i in range(4))))

    def update(self, type, context):
        for t in self.stat.keys():
            if t == type:
                if context in self.stat.values():
                    self.stat[t][context] += 1
                else:
                    self.stat[t][context] = 1

if __name__ == '__main__':
    inc = sys.stdin.read()
    outc = read_corpus(inc)
    write_corpus(outc, sys.stdout)
