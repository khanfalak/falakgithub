import streamlit as st
import mysql.connector
import hashlib
#to use button feature
from streamlit_extras.switch_page_button import switch_page

home = st.button("Home page!")
if home:
    switch_page("Home")

# Custom SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Create a session state object
session_state = SessionState(page="Home")

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PHW#84#jeor",
    database="userstable"
)
cursor = db.cursor()

# Hashing Function
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# DB Functions
def create_usertable():
    cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username VARCHAR(255), password VARCHAR(255))')

def add_userdata(username, password):
    cursor.execute('INSERT INTO userstable(username, password) VALUES (%s, %s)', (username, password))
    db.commit()

def login_user(username, password):
    cursor.execute('SELECT * FROM userstable WHERE username = %s', (username,))
    user = cursor.fetchone()
    if user and check_hashes(password, user[1]):
        return True
    return False

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def main():
    st.title("Patient's Login App")

    menu = [ "Login", "SignUp"]
    choice = st.selectbox("Menu", menu)

    #if choice == "Home":
       # st.subheader("Home")
    #home = st.button("Home page!")
   # if home:
        #switch_page("Home")

    if choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()

            if login_user(username, password):
                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task", ["Predict disease", "Book an appointment", "Book an ambulance"])
                
                if task == "Predict disease":
                    disease = st.button("predict disease")
                    if disease:
                        switch_page("predict_disease")

                    st.header("predict_disease")

                elif task == "Book an appointment":
                    st.subheader("appointment")

                elif task == "Book an ambulance":
                    st.subheader("ambulance")

                #elif task == "Profiles":
                    #st.subheader("User Profiles")
                    #cursor.execute('SELECT * FROM userstable')
                    #user_result = cursor.fetchall()
                    #clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    #st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            hashed_password = make_hashes(new_password)
            add_userdata(new_user, hashed_password)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

if __name__ == '__main__':
    # Create the user table only once when the app starts
    create_usertable()
    main()
