# Authors: AJ Ristino and Carl Tankersley

import booksdatasource as bds
import argparse as ap

def main():
    data_source = bds.BooksDataSource('books1.csv')
    parser = ap.ArgumentParser(add_help=False)
    parser.add_argument("-t", "--title", nargs='*', type=str)
    parser.add_argument("-s", "--sort", type=str)
    parser.add_argument("-a", "--author", nargs='*', type=str)
    parser.add_argument("-y", "--year", nargs='*', type=int)
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args()
    if args.title is not None:
        if len(args.title) > 1:
            print("Please enter 0 or 1 arguments")
            exit()
        search_text = None if len(args.title) == 0 else args.title[0]
        if args.sort is not None:
            books_list = data_source.books(search_text, args.sort)
        else:
            books_list = data_source.books(search_text, args)
        book_strings = format_book_strings(books_list)
        print_strings(book_strings)
    elif args.author is not None:
        if len(args.author) > 1:
            print("Please enter 0 or 1 arguments")
            exit()
        search_text = None if len(args.author) == 0 else args.author[0]
        authors_list = data_source.authors(search_text)
        output = []
        for author in authors_list:
            output += format_author_strings([author])
            output += format_books_for_author(data_source.books_by_author(author))
        print_strings(output)
    elif args.year is not None:
        if len(args.year) > 2:
            print("Please enter 0-2 years")
            exit()
        if len(args.year) == 0:
            books_list = data_source.books_between_years()
        elif len(args.year) == 1:
            books_list = data_source.books_between_years(start_year=args.year[0])
        else:
            books_list = data_source.books_between_years(args.year[0], args.year[1])
        book_strings = format_book_strings(books_list)
        print_strings(book_strings)
    elif args.help:
        with open('usage.txt') as help_message:
            print(help_message.read())

def format_book_strings(books):
    '''Creates a string of the format 
        "title", publication_year, author
       for each Book object in the input list, and returns a list containing one such string
       for each object in the list.'''
    book_strings = []
    for book in books:
        author_string = ''
        for author in book.authors:
            author_string += author.given_name + ' ' + author.surname + ' '
        string = '"' + book.title + '", ' + str(book.publication_year) + ', ' + author_string
        book_strings.append(string)
    return book_strings

def format_books_for_author(books):
    '''Creates a string of the format 
            "title", publication_year
       for each Book object in the input list, and returns a list containing one such string
       for each object in the list.'''
    book_strings = []
    for book in books:
        string = '    "' + book.title + '", ' + str(book.publication_year)
        book_strings.append(string)
    return book_strings

def print_strings(strings):
    '''Prints each string in the input list on a new line'''
    for string in strings:
        print(string)

def format_author_strings(authors):
    '''Creates a string of the format 
        given_name surname (birth_year-death_year)
       for each Author object in the input list, and returns a list containing one such string
       for each object in the list.'''
    author_strings = []
    for author in authors:
        string = author.given_name + ' ' + author.surname + ' (' + str(author.birth_year) + '-'
        if author.death_year is not None:
            string += str(author.death_year)
        string += ')'
        author_strings.append(string)
    return author_strings

if __name__ == '__main__':
    main()