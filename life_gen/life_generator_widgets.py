from tkinter import *
from life_generator_debug import log


class FancyListbox(Listbox):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack(side=LEFT)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        self.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)

        self.on_selection_change = None
        self.bind("<<ListboxSelect>>", self.selection_did_change)

    def selection_did_change(self, event):
        if self.on_selection_change:
            self.on_selection_change(event)

    def load_items(self, items):
        self.items = items
        self.delete(0, END)
        for i, item in enumerate(items):
            self.insert(END, item)
            self.itemconfig(i)

    def selected_items(self):
        return [self.items[i] for i in self.curselection()]


class IntegerEntry(Entry):
    def __init__(self, master=None, initial=0, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.initial = initial

        self.on_value_changed = None

        self.build()

    def build(self):
        self.binding = StringVar(value=self.initial)
        self.binding.trace_add("write", self.value_did_change)
        validator = self.master.register(self.should_change_text)
        self.config(
            width=3,
            textvariable=self.binding,
            validate="key",
            validatecommand=(validator, "%P"),
        )

    def int_value(self):
        try:
            return int(self.binding.get())
        except:
            return None

    # Entry value changed
    def value_did_change(self, var, index, mode):
        # strip whitespace
        self.binding.set(self.binding.get().strip())
        # call callback
        if self.on_value_changed:
            self.on_value_changed(self.int_value())

    # Ensure value is a positive integer, or empty
    def should_change_text(self, value_if_allowed):
        if value_if_allowed:
            try:
                value = int(value_if_allowed)
                log(f"Valid: {0 if value == 0 else True}")
                return value >= 0
            except:
                log(f"Valid: False")
                return False
        else:
            log(f"Valid: Empty")
            return True
