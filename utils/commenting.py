from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys as k
import os, time

def comments(driver, text):
    # driver.get(url); time.sleep(7)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    try:
        # add_comment = driver.find_element(by.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[5]/div/div[1]/div/div/div/svg")
        # add_comment.click(); time.sleep(3.5)
        add_comment = driver.find_element(by.XPATH, "//div[@data-testid='reply']")        
        add_comment.click(); time.sleep(3.5)
        add_comment = driver.find_element(by.XPATH, "//div[@data-testid='tweetTextarea_0']")
        add_comment.click(); add_comment.send_keys(text); time.sleep(1.5)
        add_comment.send_keys(" "); time.sleep(1.5)
        try:
            driver.find_element(by.XPATH, "//span[contains(text(), 'Reply')]").click()
        except:
            try:
                driver.find_element(by.XPATH, "//span[contains(text(), 'Tweet')]").click()
            except:
                try:
                    add_comment.send_keys(k.ENTER)
                except:
                    pass
        # driver.find_element(by.XPATH, "//span[contains(text(), 'Tweet')]").click()
        time.sleep(5.5)
        e="Success comment"
    except Exception as e:
        # print(e)
        return e
        pass
    return e