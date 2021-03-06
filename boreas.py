#!/usr/bin/env python

from operator import itemgetter
from multiprocessing import Pool
from time import sleep
import math
import lxml.html
import urlparse
import string
import argparse
import sys
import urllib
import re


def setupParser():
        parser = argparse.ArgumentParser(
            description='This program performs tf-idf analysis on Quiz Bowl questions with a given answer line against other answer lines requested, with tossups provided from Quinterest.org',
            epilog=
            """Examples:
                python boreas.py teddy+roosevelt,taft,eisenhower,lyndon+johnson -t 10
                python boreas.py chromium,iridium,sodium,nickel,magnesium -a magnesium -u -o
                python boreas.py war+autrian+succession,thirty+years+war,war+spanish+succession -a thirty+years+war -t 6 -o
            """,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('list', help='list of answer lines, replace spaces with "+" in words', type=str)
        parser.add_argument('-a', '--answer', help='selects desired answer line from list', type=str)
        parser.add_argument('-c', '--category', help='selects desired category for subjects', type=str)
        parser.add_argument('-d', '--difficulty', help='selects desired difficulty for subjects', type=str)
        parser.add_argument('-o', '--output', help='writes tf idf data to specified file', action='store_true')
        parser.add_argument('-t', '--terms', help='number of terms to print (between zero and number of words)', type=int)
        parser.add_argument('-u', '--upper', help='prints only upper case words', action='store_true')
        parser.add_argument('-l', '--lower', help='prints only lower case words', action='store_true')
        parser.add_argument('-r', '--reverse', help='prints list in reverse', action='store_false')
        parser.add_argument('-x', '--xargs', help='prints in format perfect for xargs', action='store_true')
        return parser.parse_args()


def stripWords(tossups, lower, upper):
    allWords = tossups.split(None)
    commonWords = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by", "word", "but", "not", "what", "all", "were", "we", "when", "your", "can", "said", "there.", "use", "an", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out", "many", "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look", "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now", "find", "long", "down", "day", "did", "get", "come", "made", "may", "part"}
    realWords = [x for x in allWords if x.lower() not in commonWords]

    if upper and lower:
        print "Please choose one option: --lower or --upper"
        sys.exit(1)
    elif upper and not lower:
        realWords = [x for x in realWords if x[0].isupper()]
    elif lower and not upper:
        realWords = [x for x in realWords if not x[0].isupper()]
    return realWords


def getTossups(url):
    f = open('.cache', 'ab+')
    cache = f.read()
    f.close()
    urlsub = url[url.find("?") + 1:]
    name = urllib.quote_plus(dict(urlparse.parse_qsl(urlsub))['info'])
    query = 'tossups for ' + name + ': '
    if query not in cache:
        if not args.xargs:
            print "Retrieving " + name + " tossups from Quinterest.org..."
        try:
            htmltree = lxml.html.parse(url)
            page = htmltree.getroot().xpath('//p')
        except:
            print(name + " is being throttled")
            sl = 30
            print("sleeping for " + str(sl) + " seconds")
            sleep(sl)
            htmltree = lxml.html.parse(url)
            page = htmltree.getroot().xpath('//p')
        page.pop(0)
        tossups = []
        for tossup in page:
            tossup = tossup.text_content().encode('latin-1', 'ignore')[10:]
            tossup = tossup.translate(string.maketrans("", ""), """!"#$%&+,./:;<=>*?@\^_`{|}~""")
            tossup = re.sub(r'\(.*?\)', '', tossup)
            tossup = re.sub(r'\[.*?\]', '', tossup)
            tossup = "tossup: " + tossup
            tossups.append(tossup)

        allTossups = " ".join(tossups)
        f = open('.cache', 'ab+')
        if len(tossups) > 0:
            f.write(query)
            f.write(allTossups + '\n')
        f.close()
        return tossups
    else:
        if not args.xargs:
            print "Retrieving " + name + " tossups from .cache..."
        index1 = cache.find(query)
        cache = cache[index1 + len(query + "tossup: "):]
        index2 = cache.find('tossups')
        if index2 != -1:
            cache = cache[:index2]

        tossups = cache.split('tossup: ')
        return tossups


def getWordRank(list, word, exploded):
    sum = 0
    docs = 0
    length = 0
    for tossup in list:
        if word in tossup:
            sum += tossup.find(word)
            length += len(tossup)
            docs += 1

    if sum == 0:
        sum = 1

    if exploded:
        return "tossups: " + str(docs) + "/" + str(len(list)) + ", earliness: " + str(1 / (float(sum) / length))[:8]


def constructCollection(answerLines, category, difficulty):
    collection = []
    pool = Pool(processes=4)
    urls = []
    for answerLine in answerLines:
        urls.append("http://quinterest.org/php/combined.php?info=" + answerLine + "&categ=" + category + "&difficulty=" + difficulty + "&stype=Answer&tournamentyear=All&qtype=Tossups")
    collection = pool.map(getTossups, urls)
    return collection


def constructDocumentList(collection):
    documentList = []
    for answerLine in collection:
        document = " ".join(answerLine)
        document = document.replace("tossup: ", "")
        documentList.append(document)
    return documentList


def freq(word, document):
    return document.split(None).count(word)


def wordCount(document):
    return len(document.split(None))


def numDocsContaining(word, documentList):
    count = 0
    for document in documentList:
        if word in document:
            count += 1
    return count


def tf(word, document):
    return (freq(word, document) / float(wordCount(document)))


def idf(word, documentList):
    return math.log(len(documentList) / float(numDocsContaining(word, documentList)))


def tfidf(word, index, documentList, collection):
    return "tf-idf: " + str(tf(word, documentList[index]) * idf(word, documentList) * 100)[:8] + ', ' + getWordRank(collection[index], word, True)


if __name__ == '__main__':
        args = setupParser()
        answerLines = args.list.split(',')

        if args.category is None:
            args.category = "All"

        if args.difficulty is None:
            args.difficulty = "All"

        collection = constructCollection(answerLines, args.category, args.difficulty)
        documentList = constructDocumentList(collection)

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
            realWords = stripWords(documentList[documentNumber], args.lower, args.upper)

            words = {}
            for word in realWords:
                words[word] = tfidf(word, documentNumber, documentList, collection)

            if args.terms and len(words.keys()) > args.terms > 0:
                words = sorted(words.items(), key=itemgetter(1), reverse=args.reverse)[:args.terms]
            else:
                words = sorted(words.items(), key=itemgetter(1), reverse=args.reverse)

            if args.xargs:
                display = "%s|"
            elif not args.xargs:
                display = "%s <= %s\n"

            if args.output and len(words) > 0:
                if len(answerLine) < 200:
                    f = open(answerLine + '.txt', 'wb+')
                else:
                    f = open(answerLine[:200] + '.txt', 'wb+')
                print "writing " + str(len(words)) + " results for '" + answerLines[documentNumber] + "' to " + answerLine + ".txt [" + str(documentNumber + 1) + "/" + str(len(answerLines)) + "]"
                f.write("writing " + str(len(words)) + "  results for '" + answerLines[documentNumber] + "' to " + answerLine + ".txt\n")
                for item in words:
                        f.write(display % (item[1], item[0]))

                f.close()
            else:
                if not args.xargs:
                    print "showing " + str(len(words)) + " results for '" + answerLines[documentNumber] + "'"
                if args.xargs:
                    sys.stdout.write("'(")
                for item in words:
                    if args.xargs:
                        sys.stdout.write(display % (item[0]))
                    else:
                        sys.stdout.write(display % (item[1], item[0]))
                if args.xargs:
                    sys.stdout.write(")'")
