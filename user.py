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

#--------------------------------------------------------------------------------------------------------------------------------
def display_user():
    """Displays user records with issued book info."""
    mydb = get_db_connection()
    if mydb:
        mycursor = mydb.cursor()
        mycursor.execute("""
            SELECT UserRecord.UserID, UserRecord.UserName, UserRecord.Password, BookRecord.BookName, BookRecord.BookID
            FROM UserRecord
            LEFT JOIN BookRecord ON UserRecord.BookID = BookRecord.BookID
        """)
        records = mycursor.fetchall()
        mydb.close()

        if records:
            st.subheader("User Records")
            st.table(records)
        else:
            st.info("No user records found.")

def insert_user():
    """Inserts a new user record."""
    st.subheader("Add New User")
    user_id = st.text_input("UserID")
    user_name = st.text_input("User Name")
    password = st.text_input("Password", type="password")

    if st.button("Add User"):
        if user_id and user_name and password:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "INSERT INTO UserRecord VALUES (%s, %s, %s, %s)"
                data = (user_id, user_name, password, None)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("User added successfully!")
        else:
            st.warning("Please enter all user details.")

def delete_user():
    """Deletes a user record."""
    st.subheader("Delete User")
    user_id = st.text_input("UserID to delete")

    if st.button("Delete"):
        if user_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(
                    "DELETE from UserRecord where UserID = {0} ".format(
                        "\'" + user_id + "\'"
                    )
                )
                mydb.commit()
                mydb.close()
                st.success("User deleted successfully!")
        else:
            st.warning("Please enter UserID.")

def search_user():
    """Searches for a user record."""
    st.subheader("Search User")
    search_id = st.text_input("UserID to search")

    if st.button("Search"):
        if search_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute("""
                    SELECT UserID, UserName, Password, BookName, UserRecord.BookID
                    FROM Library.UserRecord LEFT JOIN Library.BookRecord
                    ON BookRecord.BookID = UserRecord.BookID
                    WHERE UserRecord.UserID = {0}
                """.format("\'" + search_id + "\'"))
                records = mycursor.fetchall()
                mydb.close()

                if records:
                    st.subheader("Search Result")
                    st.table(records)
                else:
                    st.info("User not found.")
        else:
            st.warning("Please enter UserID to search.")

def update_user():
    """Updates a user record."""
    st.subheader("Update User")
    user_id = st.text_input("UserID to update")
    user_name = st.text_input("Updated User Name")
    password = st.text_input("Updated Password", type="password")

    if st.button("Update"):
        if user_id and user_name and password:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "UPDATE UserRecord SET Username = %s, Password = %s WHERE UserID = %s"
                data = (user_name, password, user_id)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("User updated successfully!")
        else:
            st.warning("Please enter all user details.")

def main():
    """Main function to create the Streamlit app."""
    st.title("User Management")

    menu = ["Display Users", "Add User", "Delete User", "Search User", "Update User"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Display Users":
        display_user()
    elif choice == "Add User":
        insert_user()
    elif choice == "Delete User":
        delete_user()
    elif choice == "Search User":
        search_user()
    elif choice == "Update User":
        update_user()

if __name__ == "__main__":
    main()
