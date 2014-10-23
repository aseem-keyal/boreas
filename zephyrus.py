#!/usr/bin/env python

from urllib import quote_plus
import lxml.html
import argparse
import string
import collections


def getTossups(url):
    htmltree = lxml.html.parse(url)
    page = htmltree.xpath('//p')

    tossups = ''
    for tossup in page:
        tossup = str(tossup.text_content())
        tossup += '\n\n'
        tossups += tossup
    return tossups


def getAnswerLines(url):
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
        answerLines.append(quote_plus(answer.lower()))

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

        query = "http://quinterest.org/php/combined.php?info=" + args.answer + "&categ=" + category + "&difficulty=" + difficulty + "&sub=None&stype=AnswerQuestion&tournamentyear=All&qtype=Tossups"
        tossups = getAnswerLines(query)
        if args.common:
            counter = collections.Counter(tossups)
            print counter.most_common(args.common)
        else:
            print ",".join(list(set(tossups)))
