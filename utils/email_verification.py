from selenium.webdriver.common.by import By as by
import time

def get_email(driver):
    driver.get("https://email-fake.com/"); time.sleep(7)
    try:
        return driver.find_element(by.XPATH, "//span[@id='email_ch_text']").text
    except Exception:
        return "error"
    
def get_code(driver, email):
    driver.get(f"https://email-fake.com/{email}"); time.sleep(7)
    try:
        return driver.title.split(" ")[0]
    except Exception:
        return "error_code"