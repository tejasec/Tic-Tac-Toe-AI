import unittest
from logic import (
    TicTacToeLogic, get_easy_move, get_medium_move,
    find_best_move_ai, get_ai_move, PLAYER_X, PLAYER_O
)


class TestAIEngine(unittest.TestCase):
    def test_easy_move_returns_valid_cell(self):
        board = [PLAYER_X, None, PLAYER_O, None, None, None, None, None, None]
        move = get_easy_move(board)
        self.assertIn(move, [1, 3, 4, 5, 6, 7, 8])

    def test_easy_move_full_board(self):
        board = [PLAYER_X] * 9
        self.assertIsNone(get_easy_move(board))

    def test_medium_ai_takes_winning_move(self):
        # O has 0 and 1, cell 2 completes the win for O
        board = [
            PLAYER_O, PLAYER_O, None,
            PLAYER_X, PLAYER_X, None,
            None, None, None
        ]
        move = get_medium_move(board)
        self.assertEqual(move, 2)

    def test_medium_ai_blocks_opponent_win(self):
        # X has 0 and 1, AI must block at 2
        board = [
            PLAYER_X, PLAYER_X, None,
            PLAYER_O, None, None,
            None, None, None
        ]
        move = get_medium_move(board)
        self.assertEqual(move, 2)

    def test_unbeatable_ai_takes_immediate_win(self):
        # O can win immediately at index 2
        board = [
            PLAYER_O, PLAYER_O, None,
            PLAYER_X, PLAYER_X, None,
            None, None, None
        ]
        move = find_best_move_ai(board)
        self.assertEqual(move, 2)

    def test_unbeatable_ai_blocks_opponent_fork(self):
        # X starts center and corner: [X, None, None, None, X, None, None, None, None]
        board = [
            PLAYER_X, None, None,
            None, PLAYER_O, None,
            None, None, PLAYER_X
        ]
        # Any edge move blocks diagonal fork
        move = find_best_move_ai(board)
        self.assertIn(move, [1, 3, 5, 7])

    def test_pva_full_turn_integration(self):
        logic = TicTacToeLogic()
        logic.select_mode('pva', difficulty='easy', grid_size=3, win_length=3)
        logic.start_game(reset_scores=True)

        # Player moves at cell 4 (center)
        result = logic.handle_cell_click(4)
        self.assertTrue(result)
        self.assertEqual(logic.board[4], PLAYER_X)

        # AI should have made a move immediately
        o_count = sum(1 for c in logic.board if c == PLAYER_O)
        self.assertEqual(o_count, 1)

        # Turn should be back to Player X
        self.assertEqual(logic.current_player, PLAYER_X)


if __name__ == '__main__':
    unittest.main()
