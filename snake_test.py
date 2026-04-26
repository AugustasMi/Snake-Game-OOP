import unittest
from unittest.mock import patch, mock_open
import tkinter

from snake_game import (
    Pozicija, Snake, MaistoFactory,
    issaugoti_taskus, nuskaityti_taskus,
    SEGMENTO_DYDIS, PLOTIS, ILGIS,
    SCORE_FILE_PATH, Game
)


class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_pozicija(self):
        pos = Pozicija(10, 20)
        self.assertEqual(pos.x, 10)
        self.assertEqual(pos.y, 20)
        pos.move(5, -5)
        self.assertEqual(pos.x, 15)
        self.assertEqual(pos.y, 15)

    def test_snake_growth_movement(self):
        snake = Snake(100, 100)
        snake.dx = 1
        snake.dy = 0
        snake.grow()
        snake.move()
        self.assertEqual(snake.pozicija.x, 100+SEGMENTO_DYDIS)
        self.assertEqual(snake.kunas[0].x, 100)
        self.assertEqual(snake.kunas[0].y, 100)

    def test_maisto_factory_limits(self):
        maistas = MaistoFactory.sukurti_maista()
        self.assertTrue(0 <= maistas.pozicija.x < PLOTIS*SEGMENTO_DYDIS)
        self.assertTrue(0 <= maistas.pozicija.y < ILGIS*SEGMENTO_DYDIS)

    @patch("snake_game.open", new_callable=mock_open)
    def test_save_score(self, mock_file):
        issaugoti_taskus(10)
        mock_file.assert_called_with(SCORE_FILE_PATH, "a")

    @patch("snake_game.os.path.exists", return_value=True)
    @patch("snake_game.open", new_callable=mock_open, read_data="5\n15\n10\n")
    def test_read_high_score(self, mock_file, mock_exists):
        result = nuskaityti_taskus()
        self.assertEqual(result, 15)

    def test_food(self):
        game = Game(self.root)

        game.snake.pozicija.x = 100
        game.snake.pozicija.y = 100
        game.maistas.pozicija.x = 100
        game.maistas.pozicija.y = 100

        game.check_collisions()
        self.assertEqual(game.taskai, 1)

    def test_wall_boundaries(self):

        game = Game(self.root)
        game.snake.pozicija.x = -SEGMENTO_DYDIS
        game.check_collisions()
        self.assertTrue(game.game_over)

    def test_self_collision(self):
        game = Game(self.root)
        game.snake.kunas.append(Pozicija(100, 100))
        game.snake.pozicija.x = 100
        game.snake.pozicija.y = 100
        game.check_collisions()
        self.assertTrue(game.game_over)


if __name__ == "__main__":
    unittest.main()
