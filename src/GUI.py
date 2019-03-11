from tkinter import *
from util.FileHandler import FileHandler


class GUI:

    colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']

    def __init__(self, master):
        self.master = master
        self.master.title("Livraison avec des véhicules électrics")

        # Menu
        self.menu_bar = Menu(self.master)
        self.create_menus()

        # main frame
        self.frame = Frame(self.master, relief=SUNKEN, bg="red", width=self.master.winfo_width())
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack(fill=None, expand=False)

        # canvas to put image
        self.canvas = Canvas(self.frame, bg="light gray", bd=0,
                             height=(self.master.winfo_height()-250),
                             width=(self.master.winfo_width()-100))
        self.canvas.grid(row=1, column=0, sticky=NSEW)
        self.canvas.config(state=DISABLED)

        # Frame to put text
        self.textFrame = Frame(self.frame, relief=SUNKEN, bg=self.master.cget('bg'),
                               width=(self.master.winfo_width()),
                               height=(self.master.winfo_height()-int(self.canvas['height'])-50))
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textFrame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.textFrame.grid_propagate(False)

    def create_menus(self):
        """
        create pull-down menus, and add it to the menu bar
        """
        # menu File
        file_menu = Menu(self.menu_bar, tearoff=0)
        #file_menu.add_command(label="New Image", command=self.open_file)
        #file_menu.add_command(label="Save Data", command=self.save_to)
        file_menu.add_command(label="Load matrix data", command=self.load_matrix_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

    def load_matrix_data(self):
        my_file_handler = FileHandler(self.master)
        content = my_file_handler.load_file()
        if my_file_handler.file_extension:
            return
            # self.print_matrix(content, my_file_handler.file_extension)
