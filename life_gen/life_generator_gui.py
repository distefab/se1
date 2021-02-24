from tkinter import *
from life_generator_widgets import *
from life_generator_data import *
from life_generator_debug import log


def start_gui():
    root = Tk()
    root.minsize(500, 500)
    app = Application(master=root)
    app.mainloop()


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.result = None

        self.build_ui()
        self.load()

    # Build

    def build_ui(self):
        self.create_title().pack(side=TOP, padx=50, pady=20)
        Label(self.master, text="Categories:", justify=LEFT).pack(
            side=TOP, anchor="w", padx=50
        )
        self.create_category_selector().pack(
            side=TOP, padx=50, pady=(10, 20), fill=BOTH, expand=True
        )
        self.create_generate_button().pack(side=TOP, padx=50, pady=10)
        Label(self.master, text="Results:", justify=LEFT).pack(
            side=TOP, anchor="w", padx=50
        )
        self.create_output_view().pack(
            side=TOP, padx=50, pady=(10, 10), fill=BOTH, expand=True
        )
        self.create_export_button().pack(side=TOP, anchor="e", padx=50, pady=(0, 50))
        self.create_population_module_frame().pack(side=TOP, padx=50, pady=(0, 50))

    def create_title(self):
        frame = Frame(self.master)
        title = Label(frame, text="Life Generator", font="default 32 bold")
        title.pack(side=TOP)
        subtitle = Label(frame, text="By: Matt Pennington", font="default 10 italic")
        subtitle.pack(side=TOP)
        return frame

    def create_category_selector(self):
        # self.table = ScrollableTable(self.master, width=100, height=100)
        # self.table.pack(side=TOP, padx=50, pady=20, expand=True)
        listbox = FancyListbox(self.master, exportselection=False)
        listbox.on_selection_change = self.selection_did_change
        self.categories_view = listbox
        return listbox

    def create_generate_button(self):
        frame = Frame(self.master)

        label = Label(frame, text="Generate")
        label.pack(side=LEFT)

        countEntry = IntegerEntry(frame, initial=20)
        countEntry.on_value_changed = self.toy_count_did_change
        countEntry.pack(side=LEFT)
        self.countEntry = countEntry

        label = Label(frame, text="results: ")
        label.pack(side=LEFT)

        button = Button(frame, text="GO!", command=self.go_clicked)
        button.pack(side=LEFT)
        self.go_button = button

        return frame

    def create_output_view(self):
        listbox = FancyListbox(self.master)  # , selectmode="multiple")
        self.output_view = listbox
        return listbox

    def create_export_button(self):
        button = Button(self.master, text="Export", command=self.export_clicked)
        self.export_button = button
        return button

    def create_population_module_frame(self):
        frame = Frame(self.master)

        button = Button(
            frame,
            text="Get California Population in 2010:",
            command=self.get_population_clicked,
        )
        button.pack(side=LEFT)

        label = Label(frame, text="")
        label.pack(side=LEFT)
        self.population_label = label

        return frame

    # Data

    def load(self):
        self.load_data()
        self.load_categories()
        self.update_ui()

    def load_data(self):
        self.td = ToyData()
        self.td.load()

        self.pd = PopulationData()

    def load_categories(self):
        self.categories_view.load_items(self.td.categories())

    def load_result(self, result):
        items = list(result.output_item_name)
        self.output_view.load_items(items)

        self.result = result
        self.update_ui()

    def load_population_data(self, result):
        self.population_label["text"] = result

    # Callbacks

    def toy_count_did_change(self, value):
        self.update_ui()

    def selection_did_change(self, event):
        log("Selection changed")
        self.update_ui()

    def go_clicked(self):
        if not self.ready_for_go():
            log("Error: Go clicked, but go not ready.")
            self.update_ui()
            return

        cats = self.categories_view.selected_items()
        count = self.countEntry.int_value()
        categories = [(cat, count) for cat in cats]

        self.td.calc_top_toys_for(categories, self.load_result)

    def export_clicked(self):
        if self.result is None:
            log("Error: No result to export.")
            self.update_ui()
            return

        # TODO: GUI prompt
        # if path.exists(OUTPUT_FILE):
        #     if not user_confirm_action('File "output.csv" already exists. Overwrite?'):
        #         log("Aborting.")
        #         return

        self.td.export(self.result)
        log("Export clicked.")

    def get_population_clicked(self):
        self.pd.get_data_as_string(self.load_population_data)

    # Helpers

    def selection_valid(self):
        selected = self.categories_view.curselection()
        return selected and len(selected) > 0

    def count_valid(self):
        value = self.countEntry.int_value()
        return value and value > 0

    def ready_for_go(self):
        return self.selection_valid() and self.count_valid()

    def ready_for_export(self):
        return self.result is not None and not self.result.empty

    def update_ui(self):
        self.go_button["state"] = NORMAL if self.ready_for_go() else DISABLED
        self.export_button["state"] = NORMAL if self.ready_for_export() else DISABLED