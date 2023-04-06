from flask import Flask, redirect, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# define the route for the login page
@app.route("/logins")
def logins():
    # create a new Firefox driver instance
    driver = webdriver.Firefox()

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



if __name__ == "__main__":
    app.run()
