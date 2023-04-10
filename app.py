

from flask import Flask, render_template, request, redirect, session, flash
import re
import pymongo
from flask import Flask, redirect, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Set up MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
user_collection = db["users"]

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = user_collection.find_one({"username": username, "password": password})
            if user:
                session['username'] = username
                session.setdefault('login_count', 0)
                session['login_count'] += 1
                user_type = user.get('user_type')
                if user_type == 'admin':
                    return redirect('/admin')
                else:
                    return redirect('/non_admin_dashboard')
            else:
                error = 'Invalid username or password'
        except:
            error = 'Error in fetching data from database'
    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    # code for admin dashboard goes here
    return render_template('admin.html')

@app.route('/non_admin_dashboard')
def non_admin_dashboard():
    # code for non-admin dashboard goes here
    return render_template('non_admin_dashboard.html')

# Route for adding a new user by admin
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            user_type = request.form['user-type']

            # Check if the username or email already exists in the database
            try:
                existing_user = user_collection.find_one({"$or": [{"username": username}, {"email": email}]})
                if existing_user:
                    if existing_user.get('username') == username:
                        return render_template('add.html', error='Username already exists')
                    elif existing_user.get('email') == email:
                        return render_template('add.html', error='Email already exists')
                else:
                    # Check if the password meets the requirements
                    if not re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!])(?!\s).{8,}$", password):
                        return render_template('add.html', error='Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character')
                    new_user = {"username": username, "email": email, "password":password, "user_type": user_type}
                    try:
                        user_collection.insert_one(new_user)
                        flash('User added successfully', 'success')
                        return redirect('/users')
                    except pymongo.errors.DuplicateKeyError:
                        return render_template('add.html', error='Username already exists')
            except:
                return render_template('add.html', error='Error in fetching data from database')
        else:
            return render_template('add.html')
    else:
        return redirect('/')

@app.route('/addweb/<website>/<email_or_id>/<password>', methods=['GET', 'POST'])
def add_login(website, email_or_id, password):
    if request.method == 'POST':
        website = request.form['website']
        email_or_id = request.form['email_or_id']
        password = request.form['password']
        
        # Check if the login information already exists in the database
        try:
            existing_user = user_collection.find_one({"website": website, "$or": [{"email": email_or_id}, {"id": email_or_id}]})
            if existing_user:
                return render_template('add.html', error='Login information already exists')
            else:
                new_user = {"website": website, "email": email_or_id, "id": email_or_id, "password": password}
                user_collection.insert_one(new_login)
                flash('Login information added successfully', 'success')
                return redirect('/logins')
        except:
            return render_template('add.html', error='Error in fetching data from database')
    else:
        return render_template('add.html')

# Redirect to the admin page
    return redirect('/admin')
@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            try:
                # Check if the user exists in the database
                existing_user = user_collection.find_one({"username": username})
                if existing_user:
                    if existing_user['user_type'] == 'admin':
                        return render_template('delete.html', error='Cannot delete an admin user')
                    else:
                        user_collection.delete_one({"username": username})
                       
                        return redirect('/admin')
                else:
                    return render_template('delete.html', error='User not found')
            except Exception as e:
                flash(f'Failed to delete user "{username}": {e}', 'error')
                return redirect('/admin')
        else:
            username = request.args.get('username')
            return render_template('delete.html', username=username)
    else:
        return redirect('/')







@app.route('/change', methods=['GET', 'POST'])
def update_user_role():
    if 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            user_type = request.form['new-role']
            try:
                # Check if the username exists in the database
                existing_user = user_collection.find_one({"username": username})
                if existing_user:
                    user_collection.update_one({"username": username}, {"$set": {"user_type": user_type}})
                    return redirect('/admin')
                else:
                    return render_template('change.html', error='Username not found', username=username)
            except Exception as e:
                return render_template('error.html', error=e)
        else:
            return render_template('change.html', username=request.args.get('username'))
    else:
        return redirect('/')




@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        try:
            # Get form data from POST request
            username = request.form['username']
            current_password = request.form['current_password']
            new_password = request.form['new_password']

            # Check if user exists in MongoDB database
            user = user_collection.find_one({'username': username})
            if user:

                # Check if current password is correct
                if user['password'] == current_password:

                    # Password validation
                    if not re.search(r'[A-Z]', new_password):
                        return "Password must contain at least one uppercase letter"
                    if not re.search(r'\d', new_password):
                        return "Password must contain at least one digit"
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                        return "Password must contain at least one special character"

                    # Update user's password in MongoDB database
                    user_collection.update_one({'username': username}, {'$set': {'password': new_password}})
                    return "Password updated successfully"
                else:
                    return render_template('change_password.html', error="Incorrect current password")
            else:
                return render_template('change_password.html', error="User not found")
        except Exception as e:
            return render_template('change_password.html', error="An error occurred: {}".format(str(e)))
    else:
        return render_template('change_password.html')


# Route for deleting an existing user by admin 


# Route for displaying a list of all users
@app.route('/users')
def users():
    if 'username' in session:
        try:
            # Retrieve all users from the database
            users = user_collection.find({})

            # Render the "users.html" template with the user data
            return render_template('users.html', users=users)
        except Exception as e:
            return render_template('users.html', error="An error occurred: {}".format(str(e)))
    else:
        return redirect('/')
@app.route("/Rafay")
def Rafay():

    # create a new Firefox driver instance
    driver = webdriver.Firefox()

    try:
        # navigate to the login page
        driver.get("https://console.rafay.dev/#/login")

        # wait for the email input field to become available
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        # enter the email and hit the next button
        email_input.send_keys("aadilazizkhan14@gmail.com")
        next_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        next_button.click()

        # wait for the password input field to become available
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        # enter the password and submit the login form
        password_input.send_keys("Adil@14jan")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return "Error occurred while trying to log in"

    else:
        # Perform the necessary actions after successful login
        # ...
        driver.quit()
        return "Successfully logged in to Rafay console"

@app.route('/Spectrocloud')
def Spectrocloud():
    try:
        driver = webdriver.Firefox()

        # navigate to the login page
        driver.get("https://console.spectrocloud.com/auth")

        # wait for the email input field to become available
        emailId_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "emailId"))
        )

        # enter the email and hit the Next button
        emailId_input.send_keys("aadilazizkhan14@gmail.com")
        next_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        next_button.click()

        # wait for the password input field to become available
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # enter the password and submit the login form
        password_input.send_keys("Adil@14jan")
        signin_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        signin_button.click()

        # wait for the dashboard page to load
        dashboard = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dashboard-container']"))
        )

        driver.quit()
        return response
    except Exception as e:
        driver.quit()
        return f"An error occurred: {e}"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')