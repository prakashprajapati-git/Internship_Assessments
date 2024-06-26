import tkinter as tk
from tkinter import messagebox
from tkinter import font
import json
import os

# File to store the to-do list
TODO_FILE = 'todo.json'

# Load existing tasks from the JSON file
def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        return json.load(file)

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Main application class
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prakash's TO_DO_LIST_APP")
        self.geometry("600x400")
        self.configure(bg='#87CEEB')  # Sky blue background
        self.tasks = load_tasks()
        self.create_widgets()
        self.update_task_listbox()

    def create_widgets(self):
        # Custom fonts
        title_font = font.Font(family="Comic Sans MS", size=24, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=14)
        button_font = font.Font(family="Helvetica", size=12)

        # Title label
        self.title_label = tk.Label(self, text="The To-Do List", font=title_font, bg='#87CEEB', fg='#8b4513')
        self.title_label.pack(pady=10)

        # Task entry label
        self.task_entry_label = tk.Label(self, text="Enter the Task:", font=label_font, bg='#87CEEB', fg='#8b4513')
        self.task_entry_label.pack(pady=5)

        # Task entry
        self.task_entry = tk.Entry(self, width=50, font=label_font, bg='#ffffff', fg='#333')
        self.task_entry.pack(pady=5)

        # Button frame
        self.button_frame = tk.Frame(self, bg='#87CEEB')
        self.button_frame.pack(pady=10, side=tk.LEFT, fill=tk.Y)

        # Add task button
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, font=button_font, bg='#4682b4', fg='#fff', width=15)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        # Delete task button
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, font=button_font, bg='#4682b4', fg='#fff', width=15)
        self.delete_button.grid(row=1, column=0, padx=5, pady=5)

        # Delete all tasks button
        self.delete_all_button = tk.Button(self.button_frame, text="Delete All Tasks", command=self.delete_all_tasks, font=button_font, bg='#4682b4', fg='#fff', width=15)
        self.delete_all_button.grid(row=2, column=0, padx=5, pady=5)

        # Mark as done button
        self.mark_done_button = tk.Button(self.button_frame, text="Mark as Done", command=self.mark_task_done, font=button_font, bg='#4682b4', fg='#fff', width=15)
        self.mark_done_button.grid(row=3, column=0, padx=5, pady=5)

        # Exit button
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.quit, font=button_font, bg='#4682b4', fg='#fff', width=15)
        self.exit_button.grid(row=4, column=0, padx=5, pady=5)

        # Task list frame on the right
        self.task_list_frame = tk.Frame(self, bg='#87CEEB')
        self.task_list_frame.pack(padx=20, pady=20, side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Task listbox
        self.task_listbox = tk.Listbox(self.task_list_frame, selectmode=tk.SINGLE, height=20, width=50, font=label_font, bg='#ffffff', fg='#333')
        self.task_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Done" if task['done'] else "Pending"
            self.task_listbox.insert(tk.END, f"{task['description']} [{status}]")

    def add_task(self):
        description = self.task_entry.get().strip()
        if description:
            self.tasks.append({"description": description, "done": False})
            save_tasks(self.tasks)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "No task selected to delete.")

    def delete_all_tasks(self):
        if messagebox.askyesno("Delete All Tasks", "Are you sure you want to delete all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.update_task_listbox()

    def mark_task_done(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]['done'] = True
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "No task selected to mark as done.")

# Main function to run the application
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
