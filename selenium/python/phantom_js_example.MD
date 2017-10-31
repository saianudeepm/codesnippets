##Install Selenium with Pip and PhantomJS with Brew:
```
$ pip install selenium
$ brew install phantomjs
$ brew install geckodriver
```
##Open a page and print the page url

```
from selenium import webdriver
driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get("https://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()
```

[Reference](https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/)
