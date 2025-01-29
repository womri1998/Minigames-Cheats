from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from parsers.game_state import Cell, Row, Board, GameBoard


def get_cell_color(cell):
    if cell['aria-label'].endswith('is correct'):
        return 'green'
    elif cell['aria-label'].endswith('is in a different spot'):
        return 'yellow'
    elif cell['aria-label'].endswith('is incorrect'):
        return 'gray'
    raise ValueError("What color is this?")


def get_current_soup() -> BeautifulSoup:
    chrome_options = webdriver.ChromeOptions()  # Connect to the already open Chrome browser
    chrome_options.debugger_address = "127.0.0.1:9222"  # Connect to the debugging port
    driver = webdriver.Chrome(
        service=Service(),
        options=chrome_options  # Start Selenium WebDriver without launching a new browser
    )
    html = driver.page_source
    return BeautifulSoup(html, "html.parser")


def get_game_board(octordle_html: BeautifulSoup) -> GameBoard:
    boards = []
    board_elements = octordle_html.find_all("div", attrs={"class": "board"})
    for board_element in board_elements:
        rows = []
        row_elements = [
            row for row in board_element.find_all("div", attrs={"class": "board-row"})
            if "Guess" in row['aria-label'] and "Guess ." not in row['aria-label']
        ]
        for row_element in row_elements:
            cell_elements = row_element.find_all("div", attrs={"role": "cell"})
            cells = [
                Cell(
                    letter=cell['aria-label'][1],
                    color=get_cell_color(cell)
                ) for cell in cell_elements
            ]
            rows.append(Row(cells=cells))
        boards.append(Board(rows=rows))
    return GameBoard(boards=boards)
