import streamlit as st
import Operations  # Assuming Operations.py contains the required functions

def admin_menu():
    """Streamlit interface for the Admin Menu."""
    st.title("Admin Menu")
    menu = [
        "Book Management",
        "User Management",
        "Admin Management",
        "User Feedback and Ratings Table",
        "Logout",
    ]
    choice = st.selectbox("Select an option:", menu)

    if choice == "Book Management":
        Operations.book_management() #Ensure these functions are correct in Operations.py
    elif choice == "User Management":
        Operations.user_management()
    elif choice == "Admin Management":
        Operations.admin_management()
    elif choice == "User Feedback and Ratings Table":
        Operations.feedback_table()
    elif choice == "Logout":
        st.write("Thanks for visiting our Library:))")
        st.write("Logged out of the system")
        # You might want to clear session state or redirect here.
    else:
        st.warning("Wrong Choice......Enter Your Choice again")

def user_menu():
    """Streamlit interface for the User Menu."""
    st.title("User Menu")
    menu = ["Book Centre", "Feedback and Ratings", "Logout"]
    choice = st.selectbox("Select an option:", menu)

    if choice == "Book Centre":
        Operations.book_centre() #Ensure these functions are correct in Operations.py
    elif choice == "Feedback and Ratings":
        Operations.feedback()
    elif choice == "Logout":
        st.write("Thanks for visiting our Library:))")
        st.write("Logged out of the system")
        # You might want to clear session state or redirect here.
    else:
        st.warning("Wrong Choice......Enter Your Choice again")

def main():

    menu_type = st.radio("Select Menu Type", ("Admin", "User"))

    if menu_type == "Admin":
        admin_menu()
    elif menu_type == "User":
        user_menu()

if __name__ == "__main__":
    main()
