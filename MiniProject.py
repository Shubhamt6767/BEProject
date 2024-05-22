import random
import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Constants
BOARD_SIZE = 10
SHIP_SIZES = [5, 4, 3, 3, 2]
SHIP_NAMES = ['Carrier', 'Battleship', 'Cruiser', 'Submarine', 'Destroyer']
SHIP_COLORS = ['red', 'green', 'blue', 'orange', 'purple']
HIT_COLOR = 'black'
MISS_COLOR = 'white'

# Global variables
my_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
enemy_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
my_ships = []
enemy_ships = []
my_turn = False
game_over = False

# Networking variables
HOST = 'localhost'  # Enter the server's IP address or hostname
PORT = 5555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = None


def create_ships(board, ship_sizes):
    ships = []
    for size in ship_sizes:
        ship = []
        while True:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            direction = random.choice(['horizontal', 'vertical'])
            if can_place_ship(board, x, y, direction, size):
                if direction == 'horizontal':
                    for i in range(size):
                        board[x + i][y] = 1
                        ship.append((x + i, y))
                else:
                    for i in range(size):
                        board[x][y + i] = 1
                        ship.append((x, y + i))
                break
        ships.append(ship)
    return ships


def can_place_ship(board, x, y, direction, size):
    if direction == 'horizontal':
        for i in range(size):
            if x + i >= BOARD_SIZE or board[x + i][y] == 1:
                return False
    else:
        for i in range(size):
            if y + i >= BOARD_SIZE or board[x][y + i] == 1:
                return False
    return True


def initialize_game():
    global my_ships, enemy_ships, my_turn, game_over
    my_ships = create_ships(my_board, SHIP_SIZES)
    enemy_ships = create_ships(enemy_board, SHIP_SIZES)
    my_turn = random.choice([True, False])
    game_over = False


def start_game():
    initialize_game()
    if client_socket:
        send_message('start')
    update_status_label()


def send_message(message):
    try:
        client_socket.send(message.encode())
    except:
        messagebox.showerror('Error', 'Failed to send message.')


def receive_messages():
    global my_turn, game_over
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == 'start':
                initialize_game()
                my_turn = False
                update_status_label()
            elif message == 'your_turn':
                my_turn = True
                update_status_label()
            elif message.startswith('shoot'):
                _, x, y = message.split()
                x = int(x)
                y = int(y)
                if my_board[x][y] == 1:
                    my_board[x][y] = 2
                    hit_ship = get_ship_from_coords(my_ships, x, y)
                    if is_ship_sunk(hit_ship):
                        update_ship_status_label(hit_ship, 'Sunk')
                        if check_game_over(my_ships):
                            game_over = True
                            messagebox.showinfo('Game Over', 'You lost the game!')
                    else:
                        update_ship_status_label(hit_ship, 'Hit')
                else:
                    my_board[x][y] = -1
                    update_board_button(x, y, MISS_COLOR)
                    if check_game_over(my_ships):
                        game_over = True
                        messagebox.showinfo('Game Over', 'You won the game!')
                    else:
                        send_message('your_turn')
        except:
            break


def get_ship_from_coords(ships, x, y):
    for ship in ships:
        if (x, y) in ship:
            return ship
    return None


def is_ship_sunk(ship):
    for coord in ship:
        x, y = coord
        if my_board[x][y] != 2:
            return False
    return True


def check_game_over(ships):
    for ship in ships:
        if not is_ship_sunk(ship):
            return False
    return True


def update_status_label():
    if my_turn:
        status_label.config(text='Your Turn', fg='green')
    else:
        status_label.config(text="Opponent's Turn", fg='red')


def update_ship_status_label(ship, status):
    ship_index = my_ships.index(ship)
    ship_status_labels[ship_index].config(text=status)


def update_board_button(x, y, color):
    button = my_board_buttons[x][y]
    button.config(bg=color)
    button['state'] = 'disabled'


def shoot(x, y):
    global my_turn
    if not my_turn or game_over:
        return
    if enemy_board[x][y] == 0:
        enemy_board[x][y] = -1
        update_board_button(x, y, MISS_COLOR)
        send_message(f'shoot {x} {y}')
        my_turn = False
        update_status_label()
    else:
        messagebox.showerror('Invalid Move', 'You already shot there!')


def create_board_buttons(frame, board, click_handler):
    buttons = []
    for row in range(BOARD_SIZE):
        row_buttons = []
        for col in range(BOARD_SIZE):
            button = tk.Button(frame, width=2, bg='gray',
                               command=lambda x=row, y=col: click_handler(x, y))
            button.grid(row=row, column=col, padx=1, pady=1)
            row_buttons.append(button)
        buttons.append(row_buttons)
    return buttons


def create_ship_status_labels(frame, ship_names, ship_colors):
    labels = []
    for i in range(len(ship_names)):
        label = tk.Label(frame, text=ship_names[i], bg=ship_colors[i])
        label.grid(row=i, column=0, padx=5, pady=2, sticky='w')
        labels.append(label)
    return labels


def main():
    global client_socket

    root = tk.Tk()
    root.title('Battleship Game')

    # Create game boards
    my_board_frame = tk.Frame(root)
    my_board_frame.pack(side='left', padx=10, pady=10)
    my_board_buttons = create_board_buttons(my_board_frame, my_board, shoot)

    enemy_board_frame = tk.Frame(root)
    enemy_board_frame.pack(side='right', padx=10, pady=10)
   

