"15 puzzle with simple GUI"
import tkinter as tk
from random import shuffle
from tkinter import messagebox
from typing import List


def isSolvable(buttonsIdx: List[int]) -> bool:
    """
    Check if puzzle with given buttons order is solvable.

    :param buttonsIdx: list with position index for each button and empty cell
    :returns: True if solvable, False if not
    """
    ranking = [None]*16
    for i in range(15):
        ranking[buttonsIdx[i]] = i
    nSum = 0
    for i in range(15):
        if ranking[i] is None:
            nSum += i//4 + 1
            continue
        for j in range(i + 1, 16):
            if ranking[j] is None:
                continue
            if ranking[j] < ranking[i]:
                nSum += 1
    return nSum % 2 == 0


def rotate90(buttonsIdx: List[int]) -> List[int]:
    """
    Rotate puzzle by 90 degrees counterclockwise.

    :param buttonsIdx: list with position index for each button and empty cell
    :returns: list with positions after rotation
    """
    newButtonsIdx = []
    for i in buttonsIdx:
        row, col = i//4, i%4
        newCol = row
        newRow = 3 - col
        newButtonsIdx.append(newRow*4 + newCol)
    return newButtonsIdx


class Application(tk.Frame): # pylint: disable=too-many-ancestors

    "Game application"

    def __init__(self, master=None):
        super().__init__(master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky='nsew')
        self.createWidgets()

    def checkWinning(self) -> bool:
        """
        Check if player have won.

        :returns: True if puzzle is solved, False otherwise
        """
        for i, button in enumerate(self.numButtons):
            gridInfo = button.grid_info()
            row = i//4 + 1
            col = i%4
            if gridInfo['row'] != row or gridInfo['column'] != col:
                return False
        return True

    def shuffleButtons(self):
        """
        Shuffle buttons with numbers.
        """
        # create list with position for each button and empty cell
        buttonsIdx = list(range(16))
        shuffle(buttonsIdx)
        if not isSolvable(buttonsIdx):
            buttonsIdx = rotate90(buttonsIdx)
        for i in range(15):
            self.numButtons[i].grid(
                row=buttonsIdx[i]//4 + 1,
                column=buttonsIdx[i]%4,
                sticky='nsew'
            )
        self.emptyPos[0] = buttonsIdx[-1]//4 + 1
        self.emptyPos[1] = buttonsIdx[-1]%4

    def moveButton(self, i):
        """
        Move button to empty position (if possible).

        :param i: number of the butoon to move
        """
        gridInfo = self.numButtons[i].grid_info()
        row, col = gridInfo['row'], gridInfo['column']
        # if button is adjustent to empty cell, move it to empty cell
        adjPos = {
            (row, col - 1),
            (row, col + 1),
            (row - 1, col),
            (row + 1, col),
        }
        if tuple(self.emptyPos) in adjPos:
            self.numButtons[i].grid(
                row=self.emptyPos[0],
                column=self.emptyPos[1],
                sticky='nsew'
            )
            self.emptyPos[0] = row
            self.emptyPos[1] = col

    def createWidgets(self):
        """
        Create application widgets.
        """
        # set rows/columns weights to make stretchable interface
        self.rowconfigure(0)
        for i in range(4):
            self.rowconfigure(i + 1, weight=1)
            self.columnconfigure(i, weight=1)

        # create New button
        self.newButton = tk.Button(self, text='New', command=self.shuffleButtons)
        self.newButton.grid(
            row=0,
            column=0,
            columnspan=2,
        )

        # create Exit button
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)
        self.quitButton.grid(
            row=0,
            column=2,
            columnspan=2,
        )

        # create buttons with numbers for game logic
        self.numButtons = [None]*15
        self.emptyPos = [4, 3]
        for i in range(15):

            def command(j=i):
                self.moveButton(j)
                # check if player have won
                if self.checkWinning():
                    messagebox.showinfo(message='You win!')
                    self.shuffleButtons()

            self.numButtons[i] = tk.Button(
                self,
                text=f'{i + 1}',
                command=command,
                width=7,
            )
            self.numButtons[i].grid(
                row=i//4 + 1,
                column=i%4,
                sticky='nsew'
            )
        self.shuffleButtons()


if __name__ == '__main__':
    app = Application()
    app.master.title('15')
    app.mainloop()
