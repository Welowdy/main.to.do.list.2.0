from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class todo:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List App')
        self.root.geometry('850x700+300+150')
        
        self.label = Label(self.root, text='To-Do List App', font='ariel, 25 bold', width=15, bd=5, bg='blue', fg='black')
        self.label.pack(side='top', fill=BOTH)
        
        self.label2 = Label(self.root, text='Add Task', font='ariel, 18 bold', width=10, bd=5, bg='green', fg='black')
        self.label2.place(x=40, y=54)
        
        self.label3 = Label(self.root, text='Tasks', font='ariel, 18 bold', width=45, bd=5, bg='orange', fg='black')
        self.label3.place(x=380, y=54)
        
        self.label4 = Label(self.root, text='Deadline (dd-mm-yyyy)', font='ariel, 12', width=18, bd=5, bg='yellow', fg='black')
        self.label4.place(x=20, y=180)
        
        self.label5 = Label(self.root, text='Priority (1-5)', font='ariel, 12', width=10, bd=5, bg='magenta', fg='black')
        self.label5.place(x=20, y=240)
        
        self.label6 = Label(self.root, text='Category', font='ariel, 12', width=10, bd=5, bg='purple', fg='black')
        self.label6.place(x=20, y=300)
        
        self.label7 = Label(self.root, text='Status', font='ariel, 12', width=10, bd=5, bg='pink', fg='black')
        self.label7.place(x=20, y=360)
        
        self.label8 = Label(self.root, text='Search by Date or Priority', font='ariel, 12', width=25, bd=5, bg='brown', fg='black')
        self.label8.place(x=20, y=460)

        self.label9 = Label(self.root, text='about us', font='ariel, 18 bold', width=20, bd=3, bg='cyan', fg='black')
        self.label9.place(x=680, y=400)
        
        self.label9 = Label(self.root, text='danush:)', font='ariel, 18 bold', width=20, height=6, bd=3, bg='black', fg='white')
        self.label9.place(x=680, y=450)

        self.main_text = Listbox(self.root, height=9, bd=5, width=80, font="ariel, 15 italic bold")
        self.main_text.place(x=280, y=100)
        
        self.text = Text(self.root, bd=5, height=2, width=30, font='ariel, 10 bold')
        self.text.place(x=20, y=120)

        
        self.deadline = Entry(self.root, bd=5, width=18, font='ariel, 12')
        self.deadline.place(x=20, y=210)
        
        self.priority = Entry(self.root, bd=5, width=18, font='ariel, 12')
        self.priority.place(x=20, y=270)
        
        self.category = Entry(self.root, bd=5, width=18, font='ariel, 12')
        self.category.place(x=20, y=330)
        
        self.status = ttk.Combobox(self.root, values=["Not Started", "In Progress", "Completed"], font='ariel, 12', width=18)
        self.status.place(x=20, y=390)
        self.status.current(0)
        
        self.search_entry = Entry(self.root, bd=5, width=18, font='ariel, 12')
        self.search_entry.place(x=20, y=490)
        
        self.tasks = []
        self.load_tasks()

        self.add_button = Button(self.root, text="Add", font='sarif, 15 bold italic', width=5, bd=2, bg='orange', fg='black', command=self.add)
        self.add_button.place(x=30, y=550)
        
        self.delete_button = Button(self.root, text="Delete", font='sarif, 15 bold italic', width=5, bd=2, bg='red', fg='black', command=self.delete)
        self.delete_button.place(x=130, y=550)
        
        self.search_button = Button(self.root, text="Search", font='sarif, 15 bold italic', width=6, bd=3, bg='green', fg='black', command=self.search)
        self.search_button.place(x=270, y=490)

    def add(self):
        content = self.text.get(1.0, END).strip()
        deadline = self.deadline.get().strip()
        priority = self.priority.get().strip()
        category = self.category.get().strip()
        status = self.status.get().strip()

        if content and deadline and priority and category and status:
            try:
                datetime.strptime(deadline, "%d-%m-%Y")
                priority = int(priority)
                task = f"{content} (Deadline: {deadline}, Priority: {priority}, Category: {category}, Status: {status})"
                self.main_text.insert(END, task)
                self.tasks.append(task)
                self.save_tasks()
                self.text.delete(1.0, END)
                self.deadline.delete(0, END)
                self.priority.delete(0, END)
                self.category.delete(0, END)
                self.status.current(0)
            except ValueError:
                messagebox.showerror("Invalid Data", "Please enter a valid date (dd-mm-yyyy) and priority (1-5)")
        else:
            messagebox.showerror("Missing Data", "Please fill all fields")

    def delete(self):
        selected_task_index = self.main_text.curselection()
        if selected_task_index:
            self.main_text.delete(selected_task_index)
            self.tasks.pop(selected_task_index[0])
            self.save_tasks()

    def search(self):
        query = self.search_entry.get().strip()
        if query:
            filtered_tasks = [task for task in self.tasks if query in task]
            self.main_text.delete(0, END)
            for task in filtered_tasks:
                self.main_text.insert(END, task)
        else:
            self.main_text.delete(0, END)
            for task in self.tasks:
                self.main_text.insert(END, task)

    def save_tasks(self):
        with open('data.txt', 'w') as file:
            for task in self.tasks:
                file.write(task + '\n')

    def load_tasks(self):
        try:
            with open('data.txt', 'r') as file:
                for line in file:
                    self.tasks.append(line.strip())
                    self.main_text.insert(END, line.strip())
        except FileNotFoundError:
            pass

    def update_countdown(self):
        for i in range(self.main_text.size()):
            task = self.main_text.get(i)
            if "Deadline:" in task:
                deadline_str = task.split("Deadline: ")[1].split(",")[0]
                deadline = datetime.strptime(deadline_str, "%d-%m-%Y")
                days_left = (deadline - datetime.now()).days
                task = f"{task} (Days Left: {days_left})"
                self.main_text.delete(i)
                self.main_text.insert(i, task)
        self.root.after(86400000, self.update_countdown)

def main():
    root = Tk()
    ui = todo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
