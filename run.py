from parsers.octordle_parser import get_current_soup, get_game_board
from word_fetchers.english_fetcher import EnglishFetcher
from wordle_solver import WordleSolver


def main():
    game_board = get_game_board(get_current_soup())
    all_words = EnglishFetcher(5).get_filtered_words()
    solver = WordleSolver(all_words)
    for i, board in enumerate(game_board.boards):
        print(i)
        board.print()
        print(solver.possible_guesses(board))


if __name__ == "__main__":
    main()
