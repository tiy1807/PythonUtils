# ------------------------------------------------------------------------------
# Class Store
#
# Allows for objects to be stored into .csv file format and then recreated when
# read from a file. The benefit to this is when a program has a list of objects
# that must be kept between instances of the program being run.
# ------------------------------------------------------------------------------
import csv
import sys

class Store:
    def __init__(self, file_path, object, object_container=None):
        self.file_path = file_path
        self.constructor = object
        self.container = object_container

    def read_to_container(self):
        if self.container is None:
            raise TypeError("No container has been defined for this object")

        return self.container(self.read())

    def read(self):
        # Reads the .csv file, and returns a list of objects
        object_list = []
        reader = csv.reader(open(self.file_path))
        for row in reader:
            object_list.append(self.constructor(*row))
        return object_list

    def write(self, object, access="w"):
        # Overwrites file. Writes objects in a .csv format. Requires object
        # to have a to_csv function
        writer = csv.writer(open(self.file_path,access,newline=''))
        writer.writerows(object.to_csv())

    def sort(self, get_sort_value):
        object_list = self.read()
        object_list.sort(key=lambda object:get_sort_value(object))

    def write_new_record(self, args):
        with open(self.file_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            object = self.constructor(*args)
            writer.writerow(object.to_csv())
