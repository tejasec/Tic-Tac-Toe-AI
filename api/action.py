import json
from http.server import BaseHTTPRequestHandler

from logic import TicTacToeLogic, apply_action, decode_game_session, encode_game_session


class handler(BaseHTTPRequestHandler):
    """Vercel Function endpoint for stateless, per-browser game sessions."""

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length < 0 or content_length > 32768:
                self._send_json(413, {'error': 'Request is too large.'})
                return
            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode('utf-8'))
            if not isinstance(data, dict):
                raise ValueError('Request must be a JSON object.')

            session_token = data.pop('session_token', None)
            game = decode_game_session(session_token) if session_token else TicTacToeLogic()
            state = apply_action(game, data)
            state['session_token'] = encode_game_session(game.__dict__)
            self._send_json(200, state)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            self._send_json(400, {'error': str(exc) or 'Invalid request.'})
        except RuntimeError as exc:
            self._send_json(500, {'error': str(exc)})

    def do_GET(self):
        self._send_json(405, {'error': 'Use POST for game actions.'})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
