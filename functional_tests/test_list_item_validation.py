import os
import time
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from .base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # the home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You can't have an empty list item",
            )
        )

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_id("id_new_item").send_keys("Buy milk")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: Buy milk")

        # Preversely, she now decides to submit a second blank list time
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # She receives a simlar warning on the list page
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You can't have an empty list item",
            )
        )

        # And she can correct it by filling some text in
        self.browser.find_elements_by_id("id_new_item").send_keys("Make tea")
        self.browser.find_elements_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: Buy milk")
        self.wait_for_now_in_list_table("2: Make tea")