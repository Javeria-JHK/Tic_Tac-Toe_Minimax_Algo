from tkinter import StringVar, Tk, Button, Label, PhotoImage, messagebox
from tkinter.font import Font
from copy import deepcopy
import pygame

class Board:
    def __init__(self, other=None):
        self.player = 'X'
        self.opponent = 'O'
        self.empty = '.'
        self.size = 3
        self.fields = {(x, y): self.empty for y in range(self.size) for x in range(self.size)}
        # Copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def move(self, x, y):
        board = Board(self)
        board.fields[x, y] = board.player
        board.player, board.opponent = board.opponent, board.player
        return board

    def __minimax(self, player):
        if self.won():
            return (-1, None) if player else (+1, None)
        elif self.tied():
            return 0, None
        elif player:
            best = (-2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y).__minimax(not player)[0]
                    if value > best[0]:
                        best = (value, (x, y))
            return best
        else:
            best = (+2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y).__minimax(not player)[0]
                    if value < best[0]:
                        best = (value, (x, y))
            return best

    def best(self):
        return self.__minimax(True)[1]

    def tied(self):
        return all(self.fields[x, y] != self.empty for x, y in self.fields)

    def won(self):
        for y in range(self.size):
            if all(self.fields[x, y] == self.opponent for x in range(self.size)):
                return [(x, y) for x in range(self.size)]
        for x in range(self.size):
            if all(self.fields[x, y] == self.opponent for y in range(self.size)):
                return [(x, y) for y in range(self.size)]
        if all(self.fields[i, i] == self.opponent for i in range(self.size)):
            return [(i, i) for i in range(self.size)]
        if all(self.fields[i, self.size - 1 - i] == self.opponent for i in range(self.size)):
            return [(i, self.size - 1 - i) for i in range(self.size)]
        return None

    def __str__(self):
        return '\n'.join(' '.join(self.fields[x, y] for x in range(self.size)) for y in range(self.size))

class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.game_mode_var = StringVar()
        self.create_game_mode_selection()
        self.app.mainloop()

    def create_game_mode_selection(self):
        label = Label(self.app, text="Select Game Mode", font=Font(family="Dancing Script", size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        two_players_button = Button(self.app, text='Two Players', command=self.start_two_players_game, font=Font(size=15), width=15, height=3, bd=5, bg='lightpink')
        two_players_button.grid(row=1, column=0, padx=10, pady=10)

        play_with_computer_button = Button(self.app, text='With Computer', command=self.start_computer_game, font=Font(size=15), width=15, height=3, bd=5, bg='lightblue')
        play_with_computer_button.grid(row=1, column=1, padx=10, pady=10)

    def start_two_players_game(self):
        self.app.destroy()
        TwoPlayersGame().mainloop()

    def start_computer_game(self):
        self.app.destroy()
        ComputerGame().mainloop()

class TwoPlayersGame:
    def __init__(self):
        self.app = Tk()
        self.app.title('Tic Tac Toe - Two Players')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.font_size = 40
        self.font = Font(family="Helvetica", size=self.font_size, weight="bold")
        self.buttons = {}
        self.load_sounds()
        self.create_board_buttons()
        self.create_reset_button()
        self.play_game_start_sound()
        self.update()

    def create_board_buttons(self):
        for x, y in self.board.fields:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=4, height=2, bd=5, bg='wheat')
            button.grid(row=y, column=x, sticky="nsew")
            self.buttons[x, y] = button

    def create_reset_button(self):
        handler = lambda: self.reset()
        reset_button = Button(self.app, text='Reset', command=handler, font=self.font, width=10, height=1, bd=5, bg='teal')
        reset_button.grid(row=self.board.size, column=0, columnspan=self.board.size, sticky="we")

    def create_title_label(self):
        title_label = Label(self.app, text="Tic Tac Toe", font=Font(family="Helvetica", size=self.font_size + 2, weight="bold"))
        title_label.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky="we")

    def load_sounds(self):
        pygame.init()
        self.game_start_sound = pygame.mixer.Sound("sounds/start.wav")
        self.button_click_sound = pygame.mixer.Sound("sounds/button-press.wav")
        self.player_win_sound = pygame.mixer.Sound("sounds/win.wav")
        self.board_full_sound = pygame.mixer.Sound("sounds/game-over.wav")

    def play_game_start_sound(self):
        pygame.mixer.Sound.play(self.game_start_sound)

    def play_button_click_sound(self):
        pygame.mixer.Sound.play(self.button_click_sound)

    def play_player_win_sound(self):
        pygame.mixer.Sound.play(self.player_win_sound)

    def play_board_full_sound(self):
        pygame.mixer.Sound.play(self.board_full_sound)

    def reset(self):
        self.board = Board()
        self.play_game_start_sound()
        self.update()

    def move(self, x, y):
      if self.board.fields[x, y] == self.board.empty:
        self.play_button_click_sound()
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.update()
        if self.board.won() or self.board.tied():
            self.end_game()
        else:
            self.player_turn += 1
            self.app.config(cursor="")
            self.update()

    def end_game(self):
        if self.board.won():
            self.play_player_win_sound()
            winner = "Player X" if self.player_turn % 2 == 0 else "Player O"
            messagebox.showinfo("Game Over", f"{winner} wins!")
        elif self.board.tied():
            self.play_board_full_sound()
            messagebox.showinfo("Game Over", "It's a tie!")
        self.reset()

    def update(self):
          for (x, y) in self.board.fields:
              text = self.board.fields[x, y]
              self.buttons[x, y]['text'] = text
              self.buttons[x, y]['disabledforeground'] = 'black'
              if text == self.board.empty:
                  self.buttons[x, y]['state'] = 'normal'
              else:
                  self.buttons[x, y]['state'] = 'disabled'
          winning = self.board.won()
          if winning:
              self.play_player_win_sound()  # Play sound when a player wins
              for x, y in winning:
                  self.buttons[x, y]['disabledforeground'] = 'red'
              for x, y in self.buttons:
                  self.buttons[x, y]['state'] = 'disabled'
              messagebox.showinfo("Game Over", f"Player {self.board.opponent} wins!")
              self.reset()
          elif self.board.tied():
              self.play_board_full_sound()  # Play sound when the board is full
              messagebox.showinfo("Game Over", "It's a tie!")
              self.reset()
          for (x, y) in self.board.fields:
              self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()

class ComputerGame:
    def __init__(self):
        self.app = Tk()
        self.app.title('Tic Tac Toe - Play with Computer')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.font_size = 40
        self.font = Font(family="Helvetica", size=self.font_size, weight="bold")
        self.buttons = {}
        self.load_sounds()
        self.create_board_buttons()
        self.create_reset_button()
        self.play_game_start_sound()
        self.update()

    def create_board_buttons(self):
      for x, y in self.board.fields:
          handler = lambda x=x, y=y: self.move(x, y)
          button = Button(self.app, command=handler, font=self.font, width=4, height=2, bd=5, bg='rosybrown')
          button.grid(row=y, column=x, sticky="nsew")
          self.buttons[x, y] = button

    def create_reset_button(self):
        handler = lambda: self.reset()
        reset_button = Button(self.app, text='Reset', command=handler, font=self.font, width=10, height=1, bd=5,bg='darkcyan')
        reset_button.grid(row=self.board.size, column=0, columnspan=self.board.size, sticky="we")

    def create_title_label(self):
        title_label = Label(self.app, text="Tic Tac Toe", font=Font(family="Helvetica", size=self.font_size + 4, weight="bold"))
        title_label.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky="we")

    def load_sounds(self):
        pygame.init()
        self.game_start_sound = pygame.mixer.Sound("sounds/start.wav")
        self.button_click_sound = pygame.mixer.Sound("sounds/button-press.wav")
        self.player_win_sound = pygame.mixer.Sound("sounds/win.wav")
        self.board_full_sound = pygame.mixer.Sound("sounds/game-over.wav")

    def play_game_start_sound(self):
        pygame.mixer.Sound.play(self.game_start_sound)

    def play_button_click_sound(self):
        pygame.mixer.Sound.play(self.button_click_sound)

    def play_player_win_sound(self):
        pygame.mixer.Sound.play(self.player_win_sound)

    def play_board_full_sound(self):
        pygame.mixer.Sound.play(self.board_full_sound)

    def reset(self):
        self.board = Board()
        self.play_game_start_sound()
        self.update()

    def move(self, x, y):
        if self.board.fields[x, y] == self.board.empty:
            self.play_button_click_sound()  # Play sound when a button is pressed
            self.app.config(cursor="watch")
            self.app.update()
            self.board = self.board.move(x, y)
            self.update()
            move = self.board.best()
            if move:
                self.board = self.board.move(*move)
                self.update()
            self.app.config(cursor="")

    def end_game(self):
        if self.board.won():
            self.play_player_win_sound()
            winner = "Player X" if self.player_turn % 2 == 0 else "Player O"
            messagebox.showinfo("Game Over", f"{winner} wins!")
        elif self.board.tied():
            self.play_board_full_sound()
            messagebox.showinfo("Game Over", "It's a tie!")
        self.reset()

    def update(self):
        for (x, y) in self.board.fields:
            text = self.board.fields[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.board.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = self.board.won()
        if winning:
            self.play_player_win_sound()  # Play sound when a player wins
            for x, y in winning:
                self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
            messagebox.showinfo("Game Over", f"Player {self.board.opponent} wins!")
            self.reset()
        elif self.board.tied():
            self.play_board_full_sound()  # Play sound when the board is full
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset()
        for (x, y) in self.board.fields:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()





if __name__ == '__main__':
    GUI()