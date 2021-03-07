import tkinter as tk
from tkinter import messagebox
from random import shuffle


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def checkWinning(self):
        for i, button in enumerate(self.numButtons):
            gridInfo = button.grid_info()
            row = i//4 + 1
            col = i%4
            if gridInfo['row'] != row or gridInfo['column'] != col:
                return False
        return True

    def shuffleButtons(self):
        buttonsIdx = list(range(16))
        shuffle(buttonsIdx)
        for i in range(15):
            self.numButtons[i].grid(
                row=buttonsIdx[i]//4 + 1,
                column=buttonsIdx[i]%4,
                sticky='nsew'
            )
        self.emptyPos[0] = buttonsIdx[-1]//4 + 1
        self.emptyPos[1] = buttonsIdx[-1]%4

    def moveButton(self, i):
        '''move button to emty position (if possible)'''
        gridInfo = self.numButtons[i].grid_info()
        row, col = gridInfo['row'], gridInfo['column']
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
        # set rows/columns weights to make stretchable interface
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, minsize=30)
        for i in range(4):
            self.rowconfigure(i + 1, weight=1, minsize=30)
            self.columnconfigure(i, weight=1, minsize=60)

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
            )
        self.shuffleButtons()


if __name__ == '__main__':
    app = Application()
    app.master.title('15')
    app.mainloop()
