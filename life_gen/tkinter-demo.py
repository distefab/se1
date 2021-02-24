from tkinter import *

# Tkinter Docs https://docs.python.org/3/library/tkinter.html
## Packer Options https://docs.python.org/3/library/tkinter.html#packer-options
## Data Types https://docs.python.org/3/library/tkinter.html#tk-option-data-typeS
## Bindings and Events https://docs.python.org/3/library/tkinter.html#bindings-and-events


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()
        self.create_fred()
        self.create_entry_thingy()

    # 3 ways to set options on a widget
    # Note: methods on each widget are described in tkinter/__init__.py
    #   Alternatively, use keys() method or call config() with no arguments
    def create_widgets(self):
        # dict indicies
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        # config method
        self.label = Label(self)
        self.label.config(text="I'm a label.")
        self.label.pack(side="top")

        # initializer
        self.quit = Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("Hi there, everyone!")

    # Packer - geometry manager
    def create_fred(self):
        self.fred = Button(text="Fred")
        self.fred.pack()  # defaults to side = "top"
        self.fred.pack(side="left")
        self.fred.pack(expand=1)  # 0 or 1

        # anchor
        #     Anchor type. Denotes where the packer is to place each slave in its parcel.
        # expand
        #     Boolean, 0 or 1.
        # fill
        #     Legal values: 'x', 'y', 'both', 'none'.
        # ipadx and ipady
        #     A distance - designating internal padding on each side of the slave widget.
        # padx and pady
        #     A distance - designating external padding on each side of the slave widget.
        # side
        #     Legal values are: 'left', 'right', 'top', 'bottom'.

    # Value Bindings
    def create_entry_thingy(self):
        self.entrythingy = Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind("<Key-Return>", self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:", self.contents.get())

    # File Handlers
    # Note: The file argument may either be an object with a fileno() method (such as a file or
    #   socket object), or an integer file descriptor.
    def create_filehandler(self):
        mask = READABLE | WRITABLE
        self.master.tk.createfilehandler(file, mask, self.file_done)

        self.master.tk.deletefilehandler(file)

    def file_done(self):
        print("File done.")


if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.mainloop()