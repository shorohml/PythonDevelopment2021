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
            grid_info = button.grid_info()
            row = i//4 + 1
            col = i%4
            if grid_info['row'] != row or grid_info['column'] != col:
                return False
        return True

    def shuffleButtons(self):
        buttons_idx = list(range(16))
        shuffle(buttons_idx)
        self.empty_pos = [
            buttons_idx[-1]//4 + 1,
            buttons_idx[-1]%4
        ]
        for i in range(15):
            self.numButtons[i].grid(
                row=buttons_idx[i]//4 + 1,
                column=buttons_idx[i]%4,
                sticky='nsew'
            )

    def moveButton(self, i):
        '''move button to emty position (if possible)'''
        grid_info = self.numButtons[i].grid_info()
        row, col = grid_info['row'], grid_info['column']
        flag_1 = self.empty_pos[1] == col and (self.empty_pos[0] == row - 1 or self.empty_pos[0] == row + 1)
        flag_2 = self.empty_pos[0] == row and (self.empty_pos[1] == col - 1 or self.empty_pos[1] == col + 1)
        if flag_1 or flag_2:
            self.numButtons[i].grid(
                row=self.empty_pos[0],
                column=self.empty_pos[1],
                sticky='nsew'
            )
            self.empty_pos[0] = row
            self.empty_pos[1] = col

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
        for i in range(15):

            def command(j=i):
                self.moveButton(j)
                # check if player've won
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
