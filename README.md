# Project 1

 Web Programming with Python and JavaScript



INTRODUCTION:


Hi, This is my website(BookCheckerz) to see the ratings and reviews for a book.

I have used Goodreads API for this website.

In this website you can write a comment about a particular book and a rating too.

Users can see the comments and ratings other users have posted about any particular book.



HOW TO USE:


To post or see a review or rating user first have to make an account and log themselves in.

When a user will be logged in, they will be taken to a page where they can search for a book.
After their searched, they will be taken to a page where their searched book's details, review details(From Goodreads API), reviews and ratings will appear.


If a user wants to see an API of a particular book, they have to go to a route like /api/isbn where isbn is a book's isbn number.
Note that you can see the API even if you are not logged in.


FILES:



In this website, there is an application.py file which runs the whole backend.

For frontend, I have 7 .html files.


1. layout.html is the basic layout for all the web pages to follow.
2. index.html is the default page of the website.
3. register.html is to register a user to the website.
4. login.html is to log a user in to the website.
5. search.html is to search a book by title or author or year or isbn.
6. book_details.html is the details about the book which the user searched.
7. error.html is to handle errors.

Also, I have 5 .css files.

1. index.css runs for index.html.
2. register.css runs for register.html.
3. login.css runs for login.html
4. search.css runs for search.html.
5. book_details.css runs for book_details.html.

There is a books.csv file which contains the data of the books i.e title,author,year and isbn.

Import.py is to import all the books which are in books.csv to the database.

And finally, requirements.txt contains all the essential libraries which needs to be installed to run this website.




















