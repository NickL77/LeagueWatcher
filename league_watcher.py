import sys
import time
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class LeagueWatcher():

    def __init__(self, username, password):
        options = Options()
        options.headless=False
        self.driver = webdriver.Chrome(options=options)
        self.match_links = []
        self.username = username
        self.password = password

    def watch_first(self, url, time_watch=20):

        self.driver.get(url)
        time.sleep(5)

        login_btn = self.driver.find_element_by_id('riotbar-account')
        login_btn.click()
        time.sleep(5)

        user_field = self.driver.find_element_by_name('username')
        user_field.send_keys(self.username)

        pass_field = self.driver.find_element_by_name('password')
        pass_field.send_keys(self.password)

        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        time.sleep(time_watch*60)

    def change_vid(self, url, time_watch=20):

        self.driver.get(url)
        time.sleep(time_watch*60)

    def watch_many(self, time_watch=20):
        self.watch_first(self.match_links[0], time_watch)
        for url in self.match_links[1:]:
            print("Swtiched to:", url)
            self.change_vid(url, time_watch)

    def get_links(self, url):

        self.driver.get(url)
        time.sleep(5)

        for match in self.driver.find_elements_by_class_name('VodsMatch'):
            link = match.find_element_by_tag_name('a').get_attribute('href')
            self.match_links.append(link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Automatically watch League VODs for missions.')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()

    lw = LeagueWatcher(args.username, args.password)
    lw.get_links("https://watch.lolesports.com/vods/lcs/lcs_2020_split1")
    lw.watch_many(20)
