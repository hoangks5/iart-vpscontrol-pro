import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from gologin import getRandomPort

def get_random_port():
    return getRandomPort()

random_port = get_random_port() # uncomment to use random port

gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NmYwMDRhMGVkMGExMTE1MzRiNDQxOWMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NmYwMDRkMDU0NzQ3ZGM3ZWUxMzA0ODEifQ.iqMAKeYtXMgtO-epJwoLl10k96QQZQPwKRSeAaKlmq4",
	"profile_id": "66f004a2ed0a111534b44211",
	"port": random_port
	})

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.python.org")
time.sleep(3100)
driver.close()
gl.stop()
