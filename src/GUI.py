from tkinter import *
from util.FileHandler import FileHandler


class GUI:

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

        # text area widget
        self.textContent = Text(self.textFrame, font='Arial')
        self.textContent.grid(row=4, column=0, padx=25, pady=25, sticky=NSEW)

        self.config = None
        self.data = None

    def create_menus(self):
        """
        create pull-down menus, and add it to the menu bar
        """
        # menu File
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load config", command=self.load_config_file)
        file_menu.add_command(label="Load data directory", command=self.load_data_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

    def load_config_file(self):
        """
        ask user to input the init file and initialise the config
        :return: None
        """
        self.config = FileHandler(self.master).open_init_file()

    def load_data_directory(self):
        """
        ask user to input the data directory and proceed the calculate
        :return: None
        """
        data = FileHandler(self.master).open_data_directory()
        heuristique = self.calculate_heuristique(data)
        # print(heuristique)
        for trajets in heuristique:
            self.textContent.insert(END, '{\n')
            for trajet in trajets:
                self.textContent.insert(END, '\t[')
                for cord in trajet:
                    self.textContent.insert(END, cord+' ')
                self.textContent.insert(END, '], ')
            self.textContent.insert(END, '\n}\n')

    def calculate_heuristique(self, data_set):
        """
        Calculer les trajets du vhéhicule electrique
        :param data_set: a dictionary of all data
        :return: a list of trajet
        """
        newVehicle = True
        lastDemande = 0
        trajets = []
        totalDist = 0
        totalCapacity = 0
        totalTime = self.config.start_time
        while lastDemande < len(data_set['demands']):
            next_total_dist = totalDist + \
                              data_set['distances'][lastDemande][lastDemande+1] + \
                              data_set['distances'][0][lastDemande+1]
            next_total_capacity = totalCapacity + data_set['demands'][lastDemande]
            next_total_time = totalTime + data_set['times'][lastDemande][lastDemande+1]
            if newVehicle:
                totalDist = 0
                totalCapacity = 0
                totalTime = self.config.start_time
                trajet = []
                trajet.append(data_set['coordinates'][0].tolist())
            if next_total_dist <= self.config.max_dist and \
                    next_total_capacity <= self.config.capacity and \
                    next_total_time <= self.config.end_time:
                trajet.append(data_set['coordinates'][lastDemande+1].tolist())
                # print(trajet)
                totalDist += data_set['distances'][lastDemande][lastDemande+1]
                totalCapacity += data_set['demands'][lastDemande]
                totalTime += data_set['times'][lastDemande][lastDemande+1]
                newVehicle = False
                lastDemande += 1
            else:
                newVehicle = True
                trajets.append(trajet)
        trajets.append(trajet)
        return trajets
