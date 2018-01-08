from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import *
import os


class Driver:
    def __init__(self, mainLogFile):
        f_driver = open("driver_name.txt", "r")
        driver_name = f_driver.read()
        self.driver = webdriver.Chrome(driver_name)
        self.driver.set_page_load_timeout(30)
        self.logFile = mainLogFile

    def get_log_file(self):
        return self.logFile

    def set_log_file(self, logFile):
        self.logFile = logFile

    def open_browser(self, url, debug=True):
        try:
            self.driver.get(url)
        except Exception as exception:
            self.log_message(exception)
            if "TimeoutException" in exception:
                self.driver.refresh()
                sleep(60)
        if not self.check_right_page(url):
            if debug:
                self.log_message("not is correct page.")
            self.driver.get(url)
            if not self.check_right_page(url):
                self.log_message("still not in the correct page.")
                assert False, "fail to open the browser"
            else:
                self.log_message("back to main page in second time")

    def refresh(self):
        self.driver.refresh()

    def current_url(self):
        return self.driver.current_url

    def close_browser(self):
        self.driver.close()

    def check_right_page(self, url):
        return str(self.driver.current_url) == str(url)

    def driver_wait(self, xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def click_element(self, xpath=None, ele=None, inActionChain=False):
        if ele is None:
            ele = self.driver.find_element_by_xpath(xpath)
        try:
            ele.click()
        except Exception as exception:
            self.log_message(exception)
            if "TimeoutException" in exception and not inActionChain:
                self.driver.refresh()
                sleep(60)
                ele.click()
            elif "is not clickable at point" in exception and not inActionChain:
                self.scroll_to_top()
                ele.click()
            else:
                assert False, "fail to click the element"

    def click_execute_script(self, ele):
        # driver.execute_script("arguments[0].click();", ele)
        self.driver.execute_script("arguments[0].style.visibility = 'visible';", ele)
        ele.click()

    def text_element(self, text, xpath=None, ele=None):
        if ele is None:
            ele = self.driver.find_element_by_xpath(xpath)
        ele.send_keys(text)

    def find_element(self, xpath, ele=None):
        if ele is None:
            return self.driver.find_element_by_xpath(xpath)
        else:
            if xpath.startswith("//"):
                xpath = "." + str(xpath)
            return ele.find_element_by_xpath(xpath)

    def find_elements(self, xpath, ele=None):
        if ele is None:
            return self.driver.find_elements_by_xpath(xpath)
        else:
            if xpath.startswith("//"):
                xpath = "." + str(xpath)
            return ele.find_elements_by_xpath(xpath)

    def exist_element(self, xpath, ele=None):
        if ele is None:
            try:
                self.driver.find_element_by_xpath(xpath)
                return True
            except:
                return False
        else:
            try:
                if xpath.startswith("//"):
                    xpath = "." + str(xpath)
                ele.find_element_by_xpath(xpath)
                return True
            except:
                return False

    def move_to_element(self, xpath=None, ele=None):
        if ele is None:
            ele = self.find_element(xpath)
        ActionChains(self.driver).move_to_element(ele).perform()

    def move_and_click(self, xpath=None, ele=None):
        if ele is None:
            ele = self.find_element(xpath)
        ActionChains(self.driver).move_to_element(ele).click().perform()

    def move_by_offset(self, x, y):
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def log_message(self, message, debug=True):
        if debug:
            with open(self.logFile, 'a+') as outfile:
                outfile.write("{}: {}\n".format(strftime('%X %x'), message))

    def warning_message(self, item, debug=True):
        if debug:
            with open(self.logFile, 'a+') as outfile:
                outfile.write("{}: Warning: {} is not found.\n".format(strftime('%X %x'), item))


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
