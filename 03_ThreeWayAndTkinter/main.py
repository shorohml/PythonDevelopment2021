import tkinter as tk


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
        for i in range(4):
            self.rowconfigure(i + 1, weight=1)
            self.columnconfigure(i, weight=1)

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
        self.numButtons = []
        for i in range(15):
            self.numButtons.append(tk.Button(self, text=f'{i + 1}'))
            self.numButtons[-1].grid(
                row=i//4 + 1,
                column=i%4,
                sticky='nsew'
            )


if __name__ == '__main__':
    app = Application()
    app.master.title('15')
    app.mainloop()
