from task import Task
from task_list import TaskList
from storer import Store

test_store = Store("test_data.csv",Task,TaskList)
tasks = test_store.read_to_container()
test_store.write(tasks)
