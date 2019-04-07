from tkinter.filedialog import askopenfilename, askdirectory
from exceptions.InvalidInitFileError import InvalidInitFileError
from src.modele.VehicleConfiguration import VehicleConfiguration
import datetime
import time
import os
import configparser
import numpy as np


class FileHandler:

    INIT_FILE_TYPES = [("init file", "*.ini")]
    COORDINATE_DATA_FILE_NAME = "coords.txt"
    DEMANDE_DATA_FILE_NAME = "demandes.txt"
    DISTANCE_DATA_FILE_NAME = "distances.txt"
    TIMES_DATA_FILE_NAME = "times.txt"

    def __init__(self, root):
        self.root = root
        self.file_path = None
        self.file_extension = None

    def open_init_file(self):
        init_file = askopenfilename(
            parent=self.root,
            initialdir="./data",
            title='Choose a init file to load',
            filetypes=self.INIT_FILE_TYPES)

        self.file_path, self.file_extension = os.path.splitext(init_file)
        try:
            config = configparser.ConfigParser()
            config.read(init_file)
            self.check_ariables(config)
        except IOError:
            print('Can not open init file', self.file_path)
        except InvalidInitFileError as err:
            print("File error: ", err)
        else:
            vehicle_configuration = VehicleConfiguration(
                int(config['Vehicle']['max_dist']),
                int(config['Vehicle']['capacity']),
                int(config['Vehicle']['charge_fast']),
                int(config['Vehicle']['charge_midium']),
                int(config['Vehicle']['charge_slow']),
                int(self.get_datetime(config['Vehicle']['start_time'])),
                int(self.get_datetime(config['Vehicle']['end_time']))
            )
            return vehicle_configuration

    def check_ariables(self, config):
        if "Vehicle" not in config:
            raise InvalidInitFileError("Le fichier ne contient pas Véhicule.")
        else:
            try:
                config['Vehicle']['max_dist']
                config['Vehicle']['capacity']
                config['Vehicle']['charge_fast']
                config['Vehicle']['charge_midium']
                config['Vehicle']['charge_slow']
                config['Vehicle']['start_time']
                config['Vehicle']['end_time']
            except NameError:
                print("variables are not defined.")

    def open_data_directory(self):
        directory = askdirectory(parent=self.root, initialdir="./data/", title='Choose the data directory')
        if directory:
            try:
                data = {'coordinates': None, 'demands': None, 'distances': None, 'times': None}
                data['coordinates'] = np.loadtxt(directory + '/' + self.COORDINATE_DATA_FILE_NAME, delimiter=',', dtype=str)
                data['demands'] = np.loadtxt(directory + '/' + self.DEMANDE_DATA_FILE_NAME, dtype=int)
                data['distances'] = np.loadtxt(directory + '/' + self.DISTANCE_DATA_FILE_NAME, dtype=int)
                data['times'] = np.loadtxt(directory + '/' + self.TIMES_DATA_FILE_NAME, dtype=int)
            except IOError:
                print('Can not open/write.')
            else:
                return data

    def get_datetime(self, time_str):
        time_obj = time.strptime(time_str, '"%H:%M"')
        return \
            datetime.timedelta(hours=time_obj.tm_hour, minutes=time_obj.tm_min, seconds=time_obj.tm_sec).total_seconds()
