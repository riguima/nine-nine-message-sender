from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_driver() -> Chrome:
    options = Options()
    options.add_argument('user-data-dir=default')
    return Chrome(
        options=options,
        service=Service(ChromeDriverManager().install())
    )


def click(driver: Chrome, selector: str, element=None) -> None:
    if element is None:
        element = driver
    driver.execute_script(
        'arguments[0].click();',
        find_element(element, selector),
    )


def find_element(element, selector: str, wait: int = 10):
    return WebDriverWait(element, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(element, selector: str, wait: int = 10):
    return WebDriverWait(element, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
