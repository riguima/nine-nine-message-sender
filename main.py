import pandas as pd

from nine_nine_message_bot.nine_nine_browser import NineNineBrowser


if __name__ == '__main__':
    browser = NineNineBrowser()
    #browser.make_login('craybrasil@gmail.com', 'Projeto#1bot')
    browser.open_inbox()
    projects = [
        browser.get_project(url)
        for url in browser.get_projects_urls_from_inbox()
    ]
    browser.open_inbox()
    for e, project in enumerate(projects):
        if project.client_name not in ['William G.', 'Wanderley S.']:
            message = (
                '{saudação} {b}{nome do cliente}{/b}, tudo bem? \n'
                'Estamos com esse produto atualmente {b}"pacotedeautomacoes.site"'
                '{/b} caso você possua interesse. Podemos enviar os acessos '
                'através da plataforma {b}99freelas{/b}. Consiste em um pacote com'
                '9 automações para serem utilizados em divulgação, captação ou '
                'comercialização. - {b}pacotedeautomacoes.site{/b}'
            )
            message = browser.format_message(message, project)
            browser.send_message_from_inbox(message, e)
