import tkinter
import random
import os

ILGIS = 25
PLOTIS = 25
SEGMENTO_DYDIS = 25
LANGO_PLOTIS = SEGMENTO_DYDIS*PLOTIS
LANGO_ILGIS = SEGMENTO_DYDIS*ILGIS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILE_PATH = os.path.join(BASE_DIR, "score.txt")


class Pozicija:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Objektas:
    def __init__(self, x, y):
        self.pozicija = Pozicija(x, y)

    def draw(self, canvas):
        pass


class Maistas(Objektas):
    def draw(self, canvas):
        canvas.create_rectangle(
            self.pozicija.x,
            self.pozicija.y,
            self.pozicija.x + SEGMENTO_DYDIS,
            self.pozicija.y + SEGMENTO_DYDIS,
            fill="red"
        )


class Snake(Objektas):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kunas = []
        self.dx = 0
        self.dy = 0

    def move(self):
        for i in range(len(self.kunas)-1, -1, -1):
            if i == 0:
                self.kunas[i].x = self.pozicija.x
                self.kunas[i].y = self.pozicija.y
            else:
                self.kunas[i].x = self.kunas[i-1].x
                self.kunas[i].y = self.kunas[i-1].y

        self.pozicija.move(self.dx * SEGMENTO_DYDIS, self.dy * SEGMENTO_DYDIS)

    def grow(self):
        self.kunas.append(Pozicija(self.pozicija.x, self.pozicija.y))

    def draw(self, canvas):
        canvas.create_rectangle(
            self.pozicija.x,
            self.pozicija.y,
            self.pozicija.x+SEGMENTO_DYDIS,
            self.pozicija.y+SEGMENTO_DYDIS,
            fill="lime green"
        )

        for segment in self.kunas:
            canvas.create_rectangle(
                segment.x,
                segment.y,
                segment.x+SEGMENTO_DYDIS,
                segment.y+SEGMENTO_DYDIS,
                fill="lime green"
            )


class MaistoFactory:
    @staticmethod
    def sukurti_maista():
        return Maistas(
            random.randint(0, PLOTIS-1)*SEGMENTO_DYDIS,
            random.randint(0, ILGIS-1)*SEGMENTO_DYDIS
        )


def issaugoti_taskus(taskai):
    with open(SCORE_FILE_PATH, "a") as f:
        f.write(f"{taskai}\n")


def nuskaityti_taskus():
    try:
        if not os.path.exists(SCORE_FILE_PATH):
            return 0
        with open(SCORE_FILE_PATH, "r") as f:
            lines = f.readlines()
            scores = [int(s.strip()) for s in lines if s.strip().isdigit()]
            return max(scores) if scores else 0
    except Exception:
        return 0


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(
            root, bg="black", width=LANGO_PLOTIS, height=LANGO_ILGIS
        )
        self.canvas.pack()

        self.restart()
        self.high_score = nuskaityti_taskus()
        self.root.bind("<KeyRelease>", self.change_direction)
        self.update()

    def change_direction(self, e):
        if self.game_over and e.keysym == "space":
            self.restart()
            return

        if self.game_over:
            return

        if e.keysym == "Up" and self.snake.dy != 1:
            self.snake.dx = 0
            self.snake.dy = -1
        if e.keysym == "Down" and self.snake.dy != -1:
            self.snake.dx = 0
            self.snake.dy = 1
        if e.keysym == "Left" and self.snake.dx != 1:
            self.snake.dx = -1
            self.snake.dy = 0
        if e.keysym == "Right" and self.snake.dx != -1:
            self.snake.dx = 1
            self.snake.dy = 0

    def restart(self):
        self.snake = Snake(5 * SEGMENTO_DYDIS, 5 * SEGMENTO_DYDIS)
        self.maistas = MaistoFactory.sukurti_maista()
        self.game_over = False
        self.taskai = 0

    def update(self):
        if not self.game_over:
            self.snake.move()
            self.check_collisions()

        self.draw()
        self.root.after(100, self.update)

    def check_collisions(self):
        # Wall
        if (
            self.snake.pozicija.x < 0 or
            self.snake.pozicija.x >= LANGO_PLOTIS or
            self.snake.pozicija.y < 0 or
            self.snake.pozicija.y >= LANGO_ILGIS
        ):
            self.end_game()
        # Body
        for segment in self.snake.kunas:
            if (self.snake.pozicija.x == segment.x and
               self.snake.pozicija.y == segment.y):
                self.end_game()
        # FOOD
        if (
            self.snake.pozicija.x == self.maistas.pozicija.x and
            self.snake.pozicija.y == self.maistas.pozicija.y
        ):
            self.snake.grow()
            self.maistas = MaistoFactory.sukurti_maista()
            self.taskai += 1

            if self.taskai > self.high_score:
                self.high_score = self.taskai

    def end_game(self):
        if not self.game_over:
            self.game_over = True
            issaugoti_taskus(self.taskai)

    def draw(self):
        self.canvas.delete("all")

        self.maistas.draw(self.canvas)
        self.snake.draw(self.canvas)

        if self.game_over:
            self.canvas.create_text(
                LANGO_PLOTIS/2,
                LANGO_ILGIS/2,
                fill="white",
                font=("Arial", 25),
                text=f"Game Over: {self.taskai}"
            )
            self.canvas.create_text(
                LANGO_PLOTIS/2,
                LANGO_ILGIS/2+30,
                fill="white",
                font=("Arial", 15),
                text="Press SPACE to restart"
            )
            self.canvas.create_text(
                LANGO_PLOTIS/2,
                LANGO_ILGIS/2-30,
                fill="white",
                font=("Arial", 15),
                text=f"High score: {self.high_score}"
            )
        else:
            self.canvas.create_text(
                70, 20,
                fill="white",
                font=("Arial", 15),
                text=f"Score: {self.taskai}"
            )

if __name__=="__main__":
    root = tkinter.Tk()
    root.title("Snake Game")
    root.resizable(False, False)
    game = Game(root)
    root.mainloop()
