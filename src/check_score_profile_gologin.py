import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from gologin import getRandomPort
from bs4 import BeautifulSoup
import json
import os
import requests
def get_random_port():
    return getRandomPort()

random_port = get_random_port() # uncomment to use random port

def list_profile_id(api_key):
        url = "https://api.gologin.com/browser/v2"
        payload = {}
        headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            # lưu response vào file json
           list_profile = response.json()['profiles']
           list_profile = [profile['id'] for profile in list_profile]
           return list_profile
       


def get_score(profile_id, api_key):
	gl = GoLogin({
		"token": api_key,
		"profile_id": profile_id,
		"port": random_port,
		"is_cloud_headless": True,
		})
	score_full = {
		"profile_id": profile_id,
	}
	debugger_address = gl.start()
	chrome_options = Options()
	chrome_options.add_experimental_option("debuggerAddress", debugger_address)
	# headless mode
	driver = webdriver.Chrome(options=chrome_options)
	driver.get("https://ipfighter.com/")
	time.sleep(2)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	score = soup.find("text", class_="CircularProgressbar-text").text.strip().replace("%", "")
	# tìm thẻ img có class = home_flagIp__gz1ix
	country = soup.find("img", class_="home_flagIp__gz1ix")["alt"]
	score_full["country"] = country
	if score == "100":
		score_full["score_proxy"] = 100
		score_full["recommend_proxy"] = "Proxy is good"
	else:
		# tìm button có class home_btnLink__m_4M4
		button = driver.find_element("class name", "home_btnLink__m_4M4")
		button.click()
		time.sleep(1)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	# tìm thẻ text có class là CircularProgressbar-text
	score = soup.find("text", class_="CircularProgressbar-text").text
	ip_address = soup.find_all("div", class_="dflex")[1].text
	score_full["ip_address"] = ip_address
	score_full["score_proxy"] = int(score.strip().replace("%", ""))

	# tìm thẻ small
	small = driver.find_elements("tag name", "small")
	info = []
	for s in small:
		info.append(s.text)
	score_full["recommend_proxy"] = '\n'.join(info)

	driver.get("https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html")
	time.sleep(1)

	for i in range(30):
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		score = soup.find("big", id="score").text
		if 'Your score is' not in score:
			time.sleep(1)
		else:
			score = score.strip().split(":")[-1].strip()
			score = int(float(score)*100)
			score_full["score_browser"] = score
			break
	# ghi dữ liệu tiếp vào file json
	# kiểm tra có thư mục json , score chưa
	if not os.path.exists("src/json/score"):
		os.makedirs("src/json/score")
  
 
	with open(f"src/json/score/{profile_id}.json", "w", encoding="utf-8") as f:
		json.dump(score_full, f)
	driver.close()
	gl.stop()


