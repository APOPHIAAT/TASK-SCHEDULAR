"""
GROUP MEMBERS
ATWIJUKIRE APOPHIA M23B23/051
WATNEN ERIC OYWAK  S23B23/040
"""

import bisect
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class SchedulingAssistant:
    def __init__(self):
        self.tasks = []  # Format: [(start_time, end_time, type, description, priority)]

    def add_task(self, start, end, task_type, description, priority):
        """Add a task to the schedule."""
        bisect.insort(self.tasks, (start, end, task_type, description, priority))
        print("Task added successfully!")

    def sort_tasks(self, key='deadline'):
        """
        Sorts tasks based on the specified criteria.
        Parameters:
        - key: Sorting criterion ('deadline', 'priority', or 'type').
        """
        if key == 'deadline':
            self.tasks = merge_sort(self.tasks, key=lambda x: x[1])
        elif key == 'priority':
            self.tasks = merge_sort(self.tasks, key=lambda x: -x[4])  # Descending priority
        elif key == 'type':
            self.tasks = merge_sort(self.tasks, key=lambda x: x[2])
        print("\nTasks sorted based on:", key)

    def find_task_by_time(self, query_time):
        """
        Searches for tasks overlapping a given time using binary search.
        Parameters:
        - query_time: The time to search for (datetime).
        """
        overlapping_tasks = []
        for task in self.tasks:
            if task[0] <= query_time <= task[1]:
                overlapping_tasks.append(task)

        if overlapping_tasks:
            print(f"Tasks overlapping {query_time}:")
            for task in overlapping_tasks:
                print(f"{task}")
        else:
            print("No tasks found for the specified time.")

    def analyze_busy_slots(self, interval_hours=1):
        """
        Analyzes task density over specified time intervals.
        Parameters:
        - interval_hours: Length of each time interval in hours.
        """
        print(f"\nAnalyzing busy slots with {interval_hours}-hour intervals...")
        if not self.tasks:
            print("No tasks to analyze.")
            return

        # Calculate the start and end range for analysis
        min_time = min(task[0] for task in self.tasks)
        max_time = max(task[1] for task in self.tasks)
        interval = timedelta(hours=interval_hours)

        current_time = min_time
        busy_slots = []

        while current_time < max_time:
            end_time = current_time + interval
            count = sum(1 for task in self.tasks if task[0] < end_time and task[1] > current_time)
            busy_slots.append((current_time, end_time, count))
            current_time = end_time

        # Display the results
        for slot in busy_slots:
            print(f"{slot[0]} to {slot[1]}: {slot[2]} tasks")

    def plot_gantt_chart(self):
        """
        Generates a Gantt chart of tasks.
        Displays tasks as horizontal bars, grouped by type (personal or academic),
        with task names and dates displayed on the bars.
        """
        personal_tasks = [(task[0], task[1], task[3]) for task in self.tasks if task[2] == 'personal']
        academic_tasks = [(task[0], task[1], task[3]) for task in self.tasks if task[2] == 'academic']

        fig, ax = plt.subplots(figsize=(10, 6))
        bar_height = 0.4

        # Plot personal tasks
        for i, task in enumerate(personal_tasks, 1):
            duration = (task[1] - task[0]).total_seconds() / 3600
            ax.barh(i, duration, left=task[0].hour, height=bar_height, color='blue', label='Personal' if i == 1 else "")
            ax.text(task[0].hour + duration / 2, i, f"{task[2]} ({task[0].strftime('%Y-%m-%d')})", ha='center', va='center', color='white', fontsize=8)

        # Plot academic tasks
        for i, task in enumerate(academic_tasks, len(personal_tasks) + 1):
            duration = (task[1] - task[0]).total_seconds() / 3600
            ax.barh(i, duration, left=task[0].hour, height=bar_height, color='green', label='Academic' if i == len(personal_tasks) + 1 else "")
            ax.text(task[0].hour + duration / 2, i, f"{task[2]} ({task[0].strftime('%Y-%m-%d')})", ha='center', va='center', color='white', fontsize=8)

        ax.set_xlabel('Time (Hours)')
        ax.set_ylabel('Tasks')
        ax.set_title('Gantt Chart of Tasks')
        ax.legend()
        plt.show()


def merge_sort(data, key=lambda x: x):
    """Merge Sort Implementation."""
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)
    return merge(left, right, key)


def merge(left, right, key):
    """Helper function for merge sort."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def main():
    assistant = SchedulingAssistant()

    while True:
        print("\nPersonal Scheduling Assistant")
        print("1. Add Task")
        print("2. Sort Tasks")
        print("3. Find Task by Time")
        print("4. Analyze Busy Slots")
        print("5. Plot Gantt Chart")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            start = datetime.strptime(input("Enter start time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
            end = datetime.strptime(input("Enter end time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
            task_type = input("Enter task type (personal/academic): ")
            description = input("Enter task description: ")
            priority = int(input("Enter task priority (1-10): "))
            assistant.add_task(start, end, task_type, description, priority)
        elif choice == '2':
            key = input("Sort by (deadline/priority/type): ")
            assistant.sort_tasks(key)
        elif choice == '3':
            query_time = datetime.strptime(input("Enter the time to search for (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
            assistant.find_task_by_time(query_time)
        elif choice == '4':
            interval = int(input("Enter interval length in hours: "))
            assistant.analyze_busy_slots(interval)
        elif choice == '5':
            assistant.plot_gantt_chart()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again!")


if __name__ == "__main__":
    main()