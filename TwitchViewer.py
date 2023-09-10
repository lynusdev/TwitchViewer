import warnings
import os
from os import system
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time
from datetime import timedelta
import requests

system(f"title {os.path.basename(__file__)[:-3]}")
os.system('mode con: cols=100 lines=10')
warnings.filterwarnings("ignore")

def stats():
    global stop
    global info
    global errors
    viewer_count = 0
    counter = 30
    while True:
        if stop == True:
            return
        elif counter == 30:
            try:
                data = {"operationName":"SearchResultsPage_SearchResults","variables":{"query":f"{username}","requestID":"712bd6c8-225e-4aac-a2e8-73ce80f013fd"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"6ea6e6f66006485e41dbe3ebd69d5674c5b22896ce7b595d7fce6411a3790138"}}}
                response = requests.post("https://gql.twitch.tv/gql", headers={"Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}, json=data)
                viewer_count = response.json()["data"]["searchFor"]["channels"]["edges"][0]["item"]["stream"]["viewersCount"]
            except:
                info = f"[System] Couldn't get viewer count!"
            counter = 0
        system(f"title {os.path.basename(__file__)[:-3]} - Threads: {viewers}/{threads} ^| Viewers: {viewer_count} ^| Time: {str(timedelta(seconds=(time() - start_time))).split('.')[0]} ^| Errors: {errors} ^| Info: {info}")
        counter += 1
        sleep(0.1)

def view(username, num):
    global viewers
    global errors
    global next_thread
    global stop
    global info
    global working_proxies
    first_iteration = True
    while True:
        if stop == True:
            return
        try:
            viewing = False
            proxy = proxies[0]
            del proxies[0]
            options = webdriver.ChromeOptions()
            options.add_argument("--lang=en")
            options.add_argument("--mute-audio")
            options.add_argument("--disable-application-cache")
            options.add_argument(f"--proxy-server={proxy}")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            if headless == "y":
                options.headless = True
            driver = webdriver.Chrome("chromedriver.exe", options=options)
            driver.maximize_window()
            driver.set_page_load_timeout(30)
            if first_iteration == True:
                next_thread = True
                first_iteration = False
            try:
                driver.get(f"https://www.twitch.tv/{username}")
            except:
                info = f"[Thread {num}] Proxy not working!"
                if proxy in working_proxies:
                    working_proxies.remove(proxy)
                raise ValueError('Proxy not working!')
            else:
                working_proxies.append(proxy)
                viewing = True
                info = f"[Thread {num}] Now viewing!"
                viewers += 1
            counter = 0
            while True:
                if stop == True:
                    return
                try:
                    driver.find_element(By.CSS_SELECTOR, "#root > div > div.Layout-sc-1xcs6mc-0.kBprba > div.Layout-sc-1xcs6mc-0.dajtya > main > div.root-scrollable.scrollable-area.scrollable-area--suppress-scroll-x > div.simplebar-scroll-content > div > div > div.InjectLayout-sc-1i43xsx-0.persistent-player > div > div.Layout-sc-1xcs6mc-0.video-player > div > div.Layout-sc-1xcs6mc-0.video-ref > div > div > div.Layout-sc-1xcs6mc-0.MIEJo.player-overlay-background.player-overlay-background--darkness-0.content-overlay-gate > div > div.Layout-sc-1xcs6mc-0.gRbxbd.content-overlay-gate__allow-pointers > button").click()
                    counter = 0
                except:
                    page_source = driver.page_source
                    if "This site can’t be reached" in page_source or "This page isn’t working" in page_source or "Error #2000" in page_source:
                        driver.refresh()
                        counter = 0
                    elif counter == 300:
                        info = f"[Thread {num}] Regaining focus!"
                        driver.minimize_window()
                        driver.maximize_window()
                    elif counter == 600:
                        info = f"[Thread {num}] Refreshing!"
                        driver.refresh()
                        counter = 0
                counter += 1
                sleep(1)
        except:
            if viewing == True:
                viewers -= 1
                info = f"[Thread {num}] Error while viewing!"
            else:
                info = f"[Thread {num}] Error while starting to view!"
            errors += 1
            try:
                driver.close()
            except:
                pass

username = input("Enter username: ")
with open("proxies.txt", "r") as f:
    proxies = f.read().splitlines()
while True:
    threads = int(input(f"Enter amount of viewers (max: {len(proxies)}): "))
    if threads > len(proxies):
        print(f"Max viewers: {len(proxies)}")
    else:
        break
while True:
    headless = input("Headless mode (y/n): ")
    if headless == "y" or headless == "n":
        break

viewers = 0
errors = 0
start_time = time()
stop = False
info = ""
working_proxies = []
Thread(target=stats).start()
for i in range(threads):
    t = Thread(target=view, args=(username, i+1))
    t.start()
    if i >= 10:
        next_thread = False
        while next_thread == False:
            sleep(3)
info = f"[System] Started all threads!"
input("Press ENTER to stop...")
stop = True
with open("proxies.txt", "r") as f:
    all_proxies = f.read().splitlines()
os.remove("proxies.txt")
with open("proxies.txt", "a+") as file:
    for proxy in working_proxies:
        file.write(f"{proxy}\n")
    for proxy in all_proxies:
        if proxy not in working_proxies:
            file.write(f"{proxy}\n")