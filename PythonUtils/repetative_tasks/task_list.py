# ------------------------------------------------------------------------------
# Class TaskList
#
# Stores a tasks in a list. Prints them in order
# ------------------------------------------------------------------------------
from PythonUtils.repetative_tasks.task import Task
from PythonUtils.user_input import UserInput
from PythonUtils.multiple_inputs import MultipleInput
from PythonUtils.text_input import TextInput
from PythonUtils.object_list import ObjectList

class TaskList(ObjectList):
    def __init__(self, task_list=[]):
        ObjectList.__init__(self, Task, task_list)

    def add_task(self):
        tui_name = TextInput("What is the name of your task?")
        tui_frequency = TextInput("How often do you need to do this?")
        tui_ask = MultipleInput([tui_name,tui_frequency],self._add)

        tui_ask.request_inputs()

    def task_names(self):
        return [task.name for task in self.object_list]

    def to_string(self):
        self.object_list.sort(key=lambda task:task.due())
        result = ""
        max_name_length = self.max_name_length()
        for task in self.object_list:
            result += task.to_string(max_name_length) + "\n"
        return result

    def find_task_with_name(self,name):
        matching_task = None
        # Replace with list comprehension
        for task in self.object_list:
            if task.name == name:
                matching_task = task
        return matching_task

    def max_name_length(self):
        length = 0
        for task in self.object_list:
            if length < len(task.name):
                length = len(task.name)
        return length
