import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import json
import os
from tkcalendar import Calendar
import PyPDF2
import customtkinter as ctk
#customtkinter==5.2.0
#tkcalendar==1.6.1
#PyPDF2==3.0.1
#Pillow==10.0.0
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Todo List")
        self.root.geometry("1000x600")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize variables
        self.tasks = []
        self.current_task_type = tk.StringVar(value="general")
        self.grocery_items = [
            "Milk", "Bread", "Eggs", "Butter", "Cheese", "Yogurt",
            "Chicken", "Beef", "Fish", "Rice", "Pasta", "Flour",
            "Sugar", "Salt", "Pepper", "Oil", "Vinegar", "Ketchup",
            "Mustard", "Mayonnaise", "Cereal", "Coffee", "Tea",
            "Fruits", "Vegetables", "Potatoes", "Onions", "Garlic",
            "Tomatoes", "Cucumber", "Carrots", "Apples", "Bananas",
            "Orange Juice", "Water", "Soda", "Chips", "Cookies",
            "Chocolate", "Ice Cream", "Frozen Pizza", "Frozen Vegetables"
        ]
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel for task input
        self.create_left_panel()
        
        # Create right panel for task list
        self.create_right_panel()
        
        # Load existing tasks
        self.load_tasks()

    def create_left_panel(self):
        left_panel = ctk.CTkFrame(self.main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Task type selection
        task_types = [("General", "general"), ("Grocery", "grocery"), ("Appointment", "appointment")]
        for text, value in task_types:
            ctk.CTkRadioButton(left_panel, text=text, variable=self.current_task_type, 
                             value=value, command=self.on_task_type_change).pack(pady=5)
        
        # Task input section
        self.task_label = ctk.CTkLabel(left_panel, text="Task:")
        self.task_label.pack(pady=5)
        
        # Regular task entry
        self.task_entry = ctk.CTkEntry(left_panel, width=300)
        self.task_entry.pack(pady=5)
        
        # Grocery items dropdown (initially hidden)
        self.grocery_dropdown = ctk.CTkOptionMenu(left_panel, values=self.grocery_items,
                                                command=self.on_grocery_select)
        self.grocery_dropdown.pack(pady=5)
        self.grocery_dropdown.pack_forget()  # Initially hidden
        
        # Due date
        ctk.CTkLabel(left_panel, text="Due Date:").pack(pady=5)
        self.calendar = Calendar(left_panel, selectmode='day', 
                               year=datetime.datetime.now().year,
                               month=datetime.datetime.now().month,
                               day=datetime.datetime.now().day)
        self.calendar.pack(pady=5)
        
        # Time input
        ctk.CTkLabel(left_panel, text="Time (HH:MM):").pack(pady=5)
        self.time_entry = ctk.CTkEntry(left_panel, width=100)
        self.time_entry.pack(pady=5)
        
        # Add task button
        ctk.CTkButton(left_panel, text="Add Task", command=self.add_task).pack(pady=10)
        
        # Import PDF button
        ctk.CTkButton(left_panel, text="Import from PDF", command=self.import_pdf).pack(pady=10)

    def on_task_type_change(self):
        task_type = self.current_task_type.get()
        if task_type == "grocery":
            self.task_entry.pack_forget()
            self.grocery_dropdown.pack(pady=5)
        else:
            self.grocery_dropdown.pack_forget()
            self.task_entry.pack(pady=5)

    def on_grocery_select(self, choice):
        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, choice)

    def create_right_panel(self):
        right_panel = ctk.CTkFrame(self.main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Task list
        ctk.CTkLabel(right_panel, text="Tasks:").pack(pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(right_panel, columns=("Task", "Type", "Due Date", "Time"), show="headings")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Time", text="Time")
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Delete button
        ctk.CTkButton(right_panel, text="Delete Selected", command=self.delete_task).pack(pady=10)

    def add_task(self):
        task_type = self.current_task_type.get()
        
        if task_type == "grocery":
            task = self.grocery_dropdown.get()
        else:
            task = self.task_entry.get()
            
        due_date = self.calendar.get_date()
        time = self.time_entry.get()
        
        if not task:
            messagebox.showerror("Error", "Please enter a task")
            return
            
        if task_type == "appointment" and not time:
            messagebox.showerror("Error", "Please enter time for appointment")
            return
            
        self.tasks.append({
            "task": task,
            "type": task_type,
            "due_date": due_date,
            "time": time
        })
        
        self.update_task_list()
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        if task_type == "grocery":
            self.grocery_dropdown.set("Select Item")

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to delete")
            return
            
        index = self.tree.index(selected_item[0])
        del self.tasks[index]
        self.update_task_list()
        self.save_tasks()

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(
                task["task"],
                task["type"],
                task["due_date"],
                task["time"]
            ))

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                self.update_task_list()
        except FileNotFoundError:
            pass

    def import_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
            
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                    
                # Split text into lines and add as tasks
                lines = text.split('\n')
                for line in lines:
                    if line.strip():
                        self.tasks.append({
                            "task": line.strip(),
                            "type": "general",
                            "due_date": datetime.datetime.now().strftime("%m/%d/%y"),
                            "time": ""
                        })
                        
                self.update_task_list()
                self.save_tasks()
                messagebox.showinfo("Success", "PDF imported successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error importing PDF: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop() 