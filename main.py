from cgitb import text
from selenium.webdriver.common.by import By as by

from .chrome._compat import Chrome
from .utils.phone_verification import PhoneVerification
from .utils.email_verification import get_email, get_code

import requests, json, time, os, random

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

def random_user_agent():
	return UserAgent(software_names=[SoftwareName.CHROME.value], hardware_types={HardwareType.COMPUTER.value}, limit=100).get_random_user_agent()

def get_random_name():
    return json.loads(requests.get("https://api.namefake.com/").text)["name"]

def check_phone_verification(driver, api_key):
    if driver.current_url == "https://twitter.com/account/access":
        try:
            driver.find_element(by.XPATH, "//select[@id='country_code']/option[@value='7']")
            pv = PhoneVerification(api_key)
            number, _id = pv.get_number()
            phone_number = driver.find_element(by.XPATH, "//input[@name='']"); phone_number.click(); phone_number.send_keys(number)
            time.sleep(0.5)
            driver.find_element(by.XPATH, "//input[@value='Next']").click(); time.sleep(5.5)
            ver = driver.find_element(by.XPATH, "//input[@name='pin']")
            time.sleep(5.5)
            ver_code = pv.get_sms(_id)
            ver.click(); ver.send_keys(ver_code); time.sleep(1.5)
            driver.find_element(by.XPATH, "//input[@value='Next']").click(); time.sleep(5.5)
        except Exception:
            pass

def __init__(proxy_address=None, headless=False):
    chrome = Chrome()
    return chrome.webdriver(proxy_address=proxy_address)

def signup(api_key, url, text, proxy=None):
    # checker=True
    # while checker:
    #     driver = __init__(proxy_address=proxy)
    #     try:
    #         driver.execute_cdp_cmd("Network.setUserAgentOverride", {"UserAgent": f"{random_user_agent()}"})
    #     except Exception:
    #         pass
    #     driver.get("https://twitter.com/i/flow/signup"); time.sleep(7)
    #     if driver.find_element(by.XPATH, "//span[contains(text(), 'Use email instead')]").is_displayed():
    #         checker=False
    #     else:
    #         driver.close()
    #     time.sleep(2.5)
    driver = __init__(proxy_address=proxy)
    # driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": f"{random_user_agent()}"})
    driver.get("https://twitter.com/i/flow/signup"); time.sleep(17)
    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Sign up with phone or email')]").click(); time.sleep(10)
    except:
        pass
    try:
        # driver.find_element(by.XPATH, "//span[contains(text(), 'Use email instead')]").click(); time.sleep(1.5)
        _email = driver.find_element(by.XPATH, "//input[@name='phone_number']")
        # driver.execute_script("window.open('')")
        # driver.switch_to.window(driver.window_handles[1])
        # email = get_email(driver)
        pv = PhoneVerification(api_key)
        number, _id = pv.get_number()
        number = f"+34{number}"
        time.sleep(3.5)
        # driver.switch_to.window(driver.window_handles[0])
        _email.click(); _email.send_keys(f"{number}")
    except Exception:
        pass

    try:
        name = get_random_name()
        _name = driver.find_element(by.XPATH, "//input[@name='name']")
        _name.click(); _name.send_keys(name); time.sleep(1.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//select[@id='SELECTOR_1']/option[@value='1']").click(); time.sleep(0.5)
        driver.find_element(by.XPATH, "//select[@id='SELECTOR_2']/option[@value='1']").click(); time.sleep(0.5)
        driver.find_element(by.XPATH, "//select[@id='SELECTOR_3']/option[@value='1987']").click(); time.sleep(0.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Sign up')]").click(); time.sleep(5.5)
    except Exception:
        pass
    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'OK')]").click(); time.sleep(5.5)
    except Exception:
        pass
    time.sleep(105)
    try:
        ver = driver.find_element(by.XPATH, "//input[@name='verfication_code']")
        # driver.switch_to.window(driver.window_handles[1])
        # ver_code = get_code(driver, email)
        check=True
        while check:
            # text_res = get_sms(_id)
            ver_code = pv.get_sms(_id)
            if ver_code != "" and ver_code != None:
                check =False
            time.sleep(5)
        time.sleep(3.5)
        # driver.switch_to.window(driver.window_handles[0])
        ver.click(); ver.send_keys(ver_code)
        time.sleep(1.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
    except Exception:
        pass

    # try:
    #     country = driver.find_element(by.XPATH, "//select[@id='SELECTOR_7']/option[@value='RU']")
    #     country.click(); time.sleep(0.5)
    #     phone_number = driver.find_element(by.XPATH, "//input[@name='phone_number']")
    #     pv = PhoneVerification(api_key)
    #     number, _id = pv.get_number()
    #     phone_number.click(); phone_number.send_keys(number); time.sleep(0.5)
    # except Exception as e:
    #     # print(e)
    #     pass

    # try:
    #     driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(1.5)
    #     driver.find_element(by.XPATH, "//span[contains(text(), 'OK')]").click(); time.sleep(5.5)
    # except Exception:
    #     pass

    # try:
    #     phone_ver = driver.find_element(by.XPATH, "//input[@name='verfication_code']")
    #     time.sleep(5.5)
    #     ver_code = pv.get_sms(_id)
    #     phone_ver.click(); phone_ver.send_keys(ver_code)
    #     time.sleep(1.5)
    # except Exception:
    #     pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
        # time.sleep(60*24)
    except Exception:
        pass

    try:
        password = driver.find_element(by.XPATH, "//input[@name='password']"); password.click(); password.send_keys("Vojko123")
        time.sleep(5.5)
    except Exception:
        pass

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
        # time.sleep(60*24)
    except Exception:
        pass

    # check_phone_verification(driver, api_key)
    
    if not os.path.exists("data/accounts"):
        os.makedirs("data/accounts")

    try:
        driver.find_element(by.XPATH, "//span[contains(text(), 'Accept all cookies')]").click(); time.sleep(5.5)
    except:
        pass
    try:
        img_name = random.randint(1000, 9999)
        open(f"data/{img_name}.jpg", "wb").write(requests.get("https://thispersondoesnotexist.com/image").content)
        # img_info = random.choice(list(filter(None, open("infos.txt", "r").read().split("\n"))))
        # img_name = img_info.split("\t")[0]
        # bio = img_info.split("\t")[1]
        time.sleep(3.5)
        try:
            driver.find_elements(by.XPATH, "//input[@data-testid='fileInput']")[1].send_keys(os.path.abspath(f"data/{img_name}.jpg")) # f"data/{img_name}.jpg"
        except:
            try:
                driver.find_element(by.XPATH, "//input[@data-testid='fileInput']").send_keys(os.path.abspath(f"data/{img_name}.jpg")) # f"data/{img_name}.jpg"
            except:
                pass
        time.sleep(1.5)
        driver.find_element(by.XPATH, "//span[contains(text(), 'Apply')]").click(); time.sleep(1.5)
        driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
        os.remove(f"data/{img_name}.jpg")
        # os.remove(f"data/{img_name}")
    except Exception as e:
        # print(e)
        pass

    # try:
    #     txt_area = driver.find_element(by.XPATH, '//textarea[@data-testid="ocfEnterTextTextInput"]')
    #     txt_area.click(); txt_area.send_keys(bio); time.sleep(0.5)
    #     driver.find_element(by.XPATH, "//span[contains(text(), 'Next')]").click(); time.sleep(5.5)
    # except:
    #     pass

    try:
        driver.get("https://twitter.com"); time.sleep(7)
        try:
            driver.find_element(by.XPATH, "//span[contains(text(), 'Profile')]").click(); time.sleep(7)
        except:
            try:
                driver.find_element(by.XPATH, "//a[@data-testid='AppTabBar_Profile_Link']").click(); time.sleep(7)
            except:
                pass
        try:
            username_ = driver.current_url.replace("https://twitter.com/", "")
        except:
            username_ = ""
        img_name = random.randint()
        open(f"data/{img_name}.jpg", "wb").write(requests.get("https://thispersondoesnotexist.com/image").content)
        try:
            driver.find_element(by.XPATH, "//span[contains(text(), 'Edit profile')]").click(); time.sleep(5.5)
        except:
            try:
                driver.find_element(by.XPATH, "//span[contains(text(), 'Set Up Profile')]").click(); time.sleep(5.5)
            except:
                try:
                    driver.find_element(by.XPATH, "//span[contains(text(), 'Set up profile')]").click(); time.sleep(5.5)
                except:
                    pass
        # driver.find_element(by.XPATH, "//input[@data-testid='fileInput']").send_keys(f"data/{img_name}.jpg")
        driver.find_elements(by.XPATH, "//input[@data-testid='fileInput']")[1].send_keys(os.path.abspath(f"data/{img_name}.jpg"))
        time.sleep(1.5)
        driver.find_element(by.XPATH, "//span[contains(text(), 'Apply')]").click(); time.sleep(1.5)
        driver.find_element(by.XPATH, "//span[contains(text(), 'Save')]").click(); time.sleep(5.5)
    except:
        pass

    from .utils.commenting import comments

    # driver.get(url); time.sleep(7)
    # comments(driver, text)
    time.sleep(1.5)
    
    os.makedirs("data/accounts") if not os.path.exists("data/accounts") else False
    accounts = open("data/accounts/accounts.txt", "a")
    accounts.write(f"{number}:Vojko123:{username_}\n")
    accounts.close()
    
    driver.quit()