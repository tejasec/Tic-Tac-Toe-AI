import unittest
from logic import TicTacToeLogic, check_winner, PLAYER_X, PLAYER_O


class TestCheckWinner(unittest.TestCase):
    def test_horizontal_win_3x3(self):
        board = [
            PLAYER_X, PLAYER_X, PLAYER_X,
            None, PLAYER_O, None,
            PLAYER_O, None, None
        ]
        self.assertEqual(check_winner(board, 3, 3), PLAYER_X)

    def test_vertical_win_3x3(self):
        board = [
            PLAYER_O, PLAYER_X, None,
            PLAYER_O, PLAYER_X, None,
            PLAYER_O, None, PLAYER_X
        ]
        self.assertEqual(check_winner(board, 3, 3), PLAYER_O)

    def test_diagonal_win_3x3(self):
        board = [
            PLAYER_X, None, PLAYER_O,
            None, PLAYER_X, PLAYER_O,
            None, None, PLAYER_X
        ]
        self.assertEqual(check_winner(board, 3, 3), PLAYER_X)

    def test_antidiagonal_win_3x3(self):
        board = [
            None, None, PLAYER_O,
            PLAYER_X, PLAYER_O, None,
            PLAYER_O, PLAYER_X, None
        ]
        self.assertEqual(check_winner(board, 3, 3), PLAYER_O)

    def test_draw_3x3(self):
        board = [
            PLAYER_X, PLAYER_O, PLAYER_X,
            PLAYER_X, PLAYER_O, PLAYER_O,
            PLAYER_O, PLAYER_X, PLAYER_X
        ]
        self.assertEqual(check_winner(board, 3, 3), 'draw')

    def test_undecided_game(self):
        board = [
            PLAYER_X, PLAYER_O, None,
            None, None, None,
            None, None, None
        ]
        self.assertIsNone(check_winner(board, 3, 3))

    def test_custom_grid_4x4_win_length_3(self):
        # 4x4 grid with win_length 3
        board = [None] * 16
        board[0] = PLAYER_X
        board[1] = PLAYER_X
        board[2] = PLAYER_X
        self.assertEqual(check_winner(board, 4, 3), PLAYER_X)

    def test_custom_grid_2x2_win_length_2(self):
        board = [
            PLAYER_O, PLAYER_O,
            None, PLAYER_X
        ]
        self.assertEqual(check_winner(board, 2, 2), PLAYER_O)


class TestTicTacToeLogic(unittest.TestCase):
    def setUp(self):
        self.logic = TicTacToeLogic()

    def test_initial_state(self):
        self.logic.select_mode('pvp', grid_size=3, win_length=3)
        self.logic.start_game()
        self.assertTrue(self.logic.game_active)
        self.assertEqual(self.logic.current_player, PLAYER_X)
        self.assertEqual(len(self.logic.board), 9)
        self.assertTrue(all(c is None for c in self.logic.board))

    def test_pvp_turns_and_legality(self):
        self.logic.select_mode('pvp', grid_size=3, win_length=3)
        self.logic.start_game()

        # Valid move Player X
        res = self.logic.handle_cell_click(0)
        self.assertTrue(res)
        self.assertEqual(self.logic.board[0], PLAYER_X)
        self.assertEqual(self.logic.current_player, PLAYER_O)
        self.assertEqual(self.logic.last_sound, 'click')

        # Invalid move on occupied cell
        res_invalid = self.logic.handle_cell_click(0)
        self.assertFalse(res_invalid)
        self.assertEqual(self.logic.current_player, PLAYER_O)

        # Out of bounds click
        res_oob = self.logic.handle_cell_click(99)
        self.assertFalse(res_oob)

        # Valid move Player O
        res_o = self.logic.handle_cell_click(4)
        self.assertTrue(res_o)
        self.assertEqual(self.logic.board[4], PLAYER_O)
        self.assertEqual(self.logic.current_player, PLAYER_X)

    def test_pvp_win_and_scoring(self):
        self.logic.select_mode('pvp', grid_size=3, win_length=3)
        self.logic.start_game(reset_scores=True)

        # Round 1: X wins
        self.logic.handle_cell_click(0)  # X: 0
        self.logic.handle_cell_click(3)  # O: 3
        self.logic.handle_cell_click(1)  # X: 1
        self.logic.handle_cell_click(4)  # O: 4
        self.logic.handle_cell_click(2)  # X: 2 -> horizontal win for X!

        self.assertFalse(self.logic.game_active)
        self.assertEqual(self.logic.last_winner, PLAYER_X)
        self.assertEqual(self.logic.pvp_score_x, 1)
        self.assertEqual(self.logic.pvp_score_o, 0)
        self.assertEqual(self.logic.last_sound, 'win')

        # Round 2: starting new game without score reset keeps scores
        self.logic.start_game(reset_scores=False)
        self.assertTrue(self.logic.game_active)
        self.assertEqual(self.logic.pvp_score_x, 1)

    def test_reset_scores(self):
        self.logic.pvp_score_x = 5
        self.logic.pvp_score_o = 3
        self.logic.pvp_ties = 2
        self.logic.reset_scores('pvp')
        self.assertEqual(self.logic.pvp_score_x, 0)
        self.assertEqual(self.logic.pvp_score_o, 0)
        self.assertEqual(self.logic.pvp_ties, 0)

    def test_status_text(self):
        self.logic.select_mode('pvp', grid_size=3, win_length=3)
        self.logic.start_game()
        self.assertEqual(self.logic.get_status_text(), "Player X's Turn")

        self.logic.handle_cell_click(0)
        self.assertEqual(self.logic.get_status_text(), "Player O's Turn")

        self.logic.end_game(PLAYER_X)
        self.assertEqual(self.logic.get_status_text(), "Player X Wins!")

    def test_to_dict_schema(self):
        self.logic.select_mode('pvp', grid_size=3, win_length=3)
        self.logic.start_game()
        d = self.logic.to_dict()
        expected_keys = {
            'board', 'game_active', 'current_player', 'game_mode',
            'difficulty', 'grid_size', 'win_length', 'winner',
            'legal_moves', 'status_text', 'sound', 'pvp_score_x',
            'pvp_score_o', 'pvp_ties', 'pva_score_x', 'pva_score_o',
            'pva_ties'
        }
        self.assertTrue(expected_keys.issubset(d.keys()))


if __name__ == '__main__':
    unittest.main()
