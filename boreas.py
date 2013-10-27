#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from operator import itemgetter
import math
import string
import argparse
import sys
import urllib2


def getTossups(url):
    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)
    page = soup.findAll('p')
    tossups = ''
    for tossup in page:
        tossup = str(tossup.contents)
        length = tossup.__len__() - 2
        tossup = tossup[24:length]
        tossup += ' '
        tossups += tossup
    return tossups


def freq(word, document):
    return document.split(None).count(word)


def wordCount(document):
    return len(document.split(None))


def numDocsContaining(word, documentList):
    count = 0
    for document in documentList:
        if freq(word, document) > 0:
            count += 1
    return count


def tf(word, document):
    return (freq(word, document) / float(wordCount(document)))


def idf(word, documentList):
    return math.log(len(documentList) / float(numDocsContaining(word, documentList)))


def tfidf(word, document, documentList):
    return (tf(word, document) * idf(word, documentList))


if __name__ == '__main__':

        parser = argparse.ArgumentParser(
            description='This program performs tf-idf analysis on Quiz Bowl questions with a given answer line against other answer lines requested, with tossups provided from Quinterest.org',
            epilog=
            """Examples:
                python boreas.py teddy+roosevelt,taft,eisenhower,lyndon+johnson taft -t 10
                python boreas.py chromium,iridium,sodium,nickel,magnesium magnesium -u -o elements.txt
                python boreas.py war+autrian+succession,thirty+years+war,war+spanish+succession thirty+years+war -t 6 -o wars.txt
            """,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('list', help='list of answer lines, replace spaces with "+" in words', type=str)
        parser.add_argument('-a', '--answer', help='selects desired answer line from list', type=str)
        parser.add_argument('-o', '--output', help='writes tf idf data to specified file', action='store_true')
        parser.add_argument('-t', '--terms', help='number of terms to print (between zero and number of words)', type=int)
        parser.add_argument('-u', '--upper', help='prints only upper case words', action='store_true')
        parser.add_argument('-l', '--lower', help='prints only lower case words', action='store_true')
        args = parser.parse_args()
        answerLines = args.list.split(',')

        print "Retrieving tossups from Quinterest.org..."
        documentList = []

        for answerLine in answerLines:
            tossup = getTossups("http://quinterest.org/php/search.php?info=" + answerLine + "&categ=All&difficulty=All&stype=Answer&tournamentyear=All")
            tossup = tossup.translate(string.maketrans("", ""), string.punctuation)
            documentList.append(tossup)

        if args.answer and args.answer in answerLines:
            answerLines2 = []
            answerLines2.append(args.answer)
        elif args.answer and not args.answer in answerLines:
            print "Please choose a answer line in the list you provided"
            sys.exit(1)
        else:
            answerLines2 = answerLines

        for answerLine in answerLines2:
            documentNumber = answerLines.index(answerLine)
            allWords = documentList[documentNumber].split(None)
            commonWords = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by", "word", "but", "not", "what", "all", "were", "we", "when", "your", "can", "said", "there.", "use", "an", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out", "many", "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look", "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now", "find", "long", "down", "day", "did", "get", "come", "made", "may", "part"}
            realWords = [x for x in allWords if x.lower() not in commonWords]

            if args.upper and args.lower:
                print "Please choose one option: --lower or --upper"
                sys.exit(1)
            elif args.upper and not args.lower:
                realWords = [x for x in realWords if x.istitle()]
            elif args.lower and not args.upper:
                realWords = [x for x in realWords if not x.istitle()]

            words = {}
            for word in realWords:
                words[word] = tfidf(word, documentList[documentNumber], documentList)

            if args.terms and len(words.keys()) > args.terms > 0:
                words = sorted(words.items(), key=itemgetter(1), reverse=True)[:args.terms]
            else:
                words = sorted(words.items(), key=itemgetter(1), reverse=True)

            if args.output:
                f = open(answerLine + '.txt', 'wb+')
                print "writing results for '" + answerLines[documentNumber] + "' to " + answerLine + ".txt"
                f.write("writing results for '" + answerLines[documentNumber] + "' to " + answerLine + ".txt\n")
                for item in words:
                    f.write("%f <= %s\n" % (item[1], item[0]))
                f.close()
            else:
                print "showing results for '" + answerLines[documentNumber] + "'"
                for item in words:
                    print "%f <= %s" % (item[1], item[0])
