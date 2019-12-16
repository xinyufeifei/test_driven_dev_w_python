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

        # the home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item, which now works

        # Preversely, she now decides to submit a second blank list time

        # She receives a simlar warning on the list page

        # And she can correct it by filling some text in
        self.fail("write me!")
