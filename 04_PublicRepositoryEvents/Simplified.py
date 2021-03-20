"Simplified"
import tkinter as tk
from tkinter.messagebox import showinfo


def detachLastVal(s: str, sep: str, valType=str, default=''):
    tokens = s.split(sep)
    val = default
    if len(tokens) > 1:
        s = sep.join(tokens[:-1])
        val = valType(tokens[-1])
    return s, val


def parseRowColumnInfo(geom: str):
    geom, widthOrHeight = detachLastVal(geom, '+', int, 0)
    geom, weight = detachLastVal(geom, '.', int, 1)
    return int(geom), weight, widthOrHeight


def parseGeom(geom: str):
    geom, gravity = detachLastVal(geom, '/', str, 'NEWS')

    rowColumn = geom.split(':')
    if len(rowColumn) != 2:
        raise ValueError('Row or column info missing')

    return parseRowColumnInfo(rowColumn[0]), parseRowColumnInfo(rowColumn[1]), gravity


class Application(tk.Frame): # pylint: disable=too-many-ancestors

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.widgets = {}
        self.createWidgets()

    def __getattr__(self, name: str):
        widgets = self.widgets
        if name in widgets:
            return widgets[name]

        def get_contructor(master=self, name=name):

            def constructor(WidgetType, geom: str, **kwargs):

                class MyWidgetType(WidgetType):

                    def __getattr__(self, newName):
                        newName = name + '.' + newName
                        if newName in widgets:
                            return widgets[name]
                        return get_contructor(master=self, name=newName)

                (row, rowWeight, height), (column, columnWeight, width), gravity = parseGeom(geom)

                master.rowconfigure(row, weigh=rowWeight)
                master.columnconfigure(column, weigh=columnWeight)

                widget = MyWidgetType(master, **kwargs)
                widget.grid(
                    row=row,
                    column=column,
                    sticky=gravity,
                    rowspan=height+1,
                    columnspan=width+1,
                )
                widgets[name] = widget
                return widget

            return constructor

        return get_contructor(name=name)

    def createWidgets(self):
        '''Create all the widgets'''


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()