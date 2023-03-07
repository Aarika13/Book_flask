from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

# books_list = [
#     {
#         "id" :  0,
#         "author" : "AAA",
#         "language" : "English",
#         "title" : "Things fall apart"
#     },

#     {
#         "id" :  1,
#         "author" : "BBB",
#         "language" : "English",
#         "title" : "Things fall apart"
#     },

#     {
#         "id" :  2,
#         "author" : "ccc",
#         "language" : "English",
#         "title" : "Things fall apart"
#     },

#     {
#         "id" :  3,
#         "author" : "DDD",
#         "language" : "English",
#         "title" : "Things fall apart"
#     },

#     {
#         "id" :  4,
#         "author" : "EEE",
#         "language" : "English",
#         "title" : "Things fall apart"
#     }
# ]

def db_connection():
    conn =  None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn
    
@app.route('/books',methods =['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0],author = row[1],language =row[2], title = row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author,language,title)
        VALUES(?,?,?)"""

        cursor = conn.execute(sql,(new_author,new_lang,new_title))
        conn.commit()
        return f"Book with the id:{cursor.lastrowid} created successfully",201
    
@app.route('/book/<int:id>',methods = ['GET' ,'PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?",(id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book),200
        else:
            return "Something Wrong",404
        
    if request.method == 'PUT':
        sql = """UPDATE book 
        SET title=?,
        author = ?,
        language=?
        WHERE id=?"""
        book['author'] = request.form['author']
        book['title'] = request.form['title']
        book['language'] = request.form['language']
        updated_book = {
            'id' : id,
            'author' : book['author'],
            'title' : book['title'],
            'language' : book['language']
        }
        conn.execute(sql,(author , language, title ,id))
        conn.commit()
        return jsonify(updated_book)    

    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql,(id,))
        conn.commit()
        return "The book with id:{} has been deleted ".format(id),200
    
if __name__ == '__main__':
    app.run()