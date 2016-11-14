##! /usr/bin/python3
from itertools import groupby, chain
from sys import stdout
from functools import partial
from json import dumps

def gensymer():
    n = [0]
    def inner():
        result = str(n[0])
        n[0] += 1
        return result
    return inner

gensym = gensymer()

def printTrie(graph, prev, trie, weight):
    new_node = str(gensym())
    graph.node(new_node, "%s" % trie.letter)
    graph.edge(prev, new_node, label="%.2f" % weight)
    if not trie.children:
        return
    for child, weight in zip(trie.children, trie.ws):
        printTrie(graph, new_node, child, weight)


class Trie(object):
    def __init__(self, letter, children, ws):
        self.letter = letter
        self.children = children
        self.ws = ws

def probweight(suffixes):
    weights = [float(s["value"]) for s in suffixes]
    s = float(sum(weights))
    ws = [w/s for w in weights]
    return ws

def buildtrie(trie, suffixes):
    """
    Build a trie, also known as a prefix tree, of all the possible completions
    """
    trie.children = []
    for letter, suffs in suffixes:
        ped = partition(suffs)
        if any(map(lambda p: p[0], ped)):
            # check if there are any children
            trie.children.append(buildtrie(Trie(letter, [], probweight(suffs)), partition(suffs)))
        else:
            # we've reached the end of this word so just include the final letter
            # [1] = there is a probability of 1 of reaching this single leaf node,
            # since it is the only possible completion here
            trie.children.append(Trie(letter, [], [1]))
    return trie


def keyf(x):
    if not x["key"]:
        return ""
    return x["key"][0]

def tails(words):
    for word in words:
        yield {
               "key" : word["key"][1:],
               "value" : word["value"]
               }

def partition(words):
    """
    Partition the words into different prefixes based on the first character
    """
    groups = [
            (g[0], list(tails(g[1])))
                for g in groupby(
                    sorted(words, key=keyf),
                    key=keyf)
             ]
    return groups


def flatten_helper(letter, trie):
    return ([letter + child.letter for
            child in trie.children], trie.children)

def flatten(trie):
    if not trie.children:
        return trie.letter
    prefixes, suffixes = flatten_helper(trie.letter, trie)
    return [flatten(Trie(p, s2.children, s2.ws)) for p, s2 in zip(prefixes, suffixes)]

def flattenlist(xs):
    locs = []
    for x in xs:
        if not isinstance(x, list):
            locs.append(x)
        else:
            locs.extend(flattenlist(x))
    return locs

def matchc(trie, prefix):
    c = None
    if len(prefix) > 1:
        c = prefix[0]
    else:
        c = prefix
    return [ch for ch in trie.children if ch.letter == c]

def match(trie, word):
    if not word:
        return []
    m = matchc(trie, word[0])
    if not m:
        return []
    else:
        return [m[0]] + match(m[0], word[1:])

def complete(trie, word):
    m = match(trie, word)
    if len(word) != len(m):
        return False
    completions = [word+x[1:] for x in flattenlist(flatten(m[-1]))]
    if len(completions) > 10:
        return dumps(completions[0:10])
    return dumps(completions)

def sortTrie(trie):
    """
    Sort the children of each node in descending order
    of the probability that each child would be the completion
    of whatever that word is
    """
    if not trie.children:
        return
    sortedChilds = sorted(zip(trie.children, trie.ws), key=lambda x: x[1], reverse=True)
    trie.children = [x[0] for x in sortedChilds]
    trie.ws = [x[1] for x in sortedChilds]
    for child in trie.children:
        sortTrie(child)

def toTrie(words):
    for word in words:
        word["key"] = word["key"].lower()
    trie = buildtrie(Trie("", [], [1]), partition(words))
    trie.ws = [1]*len(trie.children)
    sortTrie(trie)
    return trie

def testkey(w):
    return {
            "key" : w,
            "value" : "1"
            }
