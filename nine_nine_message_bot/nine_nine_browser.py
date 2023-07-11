from datetime import datetime, time
from functools import cache
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nine_nine_message_bot.driver import click, create_driver, find_element, find_elements
from nine_nine_message_bot.domain import Message, Project
from nine_nine_message_bot.exceptions import (
    LoginError,
    ProjectError,
    SendMessageError,
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

    @cache
    def get_account_name(self) -> str:
        self.driver.get('https://www.99freelas.com.br/dashboard')
        return find_element(self.driver, '.user-name').text

    def open_inbox(self) -> None:
        self.driver.get('https://www.99freelas.com.br/messages/inbox')
        messages_number = len(find_elements(self.driver, 'li.conversa-item'))
        while True:
            click(self.driver, 'div.content-load-more.content-loaded')
            sleep(3)
            if messages_number == len(find_elements(self.driver, 'li.conversa-item')):
                break
            messages_number = len(find_elements(self.driver, 'li.conversa-item'))

    def get_projects_urls_from_inbox(self) -> None:
        result = []
        for conversation in find_elements(self.driver, 'li.conversa-item'):
            self.driver.execute_script('arguments[0].click();', conversation)
            result.append(
                find_element(
                    self.driver,
                    '.clone a.nome-projeto',
                ).get_attribute('href')
            )
        return result

    def send_message_from_inbox(self, message: str, index: int) -> None:
        conversation = find_elements(self.driver, 'li.conversa-item')[index]
        self.driver.execute_script('arguments[0].click();', conversation)
        breakpoint()
        find_elements(
            self.driver,
            'textarea.send-message-textarea',
        )[1].send_keys(
            message + Keys.RETURN
        )

    def get_project(self, url: str) -> Project:
        self.driver.get(url)
        try:
            return Project(
                client_name=find_element(
                    self.driver, '.info-usuario-nome .name'
                ).text,
                name=find_element(self.driver, '.nomeProjeto').text,
                category=find_element(self.driver, 'td').text,
                url=url,
            )
        except TimeoutException:
            if self.driver.find_elements(By.CSS_SELECTOR, '.fail'):
                raise ProjectError('O projeto não existe')
            raise ProjectError(
                'Projeto ainda não está disponivel para mandar mensagens'
            )

    def send_message(self, project_url: str, message: str) -> Message:
        project = self.get_project(project_url)
        message = self.format_message(message, project),
        self.driver.get(project_url)
        self.driver.get(
            find_element(self.driver, '.txt-duvidas a').get_attribute('href')
        )
        try:
            find_element(self.driver, '#mensagem-pergunta').send_keys(message)
        except TimeoutException:
            raise SendMessageError(
                'Projeto não disponivel para envio de mensagens'
            )
        click(self.driver, '#btnEnviarPergunta')
        return Message(project=project, text=message)

    def format_message(self, message: str, project: Project) -> str:
        greeting = get_greeting_according_time(datetime.now().time())
        message = message.replace('{saudação}', greeting)
        message = message.replace('{nome do cliente}', project.client_name)
        #message = message.replace('{nome do projeto}', project.name)
        #message = message.replace('{categoria}', project.category)
        #message = message.replace('{nome da conta}', self.get_account_name())
        return message
