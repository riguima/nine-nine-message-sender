from datetime import datetime, time
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nine_nine_message_bot.driver import click, create_driver, find_element, find_elements
from nine_nine_message_bot.exceptions import (
    LoginError,
)


def get_greeting_according_time(greeting_time: time) -> str:
    if time(0, 0, 0) <= greeting_time <= time(11, 59, 59):
        return 'Bom dia'
    elif time(12, 0, 0) <= greeting_time <= time(18, 59, 59):
        return 'Boa tarde'
    elif time(19, 0, 0) <= greeting_time <= time(23, 59, 59):
        return 'Boa noite'


class NineNineBrowser():
    def __init__(self) -> None:
        self.driver = create_driver()

    def make_login(self, username: str, password: str) -> None:
        self.driver.get('https://www.99freelas.com.br/login')
        find_element(self.driver, '#email').send_keys(username)
        find_element(self.driver, '#senha').send_keys(password)
        while True:
            if not self.is_logged():
                errors_messages = self.driver.find_elements(
                    By.CSS_SELECTOR, '.general-error-msg'
                )
                if errors_messages and errors_messages[0].get_attribute(
                    'style'
                ):
                    raise LoginError('Email ou senha inválidos')
            else:
                break

    def is_logged(self) -> bool:
        url = 'https://www.99freelas.com.br/login'
        if self.driver.current_url != url:
            self.driver.get(url)
        try:
            find_element(self.driver, '.user-name')
        except TimeoutException:
            return False
        return True

    def open_inbox(self) -> None:
        self.driver.get('https://www.99freelas.com.br/messages/inbox')
        messages_number = len(find_elements(self.driver, 'li.conversa-item'))
        while True:
            click(self.driver, 'div.content-load-more.content-loaded')
            sleep(3)
            if messages_number == len(find_elements(self.driver, 'li.conversa-item')):
                break
            messages_number = len(find_elements(self.driver, 'li.conversa-item'))

    def send_message_from_inbox(self, message: str) -> None:
        for e in range(len(find_elements(self.driver, 'li.conversa-item'))):
            conversations = find_elements(self.driver, 'li.conversa-item')
            self.driver.execute_script('arguments[0].click();', conversations[e + 222])
            greeting = get_greeting_according_time(datetime.now().time())
            message = message.replace('{saudação}', greeting)
            textarea = find_elements(self.driver, 'textarea.send-message-textarea')[1]
            self.driver.execute_script('arguments[0].click();', textarea)
            textarea.send_keys(message)
            textarea.send_keys(Keys.RETURN)
