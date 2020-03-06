#!/usr/bin/env python3

import csv
import spacy
import sys


def token_matches_keywords(keywords, token_raw):
    """ Matches keyword-list on a token and its children, return True if all keys are matching """
    if token_raw.lemma_.lower() != keywords[0]:
        return False

    while True:
        keywords = keywords[1:]
        if len(keywords) == 0:
            break

        child_match = False
        for child in token_raw.children:
            if child.lemma_.lower() == keywords[0]:
                child_match = True
                break

        if not child_match:
            return False

    return True


def main():
    keywords_category = {}

    with open('keywords.csv') as kw_file:
        keywords_file = csv.reader(kw_file, delimiter=',', quotechar='"')

        for row in keywords_file:
            for kw in row[3:]:
                if not kw:
                    continue
                if kw in keywords_category:
                    print('duplicate keyword', kw)
                    sys.exit(1)
                keywords_category[kw] = row[0:3]


    # python3 -m spacy download fr_core_news_sm
    nlp = spacy.load('fr_core_news_sm')

    matches = []

    with open('input.csv', newline='') as csvfile:
        comments = csv.reader(csvfile, delimiter=',', quotechar='"')

        for index, row in enumerate(comments):
            matches.append([row[0]]) # keep text as first column in match

            # natural language analyse
            phrase = nlp(row[0])

            for keywords, category in keywords_category.items():

                key_list = keywords.split(' ')

                for token_raw in phrase:
                    if token_matches_keywords(key_list[:], token_raw):
                        if category not in matches[-1]:
                            matches[-1].append(category)
                    #print(token_raw.text, token_raw.lemma_, token_raw.pos_, '->', token_raw.dep_, token_raw.head.text, token_raw.head.pos_, [child.lemma_ for child in token_raw.children])

    # output: first category of keyword is main category
    # TEXT, MAIN_CAT0, MAIN_CAT1, ..., MAIN_CATN, detail cat, ...

    main_categories = []
    for cat in keywords_category.values():
        if cat[0] not in main_categories:
            main_categories.append(cat[0])
    main_category_column = dict(zip(sorted(main_categories), range(1, len(main_categories)+1)))

    with open('output.csv', 'w', newline='') as csvfile:
        output = csv.writer(csvfile, delimiter=',', quotechar='"')

        output.writerow(['text'] + list(main_category_column.keys()))

        for match in matches:
            line = [match[0]]
            line += [''] * len(main_category_column.keys())
            for cat in match[1:]:
                print(main_category_column[cat[0]], len(line))
                line[ main_category_column[cat[0]] ] = '1'
                if cat[1] or cat[2]:
                    line.append('-'.join(cat[1:]))

            output.writerow(line)


if __name__ == '__main__':
    main()
