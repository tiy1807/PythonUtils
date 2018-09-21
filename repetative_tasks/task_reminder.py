# ------------------------------------------------------------------------------
# Class TaskReminder
# ------------------------------------------------------------------------------

from user_input import UserInput
from option_input import OptionInput
from option import Option
from storer import Store
from repetative_tasks.task_list import TaskList
from repetative_tasks.task import Task

class TaskReminder:
    def __init__(self, record_location):
        self.task_store = Store(record_location,Task,TaskList)
        self.task_list = self.task_store.read_to_container()

    def print_action(self):
        self.task_list = self.task_store.read_to_container()
        print(self.task_list.to_string())

    def complete_action(self):
        option_list = [Option(task.name,task.name,"") for task in self.task_list.object_list]
        tui_which_task = OptionInput("Which task have you completed?",options=option_list)
        rc = tui_which_task.request_input()
        if rc == UserInput.SUCCESS:
            task = self.task_list.find_task_with_name(tui_which_task.chosen_option.name)
            task.completed()
            self.task_store.write(self.task_list)
        elif rc == UserInput.ABORTED:
            print("Completion aborted. No task completed")

    def add_action(self):
        self.task_list.add_task()
        self.task_store.write(self.task_list)

    def exit_action(self):
        self.exit = True

    def run(self):
        self.exit = False

        PRINT = Option("print","p","Prints the tasks",self.print_action)
        COMPLETE = Option("complete task","c","Allows the user to mark a task as complete",self.complete_action)
        ADD = Option("add","a","Adds a new task to the list",self.add_action)
        EXIT = Option("exit","e","Exits the programme",self.exit_action)
        options = [PRINT, COMPLETE, ADD, EXIT]

        while not self.exit:
            tui_input = OptionInput("What would you like to do?",
                                  options=options,
                                  default="print")
            tui_input.request_input()
