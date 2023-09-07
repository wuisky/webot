#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from typing import Any, Callable, Tuple


class Webot:
    """
    A wrapping class of selenium lib which offers easy API for controlling webbrowser.
    """

    def __init__(self, url: str, headless: bool) -> None:
        options = Options()
        # userdata_dir = 'UserData'
        # options.add_argument('--user-data-dir=' + userdata_dir)
        if headless:
            options.add_argument('--headless')
        ua = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'
        options.add_argument('--user-agent=' + ua)
        # options.add_argument('--user-agent=hogehoge')
        options.add_argument('--no-proxy-server')
        self.driver = webdriver.Chrome(options=options)
        self.top_url = url
        self.driver.get(url)
        print(f'page title: {self.driver.title}')

    def try_cmd(self, cmd: Callable, arg: str = '') -> Tuple[bool, Any]:
        try:
            ret = cmd(arg)
            return True, ret
        except:
            return False, None

    def wait_page(self, current_url: str, timeout: int = 15) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_changes(current_url))
            return True
        except:  # pylint: disable=W0702
            print('timeout. stay in same page')
            return False

    def wait_ack(self, cmd: Callable, timeout: int) -> bool:
        current_url = self.driver.current_url
        cmd()
        return self.wait_page(current_url, timeout)

    def wait_id(self, element_id: str, timeout: int) -> None:
        WebDriverWait(self.driver,
                      timeout).until(EC.presence_of_element_located((By.ID, element_id)))

    def wait_hidden(self, element: WebElement, timeout: int) -> None:
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(element))

    def wait_show(self, element: WebElement, timeout: int) -> None:
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))

    def back_to_top(self) -> None:
        self.driver.get(self.top_url)

    def move_to_element(self, element: WebElement) -> None:
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def tear_down(self) -> None:
        self.driver.quit()

    def select_element_wrapper(self, element: WebElement) -> Select:
        return Select(element)
