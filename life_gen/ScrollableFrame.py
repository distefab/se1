import tkinter as tk
from tkinter import ttk

# Based on: https://blog.tecladocode.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, width=1000, height=500)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas = canvas
        self.scrollbar = scrollbar

    def _bind_mousewheel(self, e):
        print("Binding...")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, e):
        print("Unbinding...")
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        print(f"Mousewheel event: num:{event.num} delta:{event.delta}")
        # respond to Linux or Windows wheel event
        # self.canvas.yview_scroll(int(event), "units")
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # if event.num == 5 or event.delta == -120:
        #     self.canvas.yview_scroll(int(event), "units")
        #     self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # if event.num == 4 or event.delta == 120:
        #     self.canvas.yview_scroll(int(event), "units")
        #     self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# My own


class Table(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.build()

    # def build_old(self, width, height):
    #     frame = Frame(self.master)
    #     frame.pack()

    #     self.box = Listbox(frame, width=width, height=height)
    #     self.box.pack(side=LEFT, fill=BOTH, expand=1)

    #     scrollbar = Scrollbar(frame, command=self.box.yview)
    #     self.box["yscrollcommand"] = scrollbar.set
    #     scrollbar.pack(side=RIGHT, fill=BOTH)

    # def load_old(self, df):
    #     for row in df:
    #         self.box.insert(END, row)

    def build(self):
        self.frame = Frame(self.master)
        self.frame.pack(expand=True)

    def load(self, array):
        for i, item in enumerate(array):
            label = Label(self.frame, text=i, justify=LEFT)
            label.grid(row=i, column=0)

            label = Label(self.frame, text=item, justify=LEFT)
            label.grid(row=i, column=1)

    def load2(self, data):
        for c, key in enumerate(data):
            label = Label(self.frame, text=key)
            label.grid(row=0, column=c)

        for r, row in data:
            for c, key in enumerate(items):
                label = Label(self.frame, text=row[key])
                label.grid(row=r + 1, column=c)

            # labels.append(Label(self.frame, text=r))
            # labels.append(Label(self.frame, text=row["uniq_id"]))
            # labels.append(
            #     Label(self.frame, text=row["amazon_category_and_sub_category"])
            # )
            # labels.append(Label(self.frame, text=row["product_name"]))

            # for c, label in enumerate(labels):
            #     label.grid(row=r + 1, column=c)

            if r > 30:
                break


class ScrollableTable(Table):
    def build(self):
        frame = ScrollableFrame(self.master)
        frame.pack(expand=True)
        self.frame = frame.scrollable_frame