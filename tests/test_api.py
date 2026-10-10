import unittest
import threading
import json
import urllib.request
from http.server import HTTPServer
from logic import RequestHandler


class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Bind to port 0 to let OS select any free ephemeral port
        cls.server = HTTPServer(('127.0.0.1', 0), RequestHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_get_index_html(self):
        url = f"http://127.0.0.1:{self.port}/"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            content = response.read().decode('utf-8')
            self.assertIn("Tic-Tac-Toe AI with Fun Modes", content)
            self.assertIn('id="game-board"', content)
            self.assertNotIn("Team NextGen", content)

    def test_get_style_css(self):
        url = f"http://127.0.0.1:{self.port}/style.css"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("text/css", response.headers.get('Content-Type'))

    def test_post_api_action_start_and_click(self):
        url = f"http://127.0.0.1:{self.port}/api/action"

        # Start game
        start_payload = json.dumps({
            "action": "start",
            "mode": "pvp",
            "size": 3,
            "length": 3,
            "reset_scores": True
        }).encode('utf-8')

        req = urllib.request.Request(
            url, data=start_payload,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data['game_active'])
            self.assertEqual(data['current_player'], 'X')
            self.assertEqual(data['pvp_score_x'], 0)
            self.assertEqual(len(data['board']), 9)

        # Click move
        click_payload = json.dumps({
            "action": "click",
            "index": 4
        }).encode('utf-8')

        req = urllib.request.Request(
            url, data=click_payload,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(data['board'][4], 'X')
            self.assertEqual(data['current_player'], 'O')
            self.assertEqual(data['sound'], 'click')


if __name__ == '__main__':
    unittest.main()
