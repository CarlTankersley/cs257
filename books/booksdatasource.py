#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.Authors = []
        with open(books_csv_file_name) as csvfile:
            reader = csv.reader(csvfile)
            self.Books = []
            for line in reader:
                temp_authors = self.parse_authors(line)
                self.Books.append(Book(line[0], int(line[1]), temp_authors))
                self.add_authors(temp_authors)
        self.Books = sorted(self.Books, key=lambda book: book.title)
        self.Authors = sorted(self.Authors, key=lambda author: (author.surname, author.given_name))

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authors = []
        search_text = '' if search_text is None else search_text.lower()
        for author in self.Authors:
            if search_text in author.surname.lower() or search_text in author.given_name.lower():
                authors.append(author)
        return sorted(authors, key=lambda author: (author.surname, author.given_name))

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        books = []
        if search_text is not None:
            for book in self.Books:
                if search_text in book.title.lower(): 
                    books.append(book)
        else:
            books = self.Books
        if sort_by == 'year':
            return sorted(books, key=lambda book: book.publication_year)
        return sorted(books, key=lambda book: book.title)

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        books = []
        if start_year is None:
            start_year = 0
        if end_year is None:
            end_year = 10000
        for book in self.Books:
            if book.publication_year <= end_year and book.publication_year >= start_year:
                books.append(book)
        return sorted(books, key=lambda book: book.publication_year)

    def books_by_author(self, author):
        '''Returns a list of all of the books in the data source written by a given author'''
        books_list = []
        for book in self.Books:
            if author in book.authors:
                books_list.append(book)
        return books_list

    def parse_authors(self, line):
        '''Parses a list of author fields from the CSV input file and returns a list of Author objects'''
        author_raw_data = line[2].split(' and ') # separate multiple authors
        authors_parsed = []
        for author in author_raw_data:
            curr_author = author.split() # [first_name, surname, '(birth_year-death_year)']
            if len(curr_author) > 3: # if the author has more than one given name
                first_name = curr_author[0] + ' ' + curr_author[1] # concatenate given names
                surname = curr_author[2]
                years = curr_author[3].strip('(').strip(')').split('-')
            else:
                first_name = curr_author[0]
                surname = curr_author[1]
                years = curr_author[2].strip('(').strip(')').split('-')
            birth_year = int(years[0])
            death_year = None if years[1] == '' else int(years[1])
            authors_parsed.append(Author(surname, first_name, birth_year, death_year)) 
        return authors_parsed

    def add_authors(self, author_list):
        '''Checks to see if each Author object in the list is in the data source and adds it to the 
           data source if the author is not already there'''
        for author in author_list:
            author_in_list = False
            for i in range(len(self.Authors)):
                if author == self.Authors[i]: # if trying to add an author already in the list...
                    author_in_list = True     #
                    break                     # ...don't
            if not author_in_list:
                self.Authors.append(author)
