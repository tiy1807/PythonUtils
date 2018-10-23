from repetative_tasks.task_reminder import TaskReminder
from pathlib import Path

record_location = Path("repetative_tasks") / "test_data.csv"
reminder = TaskReminder(record_location)
reminder.run()
