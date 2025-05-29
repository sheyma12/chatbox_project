import tkinter as tk
from tkinter import messagebox
import random
from difflib import SequenceMatcher

# --- Trivia ---

trivia_questions = [
    {"question": "What is the capital of France?", "answer": "paris"},
    {"question": "Who wrote '1984'?", "answer": "george orwell"},
    {"question": "What is the smallest planet in our solar system?", "answer": "mercury"},
    {"question": "What is the square root of 64?", "answer": "8"},
    {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci"},
    {"question": "How many continents are there?", "answer": "7"},
    {"question": "What is the chemical symbol for gold?", "answer": "au"},
    {"question": "In which year did the Titanic sink?", "answer": "1912"},
    {"question": "What is the capital of Japan?", "answer": "tokyo"},
    {"question": "Who discovered penicillin?", "answer": "alexander fleming"}
]

def check_similarity(user_input, correct_answer, threshold=0.6):
    similarity = SequenceMatcher(None, user_input.lower(), correct_answer.lower()).ratio()
    return similarity >= threshold

class TriviaGame:
    def _init_(self, master):
        self.master = master
        self.questions_pool = trivia_questions.copy()
        self.questions = random.sample(self.questions_pool, 10) if len(self.questions_pool) >= 10 else self.questions_pool
        self.index = 0
        self.score = 0
        self.active = False

        self.frame = tk.Frame(master)
        self.frame.pack(fill='both', expand=True)

        self.question_label = tk.Label(self.frame, text="", font=('Arial', 14), wraplength=500)
        self.question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.frame, font=('Arial', 14))
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", self.submit_answer)

        self.feedback_label = tk.Label(self.frame, text="", font=('Arial', 12))
        self.feedback_label.pack(pady=5)

        self.next_button = tk.Button(self.frame, text="Next", command=self.next_question, state='disabled')
        self.next_button.pack(pady=10)

        self.score_label = tk.Label(self.frame, text="", font=('Arial', 12))
        self.score_label.pack(pady=10)

    def start(self):
        self.index = 0
        self.score = 0
        self.active = True
        self.feedback_label.config(text="")
        self.score_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.next_button.config(state='disabled')
        self.answer_entry.pack()
        self.show_question()

    def show_question(self):
        if self.index < len(self.questions):
            self.question_label.config(text=f"Q{self.index + 1}: {self.questions[self.index]['question']}")
            self.answer_entry.config(state='normal')
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()
            self.next_button.config(state='disabled')
            self.feedback_label.config(text="")
        else:
            self.end_game()

    def submit_answer(self, event=None):
        if not self.active or self.index >= len(self.questions):
            return
        user_ans = self.answer_entry.get().strip()
        if not user_ans:
            return
        correct_answer = self.questions[self.index]['answer']
        if check_similarity(user_ans, correct_answer):
            self.score += 1
            self.feedback_label.config(text="Correct!", fg='green')
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer: {correct_answer}", fg='red')
        self.answer_entry.config(state='disabled')
        self.next_button.config(state='normal')

    def next_question(self):
        self.index += 1
        self.show_question()

    def end_game(self):
        self.active = False
        self.question_label.config(text=f"Game over! Your score: {self.score} / {len(self.questions)}")
        self.answer_entry.pack_forget()
        self.next_button.config(state='disabled')
        self.feedback_label.config(text="")
        self.score_label.config(text="Use menu buttons to play other games or chat.")

    def pack_forget(self):
        self.frame.pack_forget()

    def pack(self):
        self.frame.pack(fill='both', expand=True)


# --- Connect Four ---

class ConnectFour:
    ROWS = 6
    COLS = 7

    def _init_(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.current_player = "Red"
        self.board = [["" for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.buttons = []
        self.vs_computer = None

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        self.create_mode_selection()

    def create_mode_selection(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.frame, text="Select Mode:", font=('Arial', 16))
        label.pack(pady=10)

        pvp_btn = tk.Button(self.frame, text="Two Players", font=('Arial', 14),
                            command=lambda: self.start_game(False))
        pvp_btn.pack(pady=5)

        pvc_btn = tk.Button(self.frame, text="Play vs Computer", font=('Arial', 14),
                            command=lambda: self.start_game(True))
        pvc_btn.pack(pady=5)

    def start_game(self, vs_computer):
        self.vs_computer = vs_computer
        self.current_player = "Red"
        self.board = [["" for _ in range(self.COLS)] for _ in range(self.ROWS)]

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = []
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack()
        for c in range(self.COLS):
            btn = tk.Button(btn_frame, text=str(c+1), width=4, command=lambda col=c: self.play(col))
            btn.grid(row=0, column=c)
            self.buttons.append(btn)

        self.canvas = tk.Canvas(self.frame, width=self.COLS*60, height=self.ROWS*60, bg="blue")
        self.canvas.pack()
        self.draw_board()

        restart_btn = tk.Button(self.frame, text="Restart", command=lambda: self.start_game(self.vs_computer))
        restart_btn.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.ROWS):
            for c in range(self.COLS):
                x1 = c*60 + 5
                y1 = r*60 + 5
                x2 = x1 + 50
                y2 = y1 + 50
                color = "white"
                if self.board[r][c] == "Red":
                    color = "red"
                elif self.board[r][c] == "Yellow":
                    color = "yellow"
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")

    def play(self, col):
        if not self.is_column_available(col):
            messagebox.showwarning("Invalid Move", "Column is full!")
            return

        self.make_move(col, self.current_player)
        self.draw_board()

        if self.check_winner(self.current_player):
            messagebox.showinfo("Game Over", f"{self.current_player} wins!")
            self.disable_buttons()
            return
        elif self.is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.disable_buttons()
            return

        self.switch_player()

        if self.vs_computer and self.current_player == "Yellow":
            self.root.after(300, self.computer_move)

    def is_column_available(self, col):
        return self.board[0][col] == ""

    def make_move(self, col, player):
        for r in reversed(range(self.ROWS)):
            if self.board[r][col] == "":
                self.board[r][col] = player
                break

    def switch_player(self):
        self.current_player = "Yellow" if self.current_player == "Red" else "Red"

    def computer_move(self):
        col = self.find_winning_move("Yellow")
        if col is None:
            col = self.find_winning_move("Red")
        if col is None:
            available_cols = [c for c in range(self.COLS) if self.is_column_available(c)]
            col = random.choice(available_cols) if available_cols else None

        if col is not None:
            self.make_move(col, "Yellow")
            self.draw_board()
            if self.check_winner("Yellow"):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.disable_buttons()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
                return
            self.switch_player()

    def find_winning_move(self, player):
        for col in range(self.COLS):
            if not self.is_column_available(col):
                continue
            row = self.get_row_for_col(col)
            self.board[row][col] = player
            if self.check_winner(player):
                self.board[row][col] = ""
                return col
            self.board[row][col] = ""
        return None

    def get_row_for_col(self, col):
        for r in reversed(range(self.ROWS)):
            if self.board[r][col] == "":
                return r
        return None

    def check_winner(self, player):
        b = self.board
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if b[r][c] != player:
                    continue
                if r + 3 < self.ROWS and all(b[r+i][c] == player for i in range(4)):
                    return True
                if c + 3 < self.COLS and all(b[r][c+i] == player for i in range(4)):
                    return True
                if r + 3 < self.ROWS and c + 3 < self.COLS and all(b[r+i][c+i] == player for i in range(4)):
                    return True
                if r + 3 < self.ROWS and c - 3 >= 0 and all(b[r+i][c-i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self):
        return all(self.board[0][c] != "" for c in range(self.COLS))

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def pack_forget(self):
        self.frame.pack_forget()

    def pack(self):
        self.frame.pack(fill='both', expand=True)


# --- Snake Game ---

class SnakeGame:
    def _init_(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.direction = "Right"
        self.score = 0

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.food = None
        self.game_running = True

        self.root.bind("<Key>", self.change_direction)
        self.spawn_food()
        self.move_snake()

    def draw_objects(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="lime", outline="")

        if self.food:
            x, y = self.food
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="")

        self.canvas.create_text(60, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

    def spawn_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        key = event.keysym
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if key in ["Left", "Right", "Up", "Down"]:
            if opposites[key] != self.direction:
                self.direction = key

    def move_snake(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= self.width // self.cell_size or
            head_y < 0 or head_y >= self.height // self.cell_size or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw_objects()
        self.root.after(100, self.move_snake)

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.width//2, self.height//2, text="GAME OVER",
                                fill="red", font=("Arial", 30))
        self.canvas.create_text(self.width//2, self.height//2 + 40, text=f"Final Score: {self.score}",
                                fill="white", font=("Arial", 20))
        self.canvas.create_text(self.width//2, self.height//2 + 80, text="Click to Restart",
                                fill="yellow", font=("Arial", 16))
        self.canvas.bind("<Button-1>", self.restart)

    def restart(self, event):
        self.canvas.unbind("<Button-1>")
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.direction = "Right"
        self.score = 0
        self.game_running = True
        self.spawn_food()
        self.move_snake()

    def pack_forget(self):
        self.frame.pack_forget()

    def pack(self):
        self.frame.pack(fill='both', expand=True)


# --- Tic Tac Toe ---

class TicTacToe:
    def _init_(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.buttons = [[None]*3 for _ in range(3)]
        self.vs_computer = None

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        self.create_mode_selection()

    def create_mode_selection(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.frame, text="Select Mode:", font=('Arial', 16))
        label.pack(pady=10)

        pvp_btn = tk.Button(self.frame, text="Two Players", font=('Arial', 14),
                            command=lambda: self.start_game(False))
        pvp_btn.pack(pady=5)

        pvc_btn = tk.Button(self.frame, text="Play vs Computer", font=('Arial', 14),
                            command=lambda: self.start_game(True))
        pvc_btn.pack(pady=5)

    def start_game(self, vs_computer):
        self.vs_computer = vs_computer
        self.current_player = "X"
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.frame)
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=('Arial', 40), width=5, height=2,
                                command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        restart_btn = tk.Button(self.frame, text="Restart", font=('Arial', 14), command=lambda: self.start_game(self.vs_computer))
        restart_btn.pack(pady=10)

        back_btn = tk.Button(self.frame, text="Back to Mode Selection", font=('Arial', 12), command=self.create_mode_selection)
        back_btn.pack(pady=5)

    def on_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "" and not self.check_winner():
            btn["text"] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                return
            self.switch_player()
            if self.vs_computer and self.current_player == "O":
                self.root.after(300, self.computer_move)

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def computer_move(self):
        best_score = -float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.buttons[r][c]["text"] == "":
                    self.buttons[r][c]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[r][c]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            r, c = best_move
            self.buttons[r][c]["text"] = "O"
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                return
            self.switch_player()

    def minimax(self, is_maximizing):
        if self.check_winner():
            return 1 if not is_maximizing else -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.buttons[r][c]["text"] == "":
                        self.buttons[r][c]["text"] = "O"
                        score = self.minimax(False)
                        self.buttons[r][c]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.buttons[r][c]["text"] == "":
                        self.buttons[r][c]["text"] = "X"
                        score = self.minimax(True)
                        self.buttons[r][c]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        b = self.buttons
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return True
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return True
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return True
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return True
        return False

    def is_draw(self):
        for row in self.buttons:
            for btn in row:
                if btn["text"] == "":
                    return False
        return True

    def pack_forget(self):
        self.frame.pack_forget()

    def pack(self):
        self.frame.pack(fill='both', expand=True)


# --- UNO ---

colors = ["Red", "Green", "Blue", "Yellow"]
values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
specials = ["Wild", "Wild Draw Four"]

def create_deck():
    deck = []
    for color in colors:
        for value in values:
            deck.append((color, value))
            if value != "0":
                deck.append((color, value))
    for _ in range(4):
        for special in specials:
            deck.append(("Black", special))
    random.shuffle(deck)
    return deck

class UnoGame:
    def _init_(self, root):
        self.root = root
        self.root.title("UNO Game")

        self.player_score = 0
        self.cpu1_score = 0
        self.cpu2_score = 0

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        self.start_game()

    def start_game(self):
        self.deck = create_deck()
        self.player_hand = [self.deck.pop() for _ in range(7)]
        self.cpu1_hand = [self.deck.pop() for _ in range(7)]
        self.cpu2_hand = [self.deck.pop() for _ in range(7)]
        self.discard_pile = [self.deck.pop()]
        self.current_color = self.discard_pile[-1][0]
        self.turn = 0
        self.direction = 1

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.score_label = tk.Label(self.frame, text=self.get_score_text(), font=("Helvetica", 12))
        self.score_label.pack()

        self.top_card_label = tk.Label(self.frame, text="", font=("Helvetica", 14, "bold"))
        self.top_card_label.pack(pady=5)

        self.message_var = tk.StringVar()
        self.info_label = tk.Label(self.frame, textvariable=self.message_var, font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        self.hand_frame = tk.Frame(self.frame)
        self.hand_frame.pack(pady=10)

        self.draw_button = tk.Button(self.frame, text="Draw Card", command=self.draw_card)
        self.draw_button.pack()

        self.play_again_button = tk.Button(self.frame, text="Play Again", command=self.start_game)
        self.play_again_button.pack(pady=10)
        self.play_again_button.config(state="disabled")

        self.message_var.set("Your turn. Select a card or draw one.")
        self.update_ui()

    def get_score_text(self):
        return f"Scores - You: {self.player_score} | CPU 1: {self.cpu1_score} | CPU 2: {self.cpu2_score}"

    def update_ui(self):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        top_card = self.discard_pile[-1]
        self.top_card_label.config(text=f"Top card: {top_card[0]} {top_card[1]}")

        if self.turn == 0:
            for card in self.player_hand:
                fg_color = "black" if card[0] == "Yellow" else "white"
                btn = tk.Button(self.hand_frame, text=f"{card[0]}\n{card[1]}", bg=card[0].lower(), fg=fg_color,
                                command=lambda c=card: self.play_card(c))
                btn.pack(side=tk.LEFT, padx=5)
            self.draw_button.config(state="normal")
            self.message_var.set("Your turn. Select a card or draw one.")
        else:
            self.draw_button.config(state="disabled")
            self.message_var.set(f"CPU {self.turn} is thinking...")
            self.root.after(1000, self.cpu_turn)

        self.score_label.config(text=self.get_score_text())

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.player_hand.append(card)
            if self.is_playable(card):
                self.player_hand.remove(card)
                self.message_var.set(f"You drew and played: {card[0]} {card[1]}")
                self.play_logic(card, is_player=True)
            else:
                self.message_var.set(f"You drew: {card[0]} {card[1]}. No playable cards, turn passed.")
                self.next_turn()
            self.update_ui()

    def play_card(self, card):
        if self.turn != 0:
            return
        if self.is_playable(card):
            self.player_hand.remove(card)
            self.play_logic(card, is_player=True)
            self.update_ui()
        else:
            self.message_var.set("You can't play that card.")

    def is_playable(self, card):
        top_color, top_value = self.discard_pile[-1]
        color, value = card
        return color == self.current_color or value == top_value or color == "Black"

    def play_logic(self, card, is_player=False):
        color, value = card
        if value.startswith("Wild"):
            if is_player:
                self.choose_color(card)
                return
            else:
                color = random.choice(colors)

        if value == "Skip":
            self.next_turn()
        elif value == "Reverse":
            self.direction *= -1
        elif value == "Draw Two":
            self.give_cards(self.get_next_turn(), 2)
        elif value == "Wild Draw Four":
            self.give_cards(self.get_next_turn(), 4)

        self.discard_pile.append((color, value))
        self.current_color = color
        self.next_turn()

    def choose_color(self, wild_card):
        def set_color(selected_color):
            self.discard_pile.append((selected_color, wild_card[1]))
            self.current_color = selected_color
            self.color_window.destroy()
            self.next_turn()
            self.update_ui()

        self.color_window = tk.Toplevel(self.root)
        self.color_window.title("Choose Color")

        for col in colors:
            btn = tk.Button(self.color_window, text=col, bg=col.lower(), fg="white", width=10,
                            command=lambda c=col: set_color(c))
            btn.pack(pady=5)

    def cpu_turn(self):
        hand = self.cpu1_hand if self.turn == 1 else self.cpu2_hand
        playable = [card for card in hand if self.is_playable(card)]

        if playable:
            card = playable[0]
            hand.remove(card)
            self.message_var.set(f"CPU {self.turn} played {card[0]} {card[1]}")
            self.play_logic(card)
        else:
            if self.deck:
                card = self.deck.pop()
                hand.append(card)
                self.message_var.set(f"CPU {self.turn} drew a card.")
                if self.is_playable(card):
                    hand.remove(card)
                    self.message_var.set(f"CPU {self.turn} played {card[0]} {card[1]} after drawing.")
                    self.play_logic(card)
                else:
                    self.next_turn()
            else:
                self.next_turn()
        self.update_ui()
        self.check_winner()

    def give_cards(self, player, count):
        hand = self.player_hand if player == 0 else self.cpu1_hand if player == 1 else self.cpu2_hand
        for _ in range(count):
            if self.deck:
                hand.append(self.deck.pop())

    def next_turn(self):
        self.turn = (self.turn + self.direction) % 3

    def get_next_turn(self):
        return (self.turn + self.direction) % 3

    def check_winner(self):
        if not self.player_hand:
            self.player_score += 1
            self.end_game("You won! 🎉")
        elif not self.cpu1_hand:
            self.cpu1_score += 1
            self.end_game("CPU 1 won. 😐")
        elif not self.cpu2_hand:
            self.cpu2_score += 1
            self.end_game("CPU 2 won. 😐")

    def end_game(self, message):
        self.message_var.set(message)
        self.draw_button.config(state="disabled")
        self.play_again_button.config(state="normal")

    def pack_forget(self):
        self.frame.pack_forget()

    def pack(self):
        self.frame.pack(fill='both', expand=True)


# --- Chat App ---

class ChatApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Chatbox with Games")

        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(side='left', fill='both', expand=True)

        self.menu_frame = tk.Frame(root, width=200)
        self.menu_frame.pack(side='right', fill='y')

        self.text_display = tk.Text(self.chat_frame, state='disabled', wrap='word', height=20)
        self.text_display.pack(padx=10, pady=10, fill='both', expand=True)

        self.entry = tk.Entry(self.chat_frame)
        self.entry.pack(padx=10, pady=(0,10), fill='x')
        self.entry.bind('<Return>', self.on_enter)

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.on_send)
        self.send_button.pack(pady=(0,10))

        self.menu_label = tk.Label(self.menu_frame, text="Select an option:", font=('Arial', 14))
        self.menu_label.pack(pady=10)

        self.buttons = []

        self.trivia = TriviaGame(root)
        self.connectfour = ConnectFour(root)
        self.snake = SnakeGame(root)
        self.tictactoe = TicTacToe(root)
        self.uno = UnoGame(root)

        self.game_instances = {
            'Trivia': self.trivia,
            'Connect Four': self.connectfour,
            'Snake': self.snake,
            'Tic Tac Toe': self.tictactoe,
            'UNO': self.uno,
        }

        games = [
            ("Chat", self.activate_chat),
            ("Trivia", self.activate_trivia),
            ("Connect Four", self.activate_connectfour),
            ("Snake", self.activate_snake),
            ("Tic Tac Toe", self.activate_tictactoe),
            ("UNO", self.activate_uno),
            ("Help", self.show_help)
        ]

        for (text, cmd) in games:
            btn = tk.Button(self.menu_frame, text=text, width=18, command=cmd)
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.active_game = None

        self.activate_chat()

    def clear_active_game(self):
        if self.active_game:
            self.active_game.pack_forget()
            self.active_game = None

    def activate_chat(self):
        self.clear_active_game()
        welcome_text = (
            "Welcome! You can talk about:\n"
            "- Jokes\n"
            "- Fun Facts\n"
            "- Movies\n"
            "- TV Shows\n"
            "- Books\n"
            "(Warning: When the application first opens, the interface might not display correctly. To fix this, please click on the buttons in the following order: Chat, Trivia, Connect Four, Tic Tac Toe, UNO, and Help. This will properly load and reset the layout.)\n"
            "Type 'help' for commands.\n"
        )
        self.append_text(welcome_text)

    def activate_trivia(self):
        self.clear_active_game()
        self.active_game = self.trivia
        self.trivia.pack()
        self.trivia.start()
        self.append_text("Trivia started! Answer the questions.\n")

    def activate_connectfour(self):
        self.clear_active_game()
        self.active_game = self.connectfour
        self.connectfour.pack()

    def activate_snake(self):
        self.clear_active_game()
        self.active_game = self.snake
        self.snake.pack()

    def activate_tictactoe(self):
        self.clear_active_game()
        self.active_game = self.tictactoe
        self.tictactoe.pack()

    def activate_uno(self):
        self.clear_active_game()
        self.active_game = self.uno
        self.uno.pack()

    def show_help(self):
        self.clear_active_game()
        help_text = (
            "Available commands:\n"
            "- Chat: Talk about jokes, fun facts, movies, TV shows, books\n"
            "- Trivia: Play trivia quiz\n"
            "- Connect Four, Snake, Tic Tac Toe, UNO: Play games\n"
            "- Help: Show this help message\n"
            "Use menu buttons to switch modes."
        )
        self.append_text(help_text + "\n")

    def append_text(self, text):
        self.text_display.config(state='normal')
        self.text_display.insert(tk.END, text)
        self.text_display.config(state='disabled')
        self.text_display.see(tk.END)

    def on_enter(self, event):
        self.on_send()

    def on_send(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.append_text(f"You: {user_input}\n")
        self.entry.delete(0, tk.END)

        if user_input.lower() in ['bye', 'quit']:
            self.append_text("Chatbot: Goodbye! Closing app...\n")
            self.root.after(1000, self.root.quit)
            return

        if user_input.lower() == 'help':
            self.show_help()
            return

        if self.active_game == self.trivia and self.trivia.active:
            self.trivia.answer_entry.delete(0, tk.END)
            self.trivia.answer_entry.insert(0, user_input)
            self.trivia.submit_answer()
            return

        response = self.simple_chat_response(user_input)
        self.append_text(f"Chatbot: {response}\n")

    def simple_chat_response(self, user_input):
        low = user_input.lower()
        if 'joke' in low:
            return random.choice([
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the chicken join a band? Because it had drumsticks!",
                "Why don’t skeletons fight each other? They don’t have the guts.",
                "Why was the math book sad? Because it had too many problems.",
                "What do you get when you cross a snowman and a vampire? Frostbite!"
            ])
        elif 'fun fact' in low:
            return random.choice([
                "Bananas are berries, but strawberries are not!",
                "Honey never spoils! Archaeologists found pots of honey over 3,000 years old!",
                "Octopuses have three hearts and blue blood!",
                "The Eiffel Tower can grow 6 inches in summer due to iron expansion.",
                "A cloud can weigh more than a million pounds!"
            ])
        elif 'movie' in low:
            return random.choice([
                "I love The Matrix! It's a great movie about simulations.",
                "If you like action, Avengers: Endgame is a must-watch!",
                "How about a classic like The Godfather?",
                "For a heartwarming experience, watch The Pursuit of Happyness!",
                "Interstellar is a must-see for sci-fi fans. It's a journey through space and time!",
                "Inception is a mind-bending thriller. Have you watched it?",
                "The Shawshank Redemption is a masterpiece about hope and friendship.",
                "Parasite won the Oscar for Best Picture and is incredible.",
                "The Dark Knight redefined superhero movies."
            ])
        elif 'tv show' in low or 'series' in low:
            return random.choice([
                "Have you seen Breaking Bad? It's an amazing drama!",
                "Friends is a timeless comedy that never gets old.",
                "Stranger Things is perfect for fans of mystery and adventure.",
                "If you enjoy thrillers, give Black Mirror a try!",
                "The Crown is a fascinating look into the British royal family.",
                "Game of Thrones is legendary for fantasy fans.",
                "The Mandalorian brings Star Wars to a new level.",
                "Sherlock is a brilliant modern mystery series.",
                "The Office is a hilarious mockumentary comedy."
            ])
        elif 'book' in low or 'literature' in low:
            return random.choice([
                "Have you read '1984' by George Orwell? It's a thought-provoking classic.",
                "If you enjoy fantasy, 'The Hobbit' by J.R.R. Tolkien is a wonderful choice.",
                "For a thrilling mystery, try 'The Girl with the Dragon Tattoo' by Stieg Larsson.",
                "If you're into self-improvement, 'Atomic Habits' by James Clear is highly recommended.",
                "'Pride and Prejudice' by Jane Austen is a timeless romance novel.",
                "'To Kill a Mockingbird' by Harper Lee is a profound story about justice.",
                "'The Catcher in the Rye' explores teenage angst and identity.",
                "'The Great Gatsby' captures the Jazz Age in America.",
                "'Harry Potter' series is magical for all ages."
            ])
        else:
            return "Sorry, I don't understand that. Try 'help' for commands."


if _name_ == "_main_":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
