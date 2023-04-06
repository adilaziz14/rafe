from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# create a new Firefox driver instance
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

# do something on the dashboard page
# ...

# close the browser window

