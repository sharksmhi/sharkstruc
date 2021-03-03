# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""
import os
from copy import deepcopy
from pathlib import Path
from sharkstruc.readers.yml import yaml_reader
from sharkstruc.utils import generate_filepaths, get_app_directory, recursive_dict_update


class Settings:
    """
    """
    def __init__(self, *args, **kwargs):
        self.readers = {}
        self.writers = {}
        self.functions = {}

        self.base_directory = get_app_directory()

        self._load_settings(os.path.join(self.base_directory, 'etc'))
        self.default_attributes = None

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self.
        Special management of readers and writers.
        """
        if os.path.isfile(name):
            if isinstance(value, dict) and ('readers' in name or 'writers' in name or 'functions' in name):
                if 'readers' in name:
                    recursive_dict_update(self.readers, {Path(name).stem: value})
                elif 'writers' in name:
                    recursive_dict_update(self.writers, {Path(name).stem: value})
                else:
                    recursive_dict_update(self.functions, {Path(name).stem: value})
            else:
                super().__setattr__(Path(name).stem, value)
        elif name == 'attributes':
            super().__setattr__(name, self._get_attribute_dictionary(value))
        else:
            super().__setattr__(name, value)

    @staticmethod
    def _get_attribute_dictionary(settings_attributes):
        d = {}
        for key, item in settings_attributes.items():
            if isinstance(item, str):
                d.setdefault(item, key)
            elif isinstance(item, list):
                for attrb in item:
                    d.setdefault(attrb, key)
            else:
                raise Warning('Type of item is nor str or list:', type(item))
        return d

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _load_settings(self, etc_path):
        """
        Loading all .yaml files from etc directory.
        Special handling of readers and writers (see SettingsBase.__setattr__())
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = generate_filepaths(etc_path, pattern='.yaml')
        etc_data = {}
        for path in paths:
            data = yaml_reader(path)
            etc_data.setdefault(path, data)

        self.set_attributes(**etc_data)

    def load_reader(self, reader):
        reader_instance = self.readers[reader].get('reader')
        return reader_instance(**deepcopy(self.readers.get(reader)))

    def load_writer(self, writer):
        writer_instance = self.writers[writer].get('writer')
        return writer_instance(**self.writers.get(writer))

    @property
    def list_of_readers(self):
        return list(self.readers)

    @property
    def list_of_writers(self):
        return list(self.writers)

    @property
    def list_of_functions(self):
        return list(self.functions)

    def get_export_file_path(self, file_path=None, file_name=None, default_file_name=None, **kwargs):
        """
        Whenever there´s not an export path given by the user, we try to export elsewhere..
        """
        if file_path:

            if os.path.isdir(file_path):
                return file_path
            elif os.path.isdir(Path(file_path).parent):
                return file_path
            else:
                raise Warning('file_path given, but it´s not valid.')

        target_path = 'C:/shark_export'
        if os.path.isdir('C:/'):
            if not os.path.isdir(target_path):
                os.mkdir(target_path)
        else:
            target_path = self.base_directory

        file_name = file_name or default_file_name

        return os.path.join(target_path, file_name)


if __name__ == '__main__':
    settings = Settings()
