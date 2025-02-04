import tkinter as tk
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100  # Milliseconds between moves
SPACE_SIZE = 50  # Size of each segment of the snake
BODY_PARTS = 3  # Initial number of segments
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        root.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def create_rounded_button(canvas, x, y, width, height, radius, text, command):
    # Create a rounded rectangle
    points = [
        x + radius, y,
        x + width - radius, y,
        x + width, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width, y + height,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height,
        x, y + height - radius,
        x, y + radius,
        x, y,
    ]
    canvas.create_polygon(points, smooth=True, fill="lightgray", outline="black")

    # Create the button text
    canvas.create_text(x + width / 2, y + height / 2, text=text, font=('consolas', 20))

    # Bind the click event to the button
    def on_click(event):
        if x <= event.x <= x + width and y <= event.y <= y + height:
            command()

    canvas.bind("<Button-1>", on_click)


def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    play_again_button = tk.Button(root, text="Play Again", command=play_again, font=('consolas', 20))
    quit_button = tk.Button(root, text="Quit", command=root.quit, font=('consolas', 20))
    canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50, window=play_again_button)
    canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, window=quit_button)

def play_again():
    global snake, food, direction, score

    canvas.delete(tk.ALL)
    direction = 'down'
    score = 0
    label.config(text="Score: {}".format(score))
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# Initialize the game window
root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

score = 0
direction = 'down'

label = tk.Label(root, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

root.update()

root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

root.mainloop()


