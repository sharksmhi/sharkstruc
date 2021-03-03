# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-05 09:38

@author: johannes

"""
from abc import ABC
import pandas as pd


class Frame(pd.DataFrame, ABC):
    """
    Stores data from one, and only one, element (usually an excel sheet or a txt file).
    """
    @property
    def _constructor(self):
        """
        Constructor for Frame, overides method in pandas.DataFrame
        """
        return Frame

    def convert_formats(self):
        self[self.data_columns] = self[self.data_columns].astype(float)


class DataFrames(dict):
    """
    Stores information for delivery elements (sheets / files, eg. delivery_info, data, analyse_info, sampling_info).
    Use element name as key in this dictionary of Frame()-objects
    """
    def __init__(self, **kwargs):
        super(DataFrames, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def append_new_frame(self, name=None, data=None, **kwargs):
        if name:
            # print('New data added for {}'.format(name))
            self.setdefault(name, Frame(data))
            # self[name].convert_formats()
            # self[name].exclude_flagged_data()
