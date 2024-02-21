from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time


# Replace these with your actual credentials
username = "7004697128"
password = "123456"

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed and in PATH
driver.get("https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id=8586493d-c97a-4f44-a767-7c23a81fd150&redirect_uri=https://web23.com")  # Or the URL for Upstox's login page

# Locate username and password fields and fill them
username_field = driver.find_element(By.ID, "mobileNum")  # Replace "mobileNum" with the actual ID
password_field = driver.find_element(By.ID, "password")   # Replace "password" with the actual ID
username_field.send_keys(username)
password_field.send_keys(password)

# Submit the form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(50)  # You might need to adjust this depending on the speed of your internet connection and the responsiveness of the website

# You can add further actions here, like navigating to a specific page after login

# Close the browser
driver.quit()
