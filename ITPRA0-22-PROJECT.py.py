'''
========================================================================================================
Programer: Kgothatso Masha

DATE: 9 June 2026 
      10:34

PURPOSE: Creating a Learner Progress Tracting Systme (LPTS)
          This system helps staff capture learner details, record assessment marks,
          determinde learner perfomance, and generate simple progress feedback.
========================================================================================================
'''

# Importing messagebox from tkinder
import tkinter as tk
from tkinter import messagebox

# Hiding the default tkinder window
root = tk.Tk()
root.withdraw()


# Creating a global ist of learners
learners = []


'''-----------------------------------------------------------------------------------------------------
Creating a recursive funtion that calculates sum of all marks
-----------------------------------------------------------------------------------------------------'''

def recursive_sum(marks, index=0):
    # Base Case: stops when we reach end of list
    if index == len(marks):
        return 0
    # Recursive Case: adds current mark to sum of the rest
    return marks[index] + recursive_sum(marks, index + 1)


'''-----------------------------------------------------------------------------------------------------
Creating Classes
-----------------------------------------------------------------------------------------------------'''

# Person
class Person:
    # Reprsents a general persom with common attribues
    def __init__(self, name, age):
        # common attributes
        self.name = name
        self.age = age

# Learner
class Learner(Person):
    # Represents learner
    def __init__(self, learner_id, name, age, course):
        # Inherits base attributes from Person
        super().__init__(name, age)
        self.learner_id = learner_id
        self.course = course
        self.marks = []
        self.__average_mark = 0 # average marks encupsulated

    # A way to get average marks
    def get_average_mark(self):
        return self.__average_mark
    
    # A way to set average marks
    def set_average_mark(self, value):
        self.__average_mark = value

    # Calculating average marks
    def calculate_average_mark(self):
        if len(self.marks) == 0:
            self.__average_mark = 0
        else:
            self.__average_mark = recursive_sum(self.marks) / len(self.marks)
        return self.__average_mark
    
    # Determining learner results
    def get_result(self):
        if len(self.marks) == 0:
            return "N/A"
        average = self.calculate_average_mark()
        if average >= 75:
            return "Passed with distinction"
        elif average >= 50:
            return "Pass"
        else:
            return "Fail"
        
    # Checking if learner qualifies for certificate
    def qualifies_for_certificate(self, pass_mark=50):
        return self.get_average_mark() >= pass_mark
    
    # Displaying full learner summary
    def display_summary(self):
        print(f"\n------ Learner Summary ------")
        print(f"Learner ID : {self.learner_id}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Course     : {self.course}")

    # If marks are not entered yet this will show
        if len(self.marks) == 0:
           print("Marks      : No marks entered yet")
           print("Average    : N/A")
           print("Result     : N/A")
           print("Certificate: N/A") 

        else:
            print(f"Marks      : {self.marks}")
            print(f"Average    : {self.get_average_mark():.2f}")
            print(f"Result     : {self.get_result()}")
            print(f"Certificate: {'Yes' if self.qualifies_for_certificate() else 'No'}")

'''------------------------------------------------------------------------------------------------------
Creating Functions
------------------------------------------------------------------------------------------------------'''

# That searches for learner esing ID
def search_learner(learner_id):
    for learner in learners:
        if learner.learner_id == learner_id:
            return learner
    return None

# That adds a learner
def add_learner():
    print("\n---- Add New Learner ----")

    # Adding ID
    learner_id = int(input("Enter Learner ID: "))

    if search_learner(learner_id) != None:
        messagebox.showerror("Error!", "A learner with that ID already exists.")
        return
    # Adding name
    name = input("Enter Learner Name: ")

    # Adding age that is between 6 and 100 years old
    while True: 
        try:
            age = int(input("Enter Learner age: "))
            if age < 6 or age > 100:
                messagebox.showerror("Error!", "Age should between 6 and 100")
                continue
            break
        except ValueError:
            messagebox.showerror("Input Invalid!", "Enter a number")
        
    # Adding course
    course = input("Enter Course Name: ")

    learner = Learner(learner_id, name, age, course)
    learners.append(learner)  
    messagebox.showinfo("Success!", "Learner Added Successfully")

# That displays all learners in the system
def show_all_learners():
    print("\n---- All Learners ----")
    if len(learners) == 0:
        print("No learners registered.")
        return
    for learner in learners:
        learner.display_summary()

# That Captures marks for a learner
def add_marks():
    print("\n---- Add Marks ----")
    learner_id = int(input("Enter Learner ID: "))
    learner = search_learner(learner_id)

    if learner is None:
        messagebox.showerror("Error!", "Learner not found!")
        return
    
    # Making sure only a number is entered
    try:
        num_marks = int(input("How many marks do you want to enter? "))
    except ValueError:
        messagebox.showerror("Error!", "Enter a number")
        return
    
    # a way to process the marks entered
    for i in range(num_marks):
        while True:
            try:
                mark = float(input(f"Enter mark {i + 1}: "))
                if mark < 0 or mark > 100:
                    print("Mark should be betwwen 0 and 100. Try again")
                    continue    # skips back to the top
                learner.marks.append(mark)   # adding mark to mark list
                break   # exits while loop when correct marks are added
            except ValueError:
                print("Invalid Mark! Enter a number")
    
    learner.calculate_average_mark()
    result = learner.get_result()
    messagebox.showinfo("Success!", "Marks captured successfuly")

# That updates an existing learner
def update_learner():
    print("\n---- Update Learner ----")
    learner_id = int(input("Enter learner ID to update: "))
    learner = search_learner(learner_id)

    if learner is None:
        messagebox.showerror("Error!", "Learner not found")
        return
    
    # New name
    n_name = input("Enter new name: ")
    if n_name != "":
        learner.name = n_name

    # New age
    n_age = input("Enter new age: ")
    if n_age != "":
        try:
            n_age = int(n_age)
            if n_age < 5 or n_age > 100:
                messagebox.showerror("Invalid Input!", "Age should be between 6 and 100")
                return
            learner.age = n_age
        except ValueError:
            messagebox.showerror("Input Invalid!", "Enter a number")
            return

    # New course
    n_course = input("Enter new course: ")
    if n_course != "":
        learner.course = n_course

    # A way to confirm is learner is updated
    messagebox.showinfo("Updated!", "Learner updated successfully")


# That removes a learner
def remove_learner():
    print("\n---- Remove Learner ----")
    learner_id = int(input("Enter learner ID to remove: "))
    learner = search_learner(learner_id)

    if learner is None:
        messagebox.showerror("Error!", "Learner does not exist")
        return

    learners.remove(learner)
    messagebox.showinfo("Deleted!", "Learner removed successfully")


'''--------------------------------------------------------------------------------------------------------
Creating Main Menu
--------------------------------------------------------------------------------------------------------'''
def main_menu():
    while True:
        print("\n======================================")
        print("   Learner Progress Tracting System   ")
        print("--------------------------------------")
        print("         1. Add learner              ")
        print("         2. Enter marks              ")
        print("         3. View all learners        ")
        print("         4. Search learner           ")
        print("         5. Update learner           ")
        print("         6. Remove learner           ")
        print("         7. Show learner result      ")
        print("         8. Exit                     ")
        print("======================================")

    # Making sure a number between 1 and 8 is chosen
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            messagebox.showerror("Input Invalid!", "Enter number between 1 and 8")
            continue

        if choice == 1:
            add_learner()

        elif choice == 2:
            add_marks()

        elif choice == 3:
            show_all_learners()

        elif choice == 4:
            learner_id = int(input("Enter learner ID to search: "))
            learner = search_learner(learner_id)
            if learner is None:
                messagebox.showerror("Error!", "Learner does not exist")
            else:
                learner.display_summary()

        elif choice == 5:
            update_learner()

        elif choice == 6:
            remove_learner()

        elif choice == 7:
            learner_id = int(input("Enter learner ID: "))
            learner = search_learner(learner_id)
            if learner is None:
                messagebox.showerror("Error!", "Learner not found")
            else:
                print(f"\n----Results for {learner.name}---")
                print(f"Average: {learner.get_average_mark():.2f}")
                print(f"Performance: {learner.get_result()}")
                if learner.qualifies_for_certificate():
                    messagebox.showinfo("Result!", f"{learner.name} qualifies for a certificate")
                else:
                    messagebox.showinfo("Result!", f"{learner.name} does not qualify for certificate")
        
        elif choice == 8:
            print("Exiting system...")
            # Asking the user to confirm exiting
            confirm = messagebox.askyesno("Exit!", "Are you sure you want to exit?")
            if confirm:
                break
        else:
            messagebox.showerror("Input Invalid!", "Enter between 1 and 8")

# Running program
if __name__ == "__main__":
    main_menu()



                      







