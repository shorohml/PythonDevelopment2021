import tkinter as tk
from random import shuffle


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        # set rows/columns weights to make interface stretchable
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, minsize=30)
        for i in range(4):
            self.rowconfigure(i + 1, weight=1, minsize=30)
            self.columnconfigure(i, weight=1, minsize=60)

        # create New button
        self.newButton = tk.Button(self, text='New')
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
        buttons_idx = list(range(16))
        shuffle(buttons_idx)
        self.numButtons = [None]*15
        empty_pos = [
            buttons_idx[-1]//4 + 1,
            buttons_idx[-1]%4
        ]
        for i in range(15):

            def command(j=i):
                # move button to emty position if possible
                grid_info = self.numButtons[j].grid_info()
                row, col = grid_info['row'], grid_info['column']
                flag_1 = empty_pos[1] == col and (empty_pos[0] == row - 1 or empty_pos[0] == row + 1)
                flag_2 = empty_pos[0] == row and (empty_pos[1] == col - 1 or empty_pos[1] == col + 1)
                if flag_1 or flag_2:
                    self.numButtons[j].grid(
                        row=empty_pos[0],
                        column=empty_pos[1],
                        sticky='nsew'
                    )
                    empty_pos[0] = row
                    empty_pos[1] = col

            self.numButtons[i] = tk.Button(
                self,
                text=f'{i + 1}',
                command=command,
            )
            self.numButtons[i].grid(
                row=buttons_idx[i]//4 + 1,
                column=buttons_idx[i]%4,
                sticky='nsew'
            )


if __name__ == '__main__':
    app = Application()
    app.master.title('15')
    app.mainloop()
