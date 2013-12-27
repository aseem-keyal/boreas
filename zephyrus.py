#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import argparse
import urllib2
import string
import collections
import json


def getTossups(url):
    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)
    page = soup.findAll('p')
    tossups = ''
    for tossup in page:
        tossup = str(tossup.contents)
        length = tossup.__len__() - 2
        tossup = tossup[24:length]
        tossup += '\n\n'
        tossups += tossup
    return tossups


def getAnswerLines(url):
    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)
    page = soup.findAll('div', {"class": "alert alert-info span7"})
    answerLines = []
    for answer in page:
        answer = str(answer)[70:len(str(answer)) - 7]
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
        answer = answer.translate(string.maketrans("", ""), string.punctuation)
        answerLines.append(answer)

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

        query = "http://quinterest.org/php/search.php?info=" + args.answer + "&categ=" + category + "&difficulty=" + difficulty + "&stype=Answer&tournamentyear=All"
        tossups = getAnswerLines(query)
        if args.common:
            counter = collections.Counter(tossups)
            print counter.most_common(args.common)
        else:
            counter = collections.Counter(tossups)
            print json.dumps(tossups)
            print len(tossups)
            print counter.most_common(5)
