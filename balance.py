import json
import time

from flask import Flask, render_template, request
from flask_cors import CORS

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException

app = Flask(__name__)
CORS(app)


def load_browser() -> WebDriver:
    opt = Options()
    opt.headless = True

    browser = Firefox(executable_path='./geckodriver', options=opt)

    return browser


def get_balance(browser: WebDriver, url: str, card_number: str) -> str:
    input_field_id = 'ean'
    balance_field_class = 'history_header_amount'

    browser.get(url)
    time.sleep(0.5)

    num_form = WebDriverWait(browser, 5).until(
        expected_conditions.presence_of_element_located(
            (By.ID, input_field_id)
        )
    )

    num_form.send_keys(card_number)
    num_form.submit()

    try:
        balance_field = WebDriverWait(browser, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, balance_field_class)
            )
        )

        balance = balance_field.text
    except TimeoutException:
        error = browser.find_element_by_class_name(
            'form-messages_message__error'
        )

        errors = [
            'Проверьте корректность введенных данных',
            'Введите корректный номер штрих-кода карты',
        ]

        if error.text in errors:
            balance = 'Карта не найдена'
        else:
            balance = error.text
    finally:
        browser.close()

    return balance


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/balance/')
def balance_page():
    return render_template('balance.html')


@app.route('/query/')
def query_balance():
    card_number = request.args.get('card_number').replace(' ', '')
    url = 'https://restaurantpass.gift-cards.ru/balance'

    browser = load_browser()

    try:
        balance = get_balance(browser, url, card_number)
    except NoSuchElementException:
        balance = 'Карта не найдена'

    card_number_spaced = ' '.join([
        card_number[0],
        card_number[1:7],
        card_number[7:],
    ])

    return json.dumps({
        'card_balance': balance,
        'card_number': card_number_spaced,
    })


if __name__ == '__main__':
    app.run()
