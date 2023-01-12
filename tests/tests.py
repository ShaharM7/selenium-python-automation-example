import os

import pytest
from dotenv import load_dotenv

from drivers.awaiter import Awaiter
from drivers.chrome_browser import ChromeBrowser
from drivers.options.browser_options import BrowserOptions
from drivers.remote_browser import RemoteBrowser
from navigation.page_navigator import PageNavigator
from pages.github_home_page import GitHubHomePage
from pages.sign_in_page import SignInPage


@pytest.fixture
def set_up():
    load_dotenv('../.env')
    options = BrowserOptions()
    if os.getenv('REMOTEBROWSER_CONFIG_USE_SELENIUM_GRID') is True:
        browser = RemoteBrowser(options=options)
    else:
        browser = ChromeBrowser(options=options)
    awaiter = Awaiter(browser)

    sign_in_page = SignInPage(browser=browser,
                              awaiter=awaiter)

    github_home_page = GitHubHomePage(browser=browser,
                                      awaiter=awaiter,
                                      sign_in_page=sign_in_page)
    page_navigator = PageNavigator(browser=browser,
                                   github_home_page=github_home_page)

    return page_navigator


def test_github_home_page(set_up):
    home_page = set_up.navigate_to_home_page()
    sign_in_page = home_page.sign_in()
    sign_in_page.enter_user_name("None")
    sign_in_page.enter_password("None-again")
    sign_in_page.click_sign_in()