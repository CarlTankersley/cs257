'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == booksdatasource.Author('Pratchett', 'Terry'))

    def test_unique_title(self):
        titles = self.data_source.books('Beloved')
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0] == booksdatasource.Book('Beloved'))

    def test_title_sort(self):
        titles = self.data_source.books()
        prev_book = titles[0]
        for book in titles:
            self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

    def test_author_search(self):
        authors = self.data_source.authors("Christie")
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], booksdatasource.Author("Christie", "Agatha"))

    def test_all_authors(self):
        authors = self.data_source.authors()
        self.assertEqual(len(authors), 22)

    def test_author_same_surname(self):
        authors = self.data_source.authors("Bront")
        self.assertEqual(len(authors), 3)
        self.assertEqual(authors[0], booksdatasource.Author("Brontë", "Ann"))
        self.assertEqual(authors[1], booksdatasource.Author("Brontë", "Charlotte"))
        self.assertEqual(authors[2], booksdatasource.Author("Brontë", "Emily"))

    def test_default_sort(self):
        titles = self.data_source.books(None, "random_thing")
        prev_book = titles[0]
        for book in titles:
            self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

    def test_between_year_sort(self):
        years = self.data_source.books_between_years(1937, 2010)
        prev_book = years[0]
        for book in years:
            self.assertLessEqual(book.publication_year,2010)
            self.assertGreaterEqual(book.publication_year,1937)
            self.assertLessEqual(prev_book.publication_year,book.publication_year)
            if(prev_book.publication_year == book.publication_year):
                self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

    def test_year_sort(self):
        years = self.data_source.books()
        prev_book = years[0]
        for book in years:
            if(prev_book.publication_year == book.publication_year):
                self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

    def test_start_year_only_sort(self):
        years = self.data_source.books_between_years(start_year=1939)
        prev_book = years[0]
        for book in years:
            self.assertGreaterEqual(book.publication_year,1939)
            self.assertLessEqual(prev_book.publication_year,book.publication_year)
            if(prev_book.publication_year == book.publication_year):
                self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

    def test_end_year_only_sort(self):
        years = self.data_source.books_between_years(end_year=2010)
        prev_book = years[0]
        for book in years:
            self.assertLessEqual(book.publication_year,2010)
            self.assertLessEqual(prev_book.publication_year,book.publication_year)
            if(prev_book.publication_year == book.publication_year):
                self.assertLessEqual(prev_book.title.lower(), book.title.lower())
            prev_book = book

if __name__ == '__main__':
    unittest.main()

