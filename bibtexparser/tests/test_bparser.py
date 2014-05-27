#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import tempfile
import os.path

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
from bibtexparser import customization


def customizations_unicode(record):
    """Use all functions related to specific fields
    + converter to unicode.

    :param record: a record
    :returns: -- customized record
    """

    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    record = convert_to_unicode(record)
    return record


def customizations_latex(record):
    """Use all functions related to specific fields
    + converter to latex.

    :param record: a record
    :returns: -- customized record
    """

    record = homogeneize_latex_encoding(record)
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record


class TestBibtexParserFunc(unittest.TestCase):

    bibfile = os.path.join(tempfile.gettempdir(), "tmp-testfile")

    def setUp(self):
        with open(self.bibfile, "w") as f:
            f.write("r")

    def test_strip_quotes(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_quotes('"before remove after"')
            expected = 'before remove after'
            self.assertEqual(result, expected)

    def test_strip_quotes_n(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_quotes('"before remove after"\n')
            expected = 'before remove after'
            self.assertEqual(result, expected)

    def test_strip_quotes2(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_quotes('before "remove" after')
            expected = 'before "remove" after'
            self.assertEqual(result, expected)

    def test_strip_braces(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_braces('{before remove after}')
            expected = 'before remove after'
            self.assertEqual(result, expected)

    def test_strip_braces2(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_braces('before {remove} after')
            expected = 'before {remove} after'
            self.assertEqual(result, expected)

    def test_strip_braces_n(self):
        with open(self.bibfile, 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            result = bib._strip_braces('{before remove after}\n')
            expected = 'before remove after'
            self.assertEqual(result, expected)


class TestBibtexParserList(unittest.TestCase):

    def test_wrong(self):
        """
        Wrong entry type
        """
        with open('bibtexparser/tests/data/wrong.bib', 'r') as bibfile:
            self.assetRaises(TypeError, BibTexParser, bibfile)

    ###########
    # ARTICLE
    ###########
    # test also that list and dict are equivalent
    def test_article(self):
        with open('bibtexparser/tests/data/article.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res_list = bib.get_entry_list()
            res_dict = bib.get_entry_dict()
            expected_list = [{'keyword': 'keyword1, keyword2',
                              'type': 'article',
                              'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french érudit word',
                              'year': '2013',
                              'journal': 'Nice Journal',
                              'id': 'Cesar2013',
                              'pages': '12-23',
                              'title': 'An amazing title',
                              'comments': 'A comment',
                              'author': 'Jean César',
                              'volume': '12',
                              'month': 'jan'
                              }]
            expected_dict = {'Cesar2013': {'keyword': 'keyword1, keyword2',
                              'type': 'article',
                              'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french érudit word',
                              'year': '2013',
                              'journal': 'Nice Journal',
                              'id': 'Cesar2013',
                              'pages': '12-23',
                              'title': 'An amazing title',
                              'comments': 'A comment',
                              'author': 'Jean César',
                              'volume': '12',
                              'month': 'jan'
                              }}
        self.assertEqual(res_list, expected_list)
        self.assertEqual(res_dict, expected_dict)

    def test_article_cust_unicode(self):
        with open('bibtexparser/tests/data/article.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=customizations_unicode)
            res = bib.get_entry_list()
        expected = [{'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french érudit word',
                     'type': 'article',
                     'pages': '12--23',
                     'volume': '12',
                     'id': 'Cesar2013',
                     'year': '2013',
                     'author': ['César, Jean'],
                     'journal': {'id': 'NiceJournal', 'name': 'Nice Journal'},
                     'comments': 'A comment',
                     'month': 'jan',
                     'keyword': ['keyword1', 'keyword2'],
                     'title': 'An amazing title'
                     }]
        self.assertEqual(res, expected)

    def test_article_cust_latex(self):
        with open('bibtexparser/tests/data/article.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=customizations_latex)
            res = bib.get_entry_list()
        expected = [{'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french {\\\'e}rudit word',
                     'type': 'article',
                     'pages': '12--23',
                     'volume': '12',
                     'id': 'Cesar2013',
                     'year': '2013',
                     'author': ['C{\\\'e}sar, Jean'],
                     'journal': {'id': 'NiceJournal', 'name': 'Nice Journal'},
                     'comments': 'A comment',
                     'month': 'jan',
                     'keyword': ['keyword1', 'keyword2'],
                     'title': '{A}n amazing title'
                     }]
        self.assertEqual(res, expected)

    def test_article_cust_order(self):
        def cust(record):
            record = customization.page_double_hyphen(record)
            record = customization.homogeneize_latex_encoding(record)
            record = customization.author(record)
            return record

        def cust2(record):
            record = customization.author(record)
            record = customization.page_double_hyphen(record)
            record = customization.homogeneize_latex_encoding(record)
            return record

        with open('bibtexparser/tests/data/multiple_entries.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=cust)
            res = bib.get_entry_list()
        with open('bibtexparser/tests/data/multiple_entries.bib', 'r') as bibfile:
            bib2 = BibTexParser(bibfile.read(), customization=cust2)
            res2 = bib.get_entry_list()
        print(res2)
        self.assertEqual(res, res2)

    ###########
    # BOOK
    ###########
    def test_book(self):
        with open('bibtexparser/tests/data/book.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'type': 'book',
                         'year': '1987',
                         'edition': '2',
                         'publisher': 'Wiley Edition',
                         'id': 'Bird1987',
                         'volume': '1',
                         'title': 'Dynamics of Polymeric Liquid',
                         'author': 'Bird, R.B. and Armstrong, R.C. and Hassager, O.'
                         }]

        self.assertEqual(res, expected)

    def test_book_cust_unicode(self):
        with open('bibtexparser/tests/data/book.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=customizations_unicode)
            res = bib.get_entry_list()
            expected = [{'type': 'book',
                         'year': '1987',
                         'edition': '2',
                         'publisher': 'Wiley Edition',
                         'id': 'Bird1987',
                         'volume': '1',
                         'title': 'Dynamics of Polymeric Liquid',
                         'author': ['Bird, R.B.', 'Armstrong, R.C.', 'Hassager, O.']
                         }]

        self.assertEqual(res, expected)

    def test_book_cust_latex(self):
        with open('bibtexparser/tests/data/book.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=customizations_latex)
            res = bib.get_entry_list()
            expected = [{'type': 'book',
                         'year': '1987',
                         'edition': '2',
                         'publisher': 'Wiley Edition',
                         'id': 'Bird1987',
                         'volume': '1',
                         'title': '{D}ynamics of {P}olymeric {L}iquid',
                         'author': ['Bird, R.B.', 'Armstrong, R.C.', 'Hassager, O.']
                         }]

        self.assertEqual(res, expected)

    ###########
    # TRAPS
    ###########
    def test_traps(self):
        with open('bibtexparser/tests/data/traps.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'keyword': 'keyword1, keyword2',
                         'type': 'article',
                         'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french érudit word',
                         'year': '2013',
                         'journal': 'Nice Journal',
                         'id': 'Laide2013',
                         'pages': '12-23',
                         'title': 'An amazing title',
                         'comments': 'A comment',
                         'author': 'Jean Laid{\\\'e}, Ben Loaeb',
                         'volume': '12',
                         'month': 'jan'
                         }]
        self.assertEqual(res, expected)

    ###########
    # FEATURES
    ###########
    def test_features(self):
        with open('bibtexparser/tests/data/features.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'type': 'inproceedings',
                         'year': '2014',
                         'title': 'Cool Stuff',
                         'author': 'John',
                         'id': 'mykey',
                         'booktitle': 'My International Conference',
                         }]
        self.assertEqual(res, expected)

    def test_features2(self):
        with open('bibtexparser/tests/data/features2.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'type': 'inproceedings',
                         'year': '2014',
                         'title': 'Cool Stuff',
                         'author': 'John Doe',
                         'id': 'mykey',
                         'booktitle': 'My International Conference',
                         'note': 'Email: John.Doe@example.com',
                         'pages': '1--10',
                         }]
        self.assertEqual(res, expected)

    ###########
    # WRONG
    ###########
    def test_wrong(self):
        with open('bibtexparser/tests/data/wrong.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'author': 'correct',
                         'id': 'bar',
                         'type': 'article'}]
        self.assertEqual(res, expected)

    ###########
    # ENCODING
    ###########
    def test_encoding(self):
        with open('bibtexparser/tests/data/encoding.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read())
            res = bib.get_entry_list()
            expected = [{'keyword': 'keyword1, keyword2',
                              'type': 'article',
                              'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french érudit word',
                              'year': '2013',
                              'journal': 'Elémentaire',
                              'id': 'Cesar_2013',
                              'pages': '12-23',
                              'title': 'An amazing title: à',
                              'comments': 'A comment',
                              'author': 'Jean César',
                              'volume': '12',
                              'month': 'jan'
                         }]
        self.assertEqual(res, expected)

    def test_encoding_with_homogeneize(self):
        with open('bibtexparser/tests/data/encoding.bib', 'r') as bibfile:
            bib = BibTexParser(bibfile.read(), customization=homogeneize_latex_encoding)
            res = bib.get_entry_list()
            expected = [{'keyword': 'keyword1, keyword2',
                              'type': 'article',
                              'abstract': 'This is an abstract. This line should be long enough to test\nmultilines... and with a french {\\\'e}rudit word',
                              'year': '2013',
                              'journal': 'El{\\\'e}mentaire',
                              'id': 'Cesar_2013',
                              'pages': '12-23',
                              'title': '{A}n amazing title: {\\`a}',
                              'comments': 'A comment',
                              'author': 'Jean C{\\\'e}sar',
                              'volume': '12',
                              'month': 'jan'
                         }]
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
