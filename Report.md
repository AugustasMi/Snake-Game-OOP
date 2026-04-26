# 1. Introduction

## What is your application?

This application is a Snake game built by using Python. It uses tkinter
library to create game window. The goal is for the player to eat food to
grow longer and survive and to achieve the highest score possible. The
game ends when the snake hits a wall or itself.

## How to run the program?

1.  Make sure that Python(version 3) is installed.
2.  Save the code into file (for example snake_game.py).
3.  Run the program.

## How to use the program?

-   Press any arrow keys to start.
-   Use arrow keys to control the snake.
-   Eat red food squares to grow and increase your score.
-   Avoid hitting the walls and colliding with yourself.
-   Press space to restart the game.

# 2. Body / Analysis

## Polymorphism

Polymorphism has the ability to use the same method differently in
different classes. Maistas and Snake use the same draw() method but in
their own ways.

``` python
class Maistas(Objektas):
    def draw(self, canvas):
        canvas.create_rectangle(..., fill="red")

class Snake(Objektas):
    def draw(self, canvas):
        canvas.create_rectangle(..., fill="lime green")
```

## Abstraction

Abstraction has a means of hiding complex implementation details and
showing only the necessary parts of an object. The best example is in
the snake.move() method.

``` python
def move(self):
    for i in range(len(self.kunas)-1, -1, -1):
        self.pozicija.move(self.dx * SEGMENTO_DYDIS, self.dy * SEGMENTO_DYDIS)
```

## Inheritance

Inheritance allows a new class to reuse code from an existing class.
Both Snake and Maistas classes inherit code from the base class
Objektas.

``` python
class Snake(Objektas):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kunas = []
        self.dx = 0
```

## Encapsulation

Encapsulation is mean of hiding internals and controlling their access
through methods. Pozicija class shows it the best.

``` python
class Pozicija:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
```

## Design pattern

The MaistoFactory uses factory method which creates objects without
specifying the exact class of an object that will be created. It is the
most suitable because it allows Game class to request new items without
needing to know specific math, grid or parameters required.

``` python
class MaistoFactory:
    @staticmethod
    def sukurti_maista():
        return Maistas(
            random.randint(0, PLOTIS-1) * SEGMENTO_DYDIS,
            random.randint(0, ILGIS-1) * SEGMENTO_DYDIS
        )
```

## Composition and Aggregation

The Game class uses composition where it contains Snake and Maistas
objects. They are created inside the Game constructor and can't exist
without it.

``` python
self.snake = Snake(5 * SEGMENTO_DYDIS, 5 * SEGMENTO_DYDIS)
self.maistas = MaistoFactory.sukurti_maista()
```

## Reading and writing to file

Input and output is handled by 2 functions: issaugoti_taskus and
nuskaityti_taskus.

``` python
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
```

## Testing

Testing was done while using unittest framework to test the
functionality.

# 3. Results and Summary

Application was successfully created using OOP principles in python.

A factory design pattern was utilized through MaistoFactory class to
handle the creation of food objects.

All four OOP pillars were applied.

Player scores are saved to and loaded from a text file score.txt using
file handling functions.

8 unit test were written and all passed.

## Conclusions

The goal was to create a functional Snake game using OOP principles. It
resulted in a functional snake game created by utilizing Tkinter library
for graphics. All scores are saved to a txt file and after every game
over it shows high score out of all of them. It could be improved by
adding varying speeds as the game progresses to add difficulty while
also adding sounds.
