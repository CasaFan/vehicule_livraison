from tkinter import *
from util.FileHandler import FileHandler
from src.modele.BrowserFrame import BrowserFrame
from src.modele.Heuristic import Heuristic
from exceptions.InvalidVariableError import InvalidVariableError
import folium


class GUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Livraison avec des véhicules électrics")

        # Menu
        self.menu_bar = Menu(self.master)
        self.create_menus()

        # main frame
        self.frame = Frame(self.master, relief=SUNKEN, width=self.master.winfo_width())
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.browser_frame = Frame(self.frame, height=self.master.winfo_height()-250, width=self.master.winfo_width()-100)
        #BrowserFrame(self.frame, self.master.winfo_height()-250, self.master.winfo_width()-100)
        self.browser_frame.grid(row=1, column=0, sticky=NSEW)
        self.frame.pack(fill=None, expand=False)
        
        # Frame to put text
        self.textFrame = Frame(self.frame, relief=SUNKEN, bg=self.master.cget('bg'),
                               width=(self.master.winfo_width()),
                               height=(self.master.winfo_height()-int(self.browser_frame['height'])-50))
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textFrame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.textFrame.grid_propagate(False)

        # text area widget
        self.textContent = Text(self.textFrame, font='Arial')
        self.textContent.grid(row=4, column=0, padx=25, pady=25, sticky=NSEW)

        self.config = None
        self.data = None
        self.mode_heuristique = 1

    def create_menus(self):
        """
        create pull-down menus, and add it to the menu bar
        """
        # menu File
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load config file", command=self.load_config_file)
        file_menu.add_command(label="Load data directory", command=self.load_data_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        heuristique_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Heuristique Mode", menu=heuristique_menu)
        heuristique_menu.add_command(label="Deterministe exhaustive", command=self.set_mode_heuristique(1))
        heuristique_menu.add_command(label="Non deterministe exhaustive", command=self.set_mode_heuristique(2))
        heuristique_menu.add_command(label="Deterministe non exhaustive", command=self.set_mode_heuristique(3))
        heuristique_menu.add_command(label="Non deterministe non exhaustive", command=self.set_mode_heuristique(4))
        self.master.config(menu=self.menu_bar)

    def load_config_file(self):
        """
        ask user to input the init file and initialise the config
        :return:
        """
        self.config = FileHandler(self.master).open_init_file()

    def load_data_directory(self):
        """
        ask user to input the data directory and proceed the calculate
        :return:
        """
        coordinate_dict = dict()
        self.data = FileHandler(self.master).open_data_directory()
        try:
            heuristique = self.calculate_heuristique(self.data)
        except InvalidVariableError as err:
            print(err.message)

        for trajets in heuristique:
            self.textContent.insert(END, 'Véhicule '+str(trajets['vehicule']))
            coordinate_list = list()
            for indice, coordinate in enumerate(trajets['coordonees']):
                coordinate_list.append(list(map(float, coordinate.tolist())))
                #self.textContent.insert(END, '('+', '.join(str(e) for e in coordinate.tolist()) + '), ')
            coordinate_dict[trajets['vehicule']] = coordinate_list
            self.textContent.insert(END, '\n')

        self.load_map_lyon_with_markers(coordinate_dict)
        self.browser_frame = BrowserFrame(self.frame, self.master.winfo_height()-250, self.master.winfo_width()-100)
        self.browser_frame.grid(row=1, column=0, sticky=NSEW)
        """
        for trajets in heuristique:
            self.textContent.insert(END, '{\n')
            for trajet in trajets:
                self.textContent.insert(END, '\t[')
                for cord in trajet:
                    self.textContent.insert(END, cord+' ')
                self.textContent.insert(END, '], ')
            self.textContent.insert(END, '\n}\n')
        """

    def calculate_heuristique(self, data_set):
        """
        Calculer les trajets du vhéhicule electrique
        :param data_set: a dictionary of all data
        :return: a list of trajets
        """
        if self.config:
            heuristique = Heuristic(data_set, self.config)
            result = heuristique.execute_heuristic(self.mode_heuristique)
            return result
        else:
            raise InvalidVariableError("Le fichier ne contient pas Véhicule.")

    def load_map_lyon_with_markers(self, dict_coords):
        """
        Generate html map file in /tmp
        :param list_coords: a list of marker coordinates to add on map
        :return:
        """
        trajet_color = ["red", "blue", "green", "yellow", "purple"]
        map = folium.Map(location=[45.7579341, 4.7650811], zoom_start=13)

        for num_vheicule, list_coords in dict_coords.items():
            for index, coords in enumerate(list_coords):
                folium.Marker(coords,
                              popup='<i>Latitude :</i>'+str(coords[0])+'<br>'+
                              '<i>Longitude  :</i>'+str(coords[1]),
                              tooltip='Véhicule N°'+str(num_vheicule))\
                    .add_to(map)
                
            folium.PolyLine(list_coords, color=trajet_color[num_vheicule-1], weight=2.5, opacity=1).add_to(map)
        map.save('./tmp/my_map_lyon.html')

    def set_mode_heuristique(self, mode):
        self.mode_heuristique = mode
