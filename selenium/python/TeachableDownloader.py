## Unfinished but prints out the links of the course lessons along with section name

import time
import os

import csv
from selenium import webdriver
import selenium.webdriver.support.ui as ui

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

login_user_xpath = '//*[@id="user_email"]'
login_password_xpath = '//*[@id="user_password"]'
login_submit_xpath = '//*[@id="new_user"]/div[3]/input'
username = 'XXXXXX'
password = 'XXXXXX'
sections_xpath = '//*[@class="col-sm-12 course-section"]'
video_script_details_xpath = '/html/head/script[13]'
pdf_download_xpath = '//*[@class="download"]'
processed_lesson = {}


class Section():
    def __init__(self, name, lessons):
        self.name = name
        self.lessons = lessons


class Lesson():
    def __init__(self, name, link):
        self.name = name
        self.link = link


# process by section
def process_lesson(section_name, lesson):
    try:
        lesson_name = lesson.name
        lesson_link = lesson.link
        if lesson_name in processed_lesson:
            return
        # print "processing lesson %s" % lesson_name
        driver.get(lesson_link)
        time.sleep(2)
        wait.until(lambda driver: driver.find_element_by_xpath(video_script_details_xpath))
        lesson_text = driver.find_element_by_xpath(video_script_details_xpath).get_attribute("innerHTML")
        print "%s|%s|%s|%s" % (section_name, lesson_name, lesson_link, lesson_text)
        processed_lesson[lesson_name] = True
    except Exception as E1:
        try:
            wait.until(lambda driver: driver.find_element_by_xpath(pdf_download_xpath))
            lesson_text = driver.find_element_by_xpath(pdf_download_xpath).get_attribute("href")
            print "%s|%s|%s|%s" % (section_name, lesson.name, lesson.link, lesson_text)
            processed_lesson[lesson_name] = True
        except Exception as E2:
            print E2
            print "failed for %s|%s|%s" % (section_name, lesson.name, lesson.link)


def process_section(section):
    # print "processing section %s" % section.name
    lessons = section.lessons
    for lesson_index in range(len(lessons)):
        lesson = lessons[lesson_index]
        process_lesson(section.name, lesson)


def login():
    wait.until(lambda driver: driver.find_element_by_xpath(login_user_xpath))
    wait.until(lambda driver: driver.find_element_by_xpath(login_password_xpath))
    driver.find_element_by_xpath(login_user_xpath).send_keys(username)
    driver.find_element_by_xpath(login_password_xpath).send_keys(password)
    driver.find_element_by_xpath(login_submit_xpath).submit()
    time.sleep(5)


driver = webdriver.Firefox(firefox_profile=fp)
driver.set_window_size(1120, 550)
driver.get("https://sso.teachable.com/secure/77566/users/sign_in")
wait = ui.WebDriverWait(driver, 10)

# Login
login()


def main():
    try:
        wait.until(lambda driver: driver.find_element_by_xpath(sections_xpath))
        section_elements = driver.find_elements_by_xpath(sections_xpath)
        sections = []
        for index in range(len(section_elements)):
            section_element = section_elements[index]
            section_name = section_element.find_element_by_class_name('section-title').text.strip()
            section_item_elements = section_element.find_elements_by_class_name('section-item')
            lessons = []
            for item in range(len(section_item_elements)):
                section_item_element = section_item_elements[item].find_element_by_tag_name('a')
                lesson_link = section_item_element.get_attribute('href')
                lesson_name = section_item_element.find_element_by_class_name('title-container').text.strip()
                lesson = Lesson(lesson_name, lesson_link)
                lessons.append(lesson)
            sections.append(Section(section_name, lessons))

        for section in sections[2:]:
            process_section(section)

    except Exception as ex:
        driver.quit()
        print ex.message
        print processed_lesson


main()
