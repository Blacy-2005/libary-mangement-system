import streamlit as st
import mysql.connector

# Database connection details (replace with your actual credentials)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "mysql123"
DB_NAME = "Library"

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

#----------------------------------------------------------------------------------------
#Admin Operation on Books
def display_book():
    """Displays book records with issued user info."""
    mydb = get_db_connection()
    if mydb:
        mycursor = mydb.cursor()
        mycursor.execute("""
            SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher, UserRecord.UserName, UserRecord.UserID
            FROM BookRecord
            LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
        """)
        records = mycursor.fetchall()
        mydb.close()

        if records:
            st.subheader("Book Records")
            st.table(records)
        else:
            st.info("No book records found.")

def insert_book():
    """Inserts a new book record."""
    st.subheader("Add New Book")
    book_id = st.text_input("BookID")
    book_name = st.text_input("Book Name")
    author = st.text_input("Author Name")
    publisher = st.text_input("Publisher Name")

    if st.button("Add Book"):
        if book_id and book_name and author and publisher:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "INSERT INTO BookRecord VALUES (%s, %s, %s, %s)"
                data = (book_id, book_name, author, publisher)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("Book added successfully!")
        else:
            st.warning("Please enter all book details.")

def delete_book():
    """Deletes a book record."""
    st.subheader("Delete Book")
    book_id = st.text_input("BookID to delete")

    if st.button("Delete"):
        if book_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(
                    "DELETE from BookRecord where BookID = {0} ".format(
                        "\'" + book_id + "\'"
                    )
                )
                mydb.commit()
                mydb.close()
                st.success("Book deleted successfully!")
        else:
            st.warning("Please enter BookID.")

def search_book():
    """Searches for a book record."""
    st.subheader("Search Book")
    search_id = st.text_input("BookID to search")

    if st.button("Search"):
        if search_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute("""
                    SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher, UserRecord.UserName, UserRecord.UserID
                    FROM BookRecord
                    LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
                    WHERE BookRecord.BookID = {0}
                """.format("\'" + search_id + "\'"))
                records = mycursor.fetchall()
                mydb.close()

                if records:
                    st.subheader("Search Result")
                    st.table(records)
                else:
                    st.info("Book not found.")
        else:
            st.warning("Please enter BookID to search.")

def update_book():
    """Updates a book record."""
    st.subheader("Update Book")
    book_id = st.text_input("BookID to update")
    book_name = st.text_input("Updated Book Name")
    author = st.text_input("Updated Author Name")
    publisher = st.text_input("Updated Publisher Name")

    if st.button("Update"):
        if book_id and book_name and author and publisher:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "UPDATE BookRecord SET Bookname = %s, Author = %s, Publisher = %s WHERE BookID = %s"
                data = (book_name, author, publisher, book_id)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("Book updated successfully!")
        else:
            st.warning("Please enter all book details.")

#----------------------------------------------------------------------------------------
#User Operation on Books
def book_list():
    """Displays all book records."""
    mydb = get_db_connection()
    if mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from BookRecord")
        records = mycursor.fetchall()
        mydb.close()

        if records:
            st.subheader("Book List")
            st.table(records)
        else:
            st.info("No books found.")

def issue_book():
    """Issues a book to a user."""
    user_id = st.text_input("Enter your UserID:")
    if st.button("Check Availability"):
        mydb = get_db_connection()
        if mydb:
            mycursor = mydb.cursor()
            mycursor.execute("Select BookID from UserRecord where UserID={0}".format("\'"+user_id+"\'"))
            checking = mycursor.fetchone()
            if checking == (None,):
                mycursor.execute("""
                    SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher, UserRecord.UserName, UserRecord.UserID
                    FROM BookRecord
                    LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
                """)
                records = mycursor.fetchall()
                available_books = []
                for row in records:
                    if row[5] is None:
                        available_books.append(row)

                if available_books:
                    st.subheader("Available Books")
                    st.table(available_books)
                    issue_id = st.text_input("Enter BookID to issue:")
                    if st.button("Issue Book"):
                        query = "UPDATE UserRecord SET BookID=%s WHERE UserID = %s"
                        data = (issue_id, user_id)
                        mycursor.execute(query, data)
                        mydb.commit()
                        mydb.close()
                        st.success("Book issued successfully!")
                else:
                    st.info("Sorry, no available books.")
            else:
                st.warning("Book already issued. Return that book first.")
            mydb.close()

def show_issued_book():
    """Shows the book issued to a user."""
    user_id = st.text_input("Enter your UserID:")
    if st.button("Show Issued Book"):
        mydb = get_db_connection()
        if mydb:
            mycursor = mydb.cursor()
            mycursor.execute("""
                SELECT UserID, UserName, UserRecord.BookID, BookName
                FROM Library.UserRecord INNER JOIN Library.BookRecord
                ON BookRecord.BookID = UserRecord.BookID
                WHERE UserID = {0}
            """.format("\'" + user_id + "\'"))
            records = mycursor.fetchall()
            mydb.close()
            if records:
                st.subheader("Issued Book")
                st.table(records)
            else:
                st.info("No book issued.")

def return_book():
    """Returns a book."""
    user_id = st.text_input("Enter your UserID:")
    book_id = st.text_input("Enter BookID to return:")
    if st.button("Return Book"):
        mydb = get_db_connection()
        if mydb:
            mycursor = mydb.cursor()
            query = """UPDATE UserRecord SET BookID = %s WHERE UserID = %s and BookID = %s"""
            data = (None, user_id, book_id)
            mycursor.execute(query, data)
            mydb.commit()
            mydb.close()
            st.success("Book returned successfully!")

def main():
    """Main function to create the Streamlit app."""
    st.title("Library Management")

    menu = ["Display Books", "Add Book", "Delete Book", "Search Book", "Update Book", "Book List", "Issue Book", "Show Issued Book", "Return Book"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Display Books":
        display_book()
    elif choice == "Add Book":
        insert_book()
    elif choice == "Delete Book":
        delete_book()
    elif choice == "Search Book":
        search_book()
    elif choice == "Update Book":
        update_book()
    elif choice == "Book List":
        book_list()
    elif choice == "Issue Book":
        issue_book()
    elif choice == "Show Issued Book":
        show_issued_book()
    elif choice == "Return Book":
        return_book()

if __name__ == "__main__":
    main()
