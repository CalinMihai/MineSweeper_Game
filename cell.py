from tkinter import Button, Label
import random
import math
import ctypes
import sys

import settings


class Cell:
    all = []
    cell_count_label_obj = None
    cell_count = settings.CELL_COUNT

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_mine_candidate = False
        self.is_opened = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left:{Cell.cell_count}",
            width=12,
            height=4,
            font=("", 30)
        )
        Cell.cell_count_label_obj = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_lenght == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
                    # Cancel Left and Right Click events if the cell was opened:
                    cell_obj.cell_btn_object.unbind('<Button-1>')
                    cell_obj.cell_btn_object.unbind('<Button-3>')
            self.show_cell()
            # If Mines count equals to the cell left count, player Won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0, "Congratulations! You won the game!", "Game Over", 0
                )

        # Cancel Left and Right Click events if the cell was opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')



    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg="orange"
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg="SystemButtonFace"
            )
            self.is_mine_candidate = False

    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(
            0, "You clicked on a mine!", "Game Over", 0
        )
        sys.exit()

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_lenght)
            # Replace the text of the cell label with the newer count
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this was a mine candidate, then change color to default
            self.cell_btn_object.configure(
                bg="SystemButtonFace"
            )
        # Mark the cell as opened( use this as the last line of the method)
        self.is_opened = True

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_lenght(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cells in picked_cells:
            picked_cells.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
