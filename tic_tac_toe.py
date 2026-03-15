import tkinter as tk


class TicTacToeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Neon Tic-Tac-Toe")
        self.root.geometry("760x880")
        self.root.minsize(680, 820)
        self.root.configure(bg="#09111f")

        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.score = {"X": 0, "O": 0, "Draws": 0}

        self.title_font = ("Avenir Next", 28, "bold")
        self.subtitle_font = ("Avenir Next", 13)
        self.score_font = ("Avenir Next", 12, "bold")
        self.button_font = ("Avenir Next", 34, "bold")
        self.status_font = ("Avenir Next", 17, "bold")

        self._build_ui()
        self.update_status("Ход игрока X")

    def _build_ui(self) -> None:
        self.canvas = tk.Canvas(
            self.root,
            bg="#09111f",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw_background)

        self.container = tk.Frame(self.canvas, bg="#09111f")
        self.canvas.create_window((0, 0), window=self.container, anchor="nw", relwidth=1, relheight=1)

        hero = tk.Frame(self.container, bg="#0c1628", padx=28, pady=24)
        hero.pack(fill="x", padx=28, pady=(28, 18))

        tk.Label(
            hero,
            text="Крестики-нолики",
            fg="#f4f7fb",
            bg="#0c1628",
            font=self.title_font,
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Минималистичный неоновый интерфейс на Python и tkinter",
            fg="#9ab0c9",
            bg="#0c1628",
            font=self.subtitle_font,
        ).pack(anchor="w", pady=(8, 0))

        self.status_label = tk.Label(
            hero,
            text="",
            fg="#8be9fd",
            bg="#0c1628",
            font=self.status_font,
        )
        self.status_label.pack(anchor="w", pady=(18, 0))

        scoreboard = tk.Frame(self.container, bg="#09111f")
        scoreboard.pack(fill="x", padx=28)

        self.score_labels = {}
        cards = (
            ("Игрок X", "X", "#32d1ff"),
            ("Игрок O", "O", "#ff6ba9"),
            ("Ничьи", "Draws", "#f8d66d"),
        )
        for title, key, color in cards:
            card = tk.Frame(scoreboard, bg="#122033", padx=20, pady=18)
            card.pack(side="left", expand=True, fill="x", padx=8, pady=(0, 20))

            tk.Label(
                card,
                text=title,
                fg="#9ab0c9",
                bg="#122033",
                font=self.subtitle_font,
            ).pack(anchor="w")

            value = tk.Label(
                card,
                text="0",
                fg=color,
                bg="#122033",
                font=("Avenir Next", 24, "bold"),
            )
            value.pack(anchor="w", pady=(10, 0))
            self.score_labels[key] = value

        board_shell = tk.Frame(self.container, bg="#09111f")
        board_shell.pack(fill="both", expand=True, padx=28, pady=(6, 20))

        board_frame = tk.Frame(board_shell, bg="#0f1b2d", padx=18, pady=18)
        board_frame.pack(expand=True)

        self.buttons = []
        for row in range(3):
            board_frame.grid_rowconfigure(row, weight=1)
            board_frame.grid_columnconfigure(row, weight=1)

        for index in range(9):
            button = tk.Button(
                board_frame,
                text="",
                command=lambda idx=index: self.handle_move(idx),
                width=4,
                height=2,
                font=self.button_font,
                fg="#f4f7fb",
                bg="#14243a",
                activebackground="#1b3250",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                highlightthickness=0,
                cursor="hand2",
            )
            row, col = divmod(index, 3)
            button.grid(row=row, column=col, padx=10, pady=10, ipadx=18, ipady=20, sticky="nsew")
            self.buttons.append(button)

        controls = tk.Frame(self.container, bg="#09111f")
        controls.pack(fill="x", padx=28, pady=(0, 28))

        self._make_action_button(controls, "Новая партия", self.reset_board, "#32d1ff", "#071520").pack(
            side="left", expand=True, fill="x", padx=(0, 10)
        )
        self._make_action_button(controls, "Сбросить счёт", self.reset_scores, "#ff6ba9", "#220b18").pack(
            side="left", expand=True, fill="x", padx=(10, 0)
        )

    def _make_action_button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        foreground: str,
        background: str,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=self.score_font,
            fg=foreground,
            bg=background,
            activebackground=background,
            activeforeground=foreground,
            bd=0,
            relief="flat",
            padx=14,
            pady=16,
            cursor="hand2",
            highlightthickness=0,
        )

    def _draw_background(self, event: tk.Event) -> None:
        self.canvas.delete("bg")
        width = event.width
        height = event.height

        self.canvas.create_rectangle(0, 0, width, height, fill="#09111f", outline="", tags="bg")
        self.canvas.create_oval(-120, -80, 280, 260, fill="#0f2b4a", outline="", tags="bg")
        self.canvas.create_oval(width - 260, 80, width + 120, 420, fill="#30152f", outline="", tags="bg")
        self.canvas.create_oval(80, height - 260, 360, height + 40, fill="#12263a", outline="", tags="bg")
        self.canvas.tag_lower("bg")

    def handle_move(self, index: int) -> None:
        if self.game_over or self.board[index]:
            return

        self.board[index] = self.current_player
        self.buttons[index].configure(
            text=self.current_player,
            fg="#32d1ff" if self.current_player == "X" else "#ff6ba9",
        )

        winner, combination = self.check_winner()
        if winner:
            self.game_over = True
            self.score[winner] += 1
            self._refresh_score()
            self.highlight_winner(combination)
            self.update_status(f"Победил игрок {winner}")
            return

        if all(cell for cell in self.board):
            self.game_over = True
            self.score["Draws"] += 1
            self._refresh_score()
            self.update_status("Ничья. Отличная битва!")
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status(f"Ход игрока {self.current_player}")

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in winning_combinations:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a, b, c)
        return None, None

    def highlight_winner(self, combination) -> None:
        for index in combination:
            self.buttons[index].configure(bg="#1f3f33", activebackground="#1f3f33")

    def update_status(self, text: str) -> None:
        self.status_label.configure(text=text)

    def reset_board(self) -> None:
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        for button in self.buttons:
            button.configure(text="", bg="#14243a", activebackground="#1b3250")
        self.update_status("Ход игрока X")

    def reset_scores(self) -> None:
        self.score = {"X": 0, "O": 0, "Draws": 0}
        self._refresh_score()
        self.reset_board()

    def _refresh_score(self) -> None:
        for key, label in self.score_labels.items():
            label.configure(text=str(self.score[key]))


def main() -> None:
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
