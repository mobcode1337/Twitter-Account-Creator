from selenium import webdriver
from datetime import datetime
import undetected_chromedriver.v2 as uc

import random, os, string, zipfile, time

os.makedirs("data") if not os.path.exists("data") else False

def Proxy(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, i):
	try:
		manifest_json = """
		{
			"manifest_version": 3,
			"name": "Proxy Manager",
			"version": "3.0.11",
			"permissions": [
				"proxy",
				"tabs",
				"unlimitedStorage",
				"storage",
				"<all_urls>",
				"webRequest",
				"webRequestBlocking"
			],
			"background": {
				"scripts": ["background.js"]
			},
			"minimum_chrome_version":"22.0.0"
		}
		"""

		background_js = string.Template(
		"""
		var config = {
				mode: "fixed_servers",
				rules: {
				singleProxy: {
					scheme: "http",
					host: "${PROXY_HOST}",
					port: parseInt(${PROXY_PORT})
				},
				bypassList: ["foobar.com"]
				}
			};
		chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
		function callbackFn(details) {
			return {
				authCredentials: {
					username: "${PROXY_USER}",
					password: "${PROXY_PASS}"
				}
			};
		}
		chrome.webRequest.onAuthRequired.addListener(
					callbackFn,
					{urls: ["<all_urls>"]},
					['blocking']
		);
		"""
		).substitute(
			PROXY_HOST=PROXY_HOST,
			PROXY_PORT=PROXY_PORT,
			PROXY_USER=PROXY_USER,
			PROXY_PASS=PROXY_PASS)
        
		if not os.path.exists("data/extension"):
			os.makedirs("data/extension")

		with zipfile.ZipFile(f'data/extension/proxy_auth_plugin_{i}.zip', 'w', zipfile.ZIP_DEFLATED, False) as zp:
			zp.writestr('manifest.json', manifest_json)
			zp.writestr('background.js', background_js)
		return f"data/extension/proxy_auth_plugin_{i}.zip"
	except Exception as e:
		return False
		now = datetime.now().strftime('%H:%M:%S')
		print(f'[{now}] - {e}')

class Chrome():
    CHROMEDRIVER = None
    chrome_num = random.randint(1000, 9999)
    user_dir = None

    def __init__(self):
        pass
    
    def webdriver(self, i=None, proxy=False, headless=False, proxy_address=None, browser_profile=None):
        options = self.options(i=i, proxy=proxy, headless=headless, proxy_address=proxy_address, browser_profile=browser_profile)
        return uc.Chrome(executable_path=self.CHROMEDRIVER, options=options)

    def close(self, driver):
        driver.quit()

    def options(self, i=None, proxy=False, headless=False, proxy_address=None, browser_profile=None):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        if proxy!=False and i!=None:
            chrome_options.add_extension(f"data/extension/proxy_auth_plugin_{i}.zip")
            # chrome_options.add_argument(f'--load-extension=data/extension/proxy_auth_plugin_{i}.crx')
        if proxy_address is not None and len(proxy_address.split(":")) == 2:
            chrome_options.add_argument("--proxy-server="+proxy_address)
        if proxy_address is not None and len(proxy_address.split(":")) == 4:
            i=random.randint(1000, 9999999)
            proxy = Proxy(*proxy_address.split(":"), i); time.sleep(1.5)
            chrome_options.add_extension(proxy)
            chrome_options.add_argument(f'--load-extension='+proxy)
        if browser_profile is not None:
            os.makedirs("data/browser-profiles") if not os.path.exists("data/browser-profiles") else False
            # user_data_dir = user_data_dir = f'data/browser-profiles/{random.randint(1000, 9999)}-{"".join(random.choice(string.ascii_letters) for i in range(8))}'
            user_data_dir = f'data/browser-profiles/{browser_profile}'
            os.makedirs(user_data_dir) if not os.path.exists(user_data_dir) else False
            self.user_dir = user_data_dir
            chrome_options.add_argument("--user-data-dir=%s" % user_data_dir)
        chrome_options.add_argument('--mute-audio')
        # chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        return chrome_options