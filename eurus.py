#!/usr/bin/env python

import lxml.html
import argparse
import sys
from random import randint
from textblob import TextBlob


def getTossups(name):
    htmltree = lxml.html.parse(name)
    p_tags = htmltree.xpath('//p')
    a_tags = htmltree.xpath("//div[@class='alert alert-info span7']")
    while True:
        i = randint(0, len(p_tags))
        tossup = p_tags[i].text_content()
        answer = a_tags[i - 1].text_content()
        blob = TextBlob(tossup)
        i = randint(0, len(blob.sentences) - 1)
        ordinal = str(i + 1) + 'th out of ' + str(len(blob.sentences)) + ' sentences'
        tossup = {'question': blob.sentences[i], 'answer': answer, 'ordinal': ordinal}
        print tossup['question']
        try:
            raw_input("Press enter for answer...")
        except KeyboardInterrupt:
            sys.exit(0)
        print tossup['answer']
        print tossup['ordinal']
        try:
            raw_input("Press enter for next question...")
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='reads in quinterest html file for tossups', type=str)
    args = parser.parse_args()
    getTossups(args.file)
