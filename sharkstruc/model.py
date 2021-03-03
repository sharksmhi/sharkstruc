# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""
from sharkstruc.config import Settings
from sharkstruc.handler import DataFrames


class Model:
    """
    Beautiful is better than ugly.
    Readability counts.

    - setup model structure
    - initialize reader
    - load data
    - use selected functions

    Example usage:
        model = Model(reader='shark_archive', model='shark_phyche')

    """
    def __init__(self, *args, reader=None, model=None, **kwargs):
        """

        Args:
            reader (str): Name of reader. Used to initialize reader object.
        """
        self.settings = Settings(reader=reader, **kwargs)

    def read(self, *args, reader=None, delivery_name=None, **kwargs):
        """
        Read and append requested data source.

        Using the given reader (name of reader) to load and initialize a reader object via Settings.
        Elements of the data delivery are put into Frame objects and collected into a source dictionary
        Args:
            delivery path (in *args): path to delivery (str)
            reader (str): One of the readers found in self.settings.list_of_readers
            delivery_name (str): Chosen name of delivery. Used as key in self.deliveries
        """
        if not reader:
            raise ValueError('Missing reader! Please give one as input (App.read(reader=NAME_OF_READER)')
        if reader not in self.settings.list_of_readers:
            raise ValueError('Given reader does not exist as a valid option! '
                             '(valid options: {}'.format(', '.join(self.settings.list_of_readers)))

        if not args:
            raise ValueError('Missing file path! Please give one as input (App.read(PATH_TO_DATA_SOURCE)')

        reader = self.settings.load_reader(reader)
        delivery_name = delivery_name

        reader.load(*args, **kwargs)

        dfs = DataFrames(data_type=reader.get('data_type'), name=delivery_name)
        for element, item in reader.elements.items():
            df = reader.read_element(item.pop('element_specifier'), **item)
            dfs.append_new_frame(name=element, data=df)

        self.deliveries.append_new_delivery(name=delivery_name, data=dfs)

    def write(self, *args, writer=None, **kwargs):
        raise NotImplementedError
