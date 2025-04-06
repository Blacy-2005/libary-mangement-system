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

def display_admin():
    """Displays all admin records in a Streamlit table."""
    mydb = get_db_connection()
    if mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM AdminRecord")
        records = mycursor.fetchall()
        mydb.close()

        if records:
            st.subheader("Admin Records")
            st.table(records)
        else:
            st.info("No admin records found.")

def insert_admin():
    """Inserts a new admin record based on user input."""
    st.subheader("Add New Admin")
    admin_id = st.text_input("AdminID")
    password = st.text_input("Password", type="password")

    if st.button("Add Admin"):
        if admin_id and password:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "INSERT INTO AdminRecord VALUES (%s, %s)"
                data = (admin_id, password)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("Admin added successfully!")
        else:
            st.warning("Please enter both AdminID and Password.")

def delete_admin():
    """Deletes an admin record based on user input."""
    st.subheader("Delete Admin")
    admin_id = st.text_input("AdminID to delete")

    if st.button("Delete"):
        if admin_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(
                    "DELETE from AdminRecord where AdminID={0}".format(
                        "\'" + admin_id + "\'"
                    )
                )
                mydb.commit()
                mydb.close()
                st.success("Admin deleted successfully!")
        else:
            st.warning("Please enter AdminID.")

def search_admin():
    """Searches and displays an admin record based on AdminID."""
    st.subheader("Search Admin")
    search_id = st.text_input("AdminID to search")

    if st.button("Search"):
        if search_id:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(
                    "SELECT * FROM AdminRecord where AdminID={0}".format(
                        "\'" + search_id + "\'"
                    )
                )
                records = mycursor.fetchall()
                mydb.close()

                if records:
                    st.subheader("Search Result")
                    st.table(records)
                else:
                    st.info("Admin not found.")
        else:
            st.warning("Please enter AdminID to search.")

def update_admin():
    """Updates an admin's password."""
    st.subheader("Update Admin Password")
    admin_id = st.text_input("AdminID to update")
    new_password = st.text_input("New Password", type="password")

    if st.button("Update"):
        if admin_id and new_password:
            mydb = get_db_connection()
            if mydb:
                mycursor = mydb.cursor()
                query = "UPDATE AdminRecord SET Password = %s WHERE AdminID=%s"
                data = (new_password, admin_id)
                mycursor.execute(query, data)
                mydb.commit()
                mydb.close()
                st.success("Password updated successfully!")
        else:
            st.warning("Please enter AdminID and new Password.")

def main():
    """Main function to create the Streamlit app."""
    st.title("Admin Management")

    menu = ["Display Admins", "Add Admin", "Delete Admin", "Search Admin", "Update Admin"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Display Admins":
        display_admin()
    elif choice == "Add Admin":
        insert_admin()
    elif choice == "Delete Admin":
        delete_admin()
    elif choice == "Search Admin":
        search_admin()
    elif choice == "Update Admin":
        update_admin()

if __name__ == "__main__":
    main()
