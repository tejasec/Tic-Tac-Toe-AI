import math
import random
import json
import os
import sys
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

PLAYER_X = 'X'
PLAYER_O = 'O'

WIN_COMBINATIONS_3X3 = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


def check_winner(board, grid_size, win_length):
    """Check for a winner or draw on an arbitrary grid_size x grid_size board.

    Returns:
        'X' or 'O' if a player has reached win_length in a line,
        'draw' if the board is full with no winner,
        None if the game is still undecided.
    """
    def get(r, c):
        return board[r * grid_size + c]

    for r in range(grid_size):
        for c in range(grid_size):
            player = get(r, c)
            if player is None:
                continue

            # Check horizontal
            if c + win_length <= grid_size:
                if all(get(r, c + i) == player for i in range(1, win_length)):
                    return player

            # Check vertical
            if r + win_length <= grid_size:
                if all(get(r + i, c) == player for i in range(1, win_length)):
                    return player

            # Check diagonal right-down
            if c + win_length <= grid_size and r + win_length <= grid_size:
                if all(get(r + i, c + i) == player for i in range(1, win_length)):
                    return player

            # Check diagonal left-down
            if c - win_length + 1 >= 0 and r + win_length <= grid_size:
                if all(get(r + i, c - i) == player for i in range(1, win_length)):
                    return player

    if None not in board:
        return 'draw'

    return None


def get_easy_move(current_board):
    """Easy AI: randomly select any unoccupied cell."""
    available_moves = [i for i, val in enumerate(current_board) if val is None]
    if not available_moves:
        return None
    return random.choice(available_moves)


def check_winner_3x3_for_score(board):
    """Fast evaluation of standard 3x3 board for minimax scoring."""
    for combo in WIN_COMBINATIONS_3X3:
        a, b, c = combo
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return 10 if board[a] == PLAYER_O else -10

    if None not in board[:9]:
        return 0
    return None


def get_medium_move(current_board):
    """Medium AI: win if possible, block opponent if threatened, else random."""
    for i in range(9):
        if current_board[i] is None:
            current_board[i] = PLAYER_O
            if check_winner_3x3_for_score(current_board) == 10:
                current_board[i] = None
                return i
            current_board[i] = None

    for i in range(9):
        if current_board[i] is None:
            current_board[i] = PLAYER_X
            if check_winner_3x3_for_score(current_board) == -10:
                current_board[i] = None
                return i
            current_board[i] = None

    return get_easy_move(current_board)


def minimax_ai(current_board, depth, is_maximizing, alpha, beta, max_depth):
    """Minimax search with alpha-beta pruning."""
    score = check_winner_3x3_for_score(current_board)
    if score is not None:
        return score
    if depth == max_depth:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if current_board[i] is None:
                current_board[i] = PLAYER_O
                current_score = minimax_ai(current_board, depth + 1, False, alpha, beta, max_depth)
                current_board[i] = None
                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if current_board[i] is None:
                current_board[i] = PLAYER_X
                current_score = minimax_ai(current_board, depth + 1, True, alpha, beta, max_depth)
                current_board[i] = None
                best_score = min(best_score, current_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score


def find_best_move_ai(current_board, max_depth=float('inf')):
    """Evaluate all top-level moves with minimax and pick the highest score."""
    best_score = -math.inf
    move = None
    for i in range(9):
        if current_board[i] is None:
            current_board[i] = PLAYER_O
            score = minimax_ai(current_board, 0, False, -math.inf, math.inf, max_depth)
            current_board[i] = None
            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        return move
    return get_easy_move(current_board)


def get_ai_move(current_board, grid_size, difficulty):
    """Delegate to appropriate difficulty AI algorithm."""
    if grid_size != 3:
        return get_easy_move(current_board)

    if difficulty == 'easy':
        return get_easy_move(current_board)
    elif difficulty == 'medium':
        return get_medium_move(current_board)
    elif difficulty == 'hard':
        return find_best_move_ai(current_board, 4)
    elif difficulty == 'unbeatable':
        return find_best_move_ai(current_board)
    else:
        return get_easy_move(current_board)


class TicTacToeLogic:
    """Definitive engine for Tic-Tac-Toe game state, rules, moves, and scoring."""

    def __init__(self):
        self.board = []
        self.game_active = False
        self.game_mode = 'pvp'
        self.current_player = PLAYER_X
        self.difficulty = None
        self.grid_size = 3
        self.win_length = 3
        self.last_winner = None
        self.last_sound = None

        self.pvp_score_x = 0
        self.pvp_score_o = 0
        self.pvp_ties = 0

        self.pva_score_x = 0
        self.pva_score_o = 0
        self.pva_ties = 0

    def select_mode(self, mode, difficulty=None, grid_size=3, win_length=3):
        """Configure game mode parameters."""
        self.game_mode = mode
        self.difficulty = difficulty
        self.grid_size = int(grid_size)
        self.win_length = int(win_length)

    def reset_scores(self, mode=None):
        """Reset scores for a specific mode or all modes."""
        if mode == 'pvp' or mode is None:
            self.pvp_score_x = 0
            self.pvp_score_o = 0
            self.pvp_ties = 0
        if mode == 'pva' or mode is None:
            self.pva_score_x = 0
            self.pva_score_o = 0
            self.pva_ties = 0

    def start_game(self, reset_scores=False):
        """Initialize a fresh board and start the match."""
        if reset_scores:
            self.reset_scores(self.game_mode)

        self.board = [None] * (self.grid_size * self.grid_size)
        self.game_active = True
        self.current_player = PLAYER_X
        self.last_winner = None
        self.last_sound = None

    def make_move(self, index, player):
        """Place player mark if index is legal and empty."""
        if 0 <= index < len(self.board) and self.board[index] is None:
            self.board[index] = player
            return True
        return False

    def handle_cell_click(self, index):
        """Process a move request. Python validates and executes all moves."""
        if not self.game_active or index < 0 or index >= len(self.board) or self.board[index] is not None:
            self.last_sound = None
            return False

        if self.game_mode == 'pvp' or (self.game_mode == 'pva' and self.current_player == PLAYER_X):
            if self.make_move(index, self.current_player):
                if self.check_game_over():
                    return True

                if self.game_mode == 'pvp':
                    self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
                    self.last_sound = 'click'
                    return True
                else:
                    self.current_player = PLAYER_O
                    self.ai_move()
                    return True

        self.last_sound = None
        return False

    def ai_move(self):
        """Execute AI turn in PvA mode."""
        move_index = get_ai_move(self.board, self.grid_size, self.difficulty)
        if move_index is not None:
            self.make_move(move_index, PLAYER_O)

        if self.check_game_over():
            return

        self.current_player = PLAYER_X
        self.game_active = True
        self.last_sound = 'click'

    def check_game_over(self):
        """Check for terminal state (win or draw) and update scores."""
        winner = check_winner(self.board, self.grid_size, self.win_length)
        if winner:
            self.end_game(winner)
            return True
        return False

    def end_game(self, result):
        """Conclude game, record scores, and assign terminal sound."""
        self.game_active = False
        self.last_winner = result
        if result == 'draw':
            self.last_sound = 'draw'
            if self.game_mode == 'pvp':
                self.pvp_ties += 1
            else:
                self.pva_ties += 1
        else:
            self.last_sound = 'win'
            if self.game_mode == 'pvp':
                if result == PLAYER_X:
                    self.pvp_score_x += 1
                else:
                    self.pvp_score_o += 1
            else:
                if result == PLAYER_X:
                    self.pva_score_x += 1
                else:
                    self.pva_score_o += 1

    def get_status_text(self):
        """Authoritative human-readable status message for the view."""
        if not self.game_active:
            if self.last_winner == 'draw':
                return "It's a tie!"
            elif self.last_winner == PLAYER_O and self.game_mode == 'pva':
                return "AI Wins!"
            elif self.last_winner:
                return f"Player {self.last_winner} Wins!"
            return ""

        if self.game_mode == 'pva':
            if self.current_player == PLAYER_X:
                return "Your Turn"
            return "AI is thinking..."

        return f"Player {self.current_player}'s Turn"

    def to_dict(self):
        """Serialize state for /api/action JSON response."""
        return {
            'board': self.board,
            'game_active': self.game_active,
            'current_player': self.current_player,
            'game_mode': self.game_mode,
            'difficulty': self.difficulty,
            'grid_size': self.grid_size,
            'win_length': self.win_length,
            'winner': self.last_winner if not self.game_active else None,
            'legal_moves': [i for i, v in enumerate(self.board) if v is None] if self.game_active else [],
            'status_text': self.get_status_text(),
            'sound': self.last_sound,
            'pvp_score_x': self.pvp_score_x,
            'pvp_score_o': self.pvp_score_o,
            'pvp_ties': self.pvp_ties,
            'pva_score_x': self.pva_score_x,
            'pva_score_o': self.pva_score_o,
            'pva_ties': self.pva_ties
        }


game = TicTacToeLogic()


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler serving static assets and the /api/action endpoint."""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.serve_static('index.html', 'text/html; charset=utf-8')
        elif self.path == '/style.css':
            self.serve_static('style.css', 'text/css; charset=utf-8')
        elif self.path.startswith('/sounds/'):
            sound_path = self.path.lstrip('/')
            content_type, _ = mimetypes.guess_type(sound_path)
            if content_type is None:
                content_type = 'audio/wav'
            self.serve_static(sound_path, content_type)
        else:
            self.send_response(404)
            self.end_headers()

    def serve_static(self, relative_path, content_type):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, relative_path)
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/action':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = {}

            action = data.get('action')

            if action == 'start':
                mode = data.get('mode', game.game_mode or 'pvp')
                difficulty = data.get('difficulty', game.difficulty)
                size = int(data.get('size', game.grid_size or 3))
                length = int(data.get('length', game.win_length or 3))
                reset_scores = bool(data.get('reset_scores', False))

                game.select_mode(mode, difficulty, size, length)
                game.start_game(reset_scores=reset_scores)

            elif action == 'restart':
                game.start_game(reset_scores=False)

            elif action == 'click':
                index = data.get('index')
                if index is not None:
                    game.handle_cell_click(int(index))

            elif action == 'reset_scores':
                game.reset_scores(data.get('mode'))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game.to_dict()).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=None):
    """Run server on port 8000 (or PORT env/arg), falling back gracefully if port 8000 is occupied."""
    if port is None:
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            port = int(os.environ.get('PORT', 8000))

    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError as e:
        if e.errno == 98 and port == 8000:
            port = 8080
            server_address = ('', port)
            httpd = HTTPServer(server_address, RequestHandler)
            print(f"Port 8000 was in use. Falling back to port {port}.")
        else:
            raise

    print(f"Serving Tic-Tac-Toe locally at http://localhost:{port}")
    print("Press Ctrl+C to quit.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run_server()
