from PythonUtils.task import Task
from PythonUtils.task_list import TaskList
from PythonUtils.storer import Store

test_store = Store("test_data.csv",Task,TaskList)
tasks = test_store.read_to_container()
test_store.write(tasks)
