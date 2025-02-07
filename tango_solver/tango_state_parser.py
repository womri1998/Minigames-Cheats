from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def init_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(
        service=Service(),
        options=chrome_options
    )
    driver.get("https://www.linkedin.com/games/tango")
    return driver


def get_cells_representations(driver: WebDriver) -> list[tuple[str, bool, bool]]:
    lotka_cells = driver.find_elements(By.CLASS_NAME, 'lotka-cell')
    raw_game = []
    for idx, cell in enumerate(lotka_cells):
        svg_element = cell.find_element(By.TAG_NAME, 'svg')
        aria_label = svg_element.get_attribute('aria-label')
        try:
            cell.find_element(By.CLASS_NAME, 'lotka-cell-edge--down')
            has_edge_down = True
        except:
            has_edge_down = False
        try:
            cell.find_element(By.CLASS_NAME, 'lotka-cell-edge--right')
            has_edge_right = True
        except:
            has_edge_right = False
        raw_game.append((aria_label, has_edge_down, has_edge_right))
    return raw_game