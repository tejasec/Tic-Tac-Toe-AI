import math
import random
import json
import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

PLAYER_X = 'X'
PLAYER_O = 'O'

def check_winner(board, grid_size, win_length):
    def get(r, c):
        return board[r * grid_size + c]

    for r in range(grid_size):
        for c in range(grid_size):
            player = get(r, c)
            if player is None:
                continue
            
            # Check horizontal
            if c + win_length <= grid_size:
                w = True
                for i in range(1, win_length):
                    if get(r, c + i) != player:
                        w = False
                        break
                if w:
                    return player
            
            # Check vertical
            if r + win_length <= grid_size:
                w = True
                for i in range(1, win_length):
                    if get(r + i, c) != player:
                        w = False
                        break
                if w:
                    return player
            
            # Check diagonal right-down
            if c + win_length <= grid_size and r + win_length <= grid_size:
                w = True
                for i in range(1, win_length):
                    if get(r + i, c + i) != player:
                        w = False
                        break
                if w:
                    return player
            
            # Check diagonal left-down
            if c - win_length + 1 >= 0 and r + win_length <= grid_size:
                w = True
                for i in range(1, win_length):
                    if get(r + i, c - i) != player:
                        w = False
                        break
                if w:
                    return player

    if None not in board:
        return 'draw'
    
    return None

def get_easy_move(current_board):
    available_moves = [i for i, val in enumerate(current_board) if val is None]
    if not available_moves:
        return None
    return random.choice(available_moves)

WIN_COMBINATIONS_3X3 = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner_3x3_for_score(board):
    for combo in WIN_COMBINATIONS_3X3:
        a, b, c = combo
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return 10 if board[a] == PLAYER_O else -10
            
    if None not in board[:9]:
        return 0
    return None

def get_medium_move(current_board):
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
    def __init__(self):
        self.board = []
        self.game_active = False
        self.game_mode = None
        self.current_player = None
        self.difficulty = None
        self.grid_size = 3
        self.win_length = 3
        self.last_winner = None
        
        self.pvp_score_x = 0
        self.pvp_score_o = 0
        self.pvp_ties = 0
        
        self.pva_score_x = 0
        self.pva_score_o = 0
        self.pva_ties = 0

    def select_mode(self, mode, difficulty=None, grid_size=3, win_length=3):
        self.game_mode = mode
        self.difficulty = difficulty
        self.grid_size = int(grid_size)
        self.win_length = int(win_length)

    def start_game(self):
        self.board = [None] * (self.grid_size * self.grid_size)
        self.game_active = True
        self.current_player = PLAYER_X
        self.last_winner = None

    def make_move(self, index, player):
        if self.board[index] is None:
            self.board[index] = player
            return True
        return False

    def handle_cell_click(self, index):
        if not self.game_active or self.board[index] is not None:
            return None

        if self.game_mode == 'pvp' or (self.game_mode == 'pva' and self.current_player == PLAYER_X):
            if self.make_move(index, self.current_player):
                if self.check_game_over():
                    return
                
                if self.game_mode == 'pvp':
                    self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
                else:
                    self.current_player = PLAYER_O
                    self.ai_move()

    def ai_move(self):
        move_index = get_ai_move(self.board, self.grid_size, self.difficulty)
        if move_index is not None:
            self.make_move(move_index, PLAYER_O)
            
        if self.check_game_over():
            return
            
        self.current_player = PLAYER_X
        self.game_active = True

    def check_game_over(self):
        winner = check_winner(self.board, self.grid_size, self.win_length)
        if winner:
            self.end_game(winner)
            return True
        return False

    def end_game(self, result):
        self.game_active = False
        self.last_winner = result
        if result == 'draw':
            if self.game_mode == 'pvp':
                self.pvp_ties += 1
            else:
                self.pva_ties += 1
        else:
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

game = TicTacToeLogic()

class RequestHandler(BaseHTTPRequestHandler):
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
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            action = data.get('action')
            
            if action == 'start':
                game.select_mode(
                    data.get('mode'), 
                    data.get('difficulty'), 
                    data.get('size', 3), 
                    data.get('length', 3)
                )
                game.start_game()
            elif action == 'click':
                index = data.get('index')
                game.handle_cell_click(index)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'board': game.board,
                'game_active': game.game_active,
                'current_player': game.current_player,
                'game_mode': game.game_mode,
                'winner': getattr(game, 'last_winner', None) if not game.game_active else None,
                'pvp_score_x': game.pvp_score_x,
                'pvp_score_o': game.pvp_score_o,
                'pvp_ties': game.pvp_ties,
                'pva_score_x': game.pva_score_x,
                'pva_score_o': game.pva_score_o,
                'pva_ties': game.pva_ties
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Serving Tic-Tac-Toe locally at http://localhost:8000")
    print("Press Ctrl+C to quit.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run_server()
