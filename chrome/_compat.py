from importlib.resources import path
from webdriver_manager.chrome import ChromeDriverManager as CM
import random, string, io, os, shutil, platform, subprocess, sys, zipfile, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver._compat as uc
from undetected_chromedriver.patcher import Patcher

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

def random_user_agent():
	return UserAgent(software_names=[SoftwareName.CHROME.value], hardware_types={HardwareType.COMPUTER.value}, limit=100).get_random_user_agent()

def setup_useragent(driver):
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": f"{random_user_agent}"})

def Proxy(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, i):
	try:
		manifest_json = """
		{
			"manifest_version": 2,
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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
          '{8237E44A-0054-442C-B6B6-EA0509993955}',
          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

def download_driver():
    OSNAME = platform.system()
    print(bcolors.WARNING + 'Getting Chrome Driver...' + bcolors.ENDC)
    if OSNAME == 'Linux':
        OSNAME = 'lin'
        EXE_NAME = ""
        with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
    elif OSNAME == 'Darwin':
        OSNAME = 'mac'
        EXE_NAME = ""
        process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
    elif OSNAME == 'Windows':
        OSNAME = 'win'
        EXE_NAME = ".exe"
        version = None
        try:
            process = subprocess.Popen(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            version = process.communicate()[0].decode(
                'UTF-8').strip().split()[-1]
        except:
            for i in CHROME:
                for j in ['opv', 'pv']:
                    try:
                        command = ['reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v', f'{j}', '/reg:32']
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
                    except:
                        pass
        if not version:
            print(bcolors.WARNING + "Couldn't find your Google Chrome version automatically!" + bcolors.ENDC)
            version = input(bcolors.WARNING + 'Please input your google chrome version (ex: 91.0.4472.114) : ' + bcolors.ENDC)
    else:
        print('{} OS is not supported.'.format(OSNAME))
        sys.exit()
    uc.install()

# print(download_driver())

def create_dirs():
    os.makedirs("data") if not os.path.exists("data") else False
    os.makedirs("data/driver") if not os.path.exists("data/driver") else False
    os.makedirs("data/browser-profiles") if not os.path.exists("data/browser-profiles") else False

create_dirs()

class Chrome():
    CHROMEDRIVER = None
    user_dir = None

    def __init__(self):
        # uc.install(); time.sleep(2.5)
        # download_driver()
        path = CM(path="data/driver").install()
        # if sys.platform == "win32":
        #     # shutil.move("chromedriver.exe", "data/driver")
        #     cd = os.path.abspath("data/driver/chromedriver.exe")
        # else:
        #     # shutil.move("chromedriver", "data/driver")
        #     time.sleep(2.5)
        #     #cd = os.path.abspath(path)
        # Patcher(executable_path=cd).patch_exe()
        self.CHROMEDRIVER = path
        Patcher.patch_exe = self.monkey_patch_exe
    
    @staticmethod
    def gen_random_cdc():
        cdc = random.choices(string.ascii_lowercase, k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def monkey_patch_exe(self):
        linect = 0
        replacement = self.gen_random_cdc()
        replacement = f"  var key = '${replacement.decode()}_';\n".encode()
        with io.open(self.CHROMEDRIVER, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"var key = " in line:
                    fh.seek(-len(line), 1)
                    fh.write(replacement)
                    linect += 1
            return linect
    
    def webdriver(self, i=None, proxy=False, headless=False, browser_profile=None, proxy_address=None):
        options = self.options(i=i, proxy=proxy, headless=headless, browser_profile=browser_profile, proxy_address=proxy_address)
        return webdriver.Chrome(executable_path=self.CHROMEDRIVER, options=options)

    def close(self, driver):
        driver.quit()

    def options(self, i=None, proxy=False, headless=False, browser_profile=None, proxy_address=None):
        chrome_options = Options()
        if proxy_address is not None and len(proxy_address.split(":")) == 2:
            chrome_options.add_argument("--proxy-server="+proxy_address)
        if proxy_address is not None and len(proxy_address.split(":")) == 4:
            i=random.randint(1000, 9999999)
            proxy = Proxy(*proxy_address.split(":"), i); time.sleep(1.5)
            chrome_options.add_extension(proxy)
            # chrome_options.add_argument(f'--load-extension='+proxy)
        if browser_profile is not None:
            os.makedirs("data/browser-profiles") if not os.path.exists("data/browser-profiles") else False
            # user_data_dir = user_data_dir = f'data/browser-profiles/{random.randint(1000, 9999)}-{"".join(random.choice(string.ascii_letters) for i in range(8))}'
            user_data_dir = f'data/browser-profiles/{browser_profile}'
            os.makedirs(user_data_dir) if not os.path.exists(user_data_dir) else False
            self.user_dir = user_data_dir
            chrome_options.add_argument("--user-data-dir=%s" % user_data_dir)
        if not headless:
            chrome_options.add_extension(os.path.abspath("creator/src/chrome/extensions/always_active.zip"))
            chrome_options.add_extension(os.path.abspath("creator/src/chrome/extensions/fingerprint_defender.zip"))
            chrome_options.add_extension(os.path.abspath("creator/src/chrome/extensions/spoof_timezone.zip"))
            chrome_options.add_extension(os.path.abspath("creator/src/chrome/extensions/webrtc_control.zip"))
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        chrome_options.add_argument('Content-Type="text/html"')
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('chartset=utf-8')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-crash-reporter")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--output=/dev/null")
        if proxy!=False and i!=None:
            chrome_options.add_extension(f"data/extension/proxy_auth_plugin_{i}.zip")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en_US,en'})
        chrome_options.add_argument('--disable-features=UserAgentClientHint')
        webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
        return chrome_options