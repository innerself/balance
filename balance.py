import time

from flask import Flask, render_template

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)


def load_browser() -> WebDriver:
    opt = Options()
    opt.headless = True

    browser = Chrome(executable_path='./chromedriver', options=opt)

    return browser


def get_balance(browser: WebDriver, url: str, card_number: str) -> str:
    input_field_id = 'ean'
    balance_field_class = 'history_header_amount'

    browser.get(url)

    num_form = browser.find_element_by_id(input_field_id)
    time.sleep(1)
    num_form.send_keys(card_number)
    num_form.submit()

    time.sleep(1)

    result = browser.find_element_by_class_name(balance_field_class)
    balance = result.text

    browser.close()

    return balance


@app.route('/<string:card_number>')
def index(card_number: str):
    url = 'https://restaurantpass.gift-cards.ru/balance'

    browser = load_browser()

    try:
        balance = get_balance(browser, url, card_number)
    except NoSuchElementException:
        balance = 'NoSuchElementException'

    card_number_spaced = ' '.join([
        card_number[0],
        card_number[1:7],
        card_number[7:],
    ])

    # balance = '2 547.78 ₽'

    return render_template(
        'index.html',
        card_number=card_number_spaced,
        card_balance=balance,
    )
