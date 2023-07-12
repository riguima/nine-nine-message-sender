
from nine_nine_message_bot.nine_nine_browser import NineNineBrowser


if __name__ == '__main__':
    browser = NineNineBrowser()
    browser.make_login('craybrasil@gmail.com', 'Projeto#1bot')
    browser.open_inbox()
    message = (
        '{saudação}, tudo bem?. '
        'Estamos com esse produto atualmente {b}"pacotedeautomacoes.site"'
        '{/b} caso você possua interesse. Podemos enviar os acessos '
        'através da plataforma {b}99freelas{/b}. Consiste em um pacote com '
        '9 automações para serem utilizados em divulgação, captação ou '
        'comercialização. - {b}pacotedeautomacoes.site{/b}'
    )
    browser.send_message_from_inbox(message)
