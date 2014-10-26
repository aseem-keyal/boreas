#!/usr/bin/env python

import lxml.html
import argparse
import string
import collections
import urllib


def getTossups(url):
    htmltree = lxml.html.parse(url)
    page = htmltree.xpath('//p')

    tossups = ''
    for tossup in page:
        tossup = str(tossup.text_content())
        tossup += '\n\n'
        tossups += tossup
    return tossups


def getAnswerLines(url, stopWords):
    htmltree = lxml.html.parse(url)
    page = htmltree.xpath("//div[@class='alert alert-info span7']")

    answerLines = []
    for answer in page:
        answer = answer.text_content()[7:]
        index = answer.find("(")
        if index != -1:
            answer = answer[:index]
        index = answer.find("[")
        if index != -1:
            answer = answer[:index]
        index = answer.find("<")
        if index != -1:
            answer = answer[:index]
        answer = answer.strip()
        answer = answer.encode('latin-1', 'ignore')
        answer = answer.translate(string.maketrans("", ""), """!"#$%&+,./:;<=>*?@\^_`{|}~""")

        if "The" in answer or "the" in answer:
            toParse = answer.split(" ")
            if toParse[0] in ["the", "The"]:
                toParse = toParse[1:]
                answer = " ".join(toParse)
        if " or " in answer and len(answer) < 100:
            toParse = answer.split(" or ")
            for word in toParse:
                if " " not in word and word.lower() in stopWords:
                    toParse.remove(word)
            toParse = [urllib.quote_plus(answerLine.lower()) for answerLine in toParse]
            answerLines += toParse
        elif len(answer) < 150:
            answerLines.append(urllib.quote_plus(answer.lower()))

    answerLines = filter(None, answerLines)
    return answerLines


if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--answer', help='selects desired answer line from list', type=str)
        parser.add_argument('-c', '--category', help='selects desired category for subjects', type=str)
        parser.add_argument('-d', '--difficulty', help='selects desired difficulty for subjects', type=str)
        parser.add_argument('-m', '--common', help='displays most common answer lines matching a pattern', type=int)
        args = parser.parse_args()

        if args.category:
            category = args.category
        else:
            category = "All"

        if args.difficulty:
            difficulty = args.difficulty
        else:
            difficulty = "All"

        tossups = []
        queries = args.answer.split(",")
        toRemove = []
        for query in queries:
            toRemove += query.split("+")
        for query in queries:
            url = "http://quinterest.org/php/combined.php?info=" + query + "&categ=" + category + "&difficulty=" + difficulty + "&sub=None&stype=AnswerQuestion&tournamentyear=All&qtype=Tossups"
            tossups += getAnswerLines(url, toRemove)

        if args.common:
            counter = collections.Counter(tossups)
            print counter.most_common(args.common)
        else:
            print ",".join(list(set(tossups)))
