"Graph Edit"
from typing import Set

import tkinter as tk


class Application(tk.Frame):  # pylint: disable=too-many-ancestors
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky='NEWS')
        self.createWidgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def createWidgets(self):
        '''Create all the widgets'''


class GraphEdit(Application):

    def __init__(self, known_names: Set[str], **kwargs):
        super().__init__(**kwargs)
        self.__known_names = known_names
        self.__previous = (0, 0)
        self.__created_oval = False
        self.__selected_id = 0
        self.__moving = False

    def clearCanvas(self):
        self.C.delete("all")

    def addTag(self, newTag: str, lineIdx: int, length: int):
        oldTag = ''
        if newTag == 'good':
            oldTag = 'bad'
        elif newTag == 'bad':
            oldTag = 'good'
        else:
            return
        self.T.tag_remove(
            oldTag,
            f'{lineIdx}.0',
            f'{lineIdx}.0 + {length} chars'
        )
        self.T.tag_add(
            newTag,
            f'{lineIdx}.0',
            f'{lineIdx}.0 + {length} chars'
        )

    def cclToCanvas(self):
        self.clearCanvas()
        cclProgram = self.T.get('1.0', tk.END)
        for i, line in enumerate(cclProgram.split('\n')):
            lineStrip = line.lstrip()
            if not lineStrip:
                continue
            if lineStrip.startswith('#'):
                self.addTag('good', i + 1, len(line))
                continue
            name, *parameters = line.split()
            if name not in self.__known_names or len(parameters) != 7:
                self.addTag('bad', i + 1, len(line))
                continue
            *coords, width, outline, fill = parameters
            try:
                x0, y0, x1, y1 = (float(coord) for coord in coords)
                width = float(width)
                contructor = getattr(self.C, f'create_{name}')
                contructor(
                    x0, y0, x1, y1,
                    width=width,
                    outline=outline,
                    fill=fill,
                )
                self.addTag('good', i + 1, len(line))
            except:
                self.addTag('bad', i + 1, len(line))

    def canvasToCCL(self):
        objIds = self.C.find_all()
        lengths = []
        text = ''
        for objId in objIds:
            coords = (str(coord) for coord in self.C.coords(objId))
            config = self.C.itemconfigure(objId)
            width = config['width'][-1]
            outline = config['outline'][-1]
            fill = config['fill'][-1]
            line = 'oval ' + ' '.join(coords) + f' {width} {outline} {fill}\n'
            text += line
            lengths.append(len(line))
        self.T.delete('1.0', 'end')
        self.T.insert('end', text)
        for i, length in enumerate(lengths):
            self.addTag('good', i + 1, length)

    def select(self, event):
        overlapping = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        self.__previous = (event.x, event.y)
        if not overlapping:
            self.__selected_id = self.C.create_oval(
                event.x, event.y, event.x, event.y,
                width=2,
                outline='blue',
                fill='red',
            )
            self.__created_oval = True
        else:
            self.__selected_id = overlapping[-1]
            self.__moving = True

    def move(self, event):
        if self.__created_oval:
            self.C.coords(
                self.__selected_id,
                self.__previous[0],
                self.__previous[1],
                event.x,
                event.y
            )
        elif self.__moving:
            self.C.move(
                self.__selected_id,
                event.x - self.__previous[0],
                event.y - self.__previous[1]
            )
            self.__previous = (event.x, event.y)

    def release(self, event):
        self.__created_oval = False
        self.__moving = False

    def createWidgets(self):
        super().createWidgets()
        self.T = tk.Text(
            self,
            undo=True,
            font='fixed',
            inactiveselectbackground='Midnightblue'
        )
        self.T.tag_configure('good', foreground='green')
        self.T.tag_configure('bad', foreground='red')
        self.C = tk.Canvas(self)
        self.C.bind("<Button-1>", self.select)
        self.C.bind("<B1-Motion>", self.move)
        self.C.bind("<B1-ButtonRelease>", self.release)
        self.T.grid(row=1, column=1, sticky='NEWS', columnspan=2)
        self.C.grid(row=1, column=3, sticky='NEWS')

        self.RunButton = tk.Button(self, text='Text2Canvas', command=self.cclToCanvas)
        self.LoadButton = tk.Button(self, text='Canvas2Text', command=self.canvasToCCL)
        self.Q = tk.Button(self, text='Quit', command=self.master.quit)
        self.RunButton.grid(row=2, column=1)
        self.LoadButton.grid(row=2, column=2)
        self.Q.grid(row=2, column=3)


app = GraphEdit(
    title="Graph Edit",
    known_names={
        'oval',
    }
)
app.mainloop()
