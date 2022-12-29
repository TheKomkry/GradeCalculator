from tkinter import *

# A function that calculates the average grade based on a list of entries.
def calculateGrade(entryList:list):
    # Initialize an empty list of grades.
    grades = []
    # Loop through the list of entries.
    for grade_, weight_ in entryList:
        try:
            # Convert the values in the entries to floats.
            if grade_.get() == "0":
                raise ValueError
            grade = float(grade_.get().replace(",", "."))
            weight = float(weight_.get().replace(",", "."))
        except ValueError:
            # If the values could not be converted to floats, set them to 0 and clear the entries.
            grade_.delete(0, END)
            weight_.delete(0, END)
            grade_.insert(0, "0")
            weight_.insert(0, "0")
            grade = 0
            weight = 0
        except Exception as e:
            # Print any other errors and continue to the next iteration.
            print(f"Error: {e}\nPress enter to continue...")
            continue
        # Append the grade and weight to the list of grades.
        grades.append([grade, weight])
        
    # Initialize the sum of weights to 0.
    weightSum = 0
    # Initialize an empty list of multiplied grades.
    multipliedGrades = []
    # Loop through the list of grades.
    for grade_, weight_ in grades:
        # Add the weight to the sum of weights.
        weightSum += weight_
        # Append the grade multiplied by the weight to the list of multiplied grades.
        multipliedGrades.append(grade_ * weight_)
    # If the sum of weights is 0, return 0.
    if weightSum == 0:
        return 0
    # Calculate and return the average grade by dividing the sum of multiplied grades by the sum of weights.
    return sum(multipliedGrades) / weightSum

# A function that adds a new field for entering a grade and weight.
def AddFieldForGrade():
    # Declare the global line number variable.
    global lineNum
    # Add a label for "Grade: " at the current line number.
    Label(root, text="Grade: ").grid(row=lineNum, column=0)
    # Add an entry field for the grade at the current line number.
    gradeEntry = Entry(root)
    gradeEntry.grid(row=lineNum, column=1)
    # Add a label for "Weight: " at the current line number.
    Label(root, text="Weight: ").grid(row=lineNum, column=2)
    # Add an entry field for the weight at the current line number.
    weightEntry = Entry(root)
    weightEntry.grid(row=lineNum, column=3)
    # Append the entries to the list of entries.
    listOfEntrys.append([gradeEntry, weightEntry])
    # Increment the line number.
    lineNum += 1

# A function that clears all the fields and resets the average to 0.
def Repeat():
    # Declare the global line number variable.
    global lineNum
    # Reset the line number to 0.
    lineNum = 0
    # Clear the list of entries.
    listOfEntrys.clear()
    # Reset the text of the average label to "Your average is: 0".
    average.config(text="Your average is: " + "0")
    # Loop through all the widgets in the root window.
    for widget in root.winfo_children():
        # If the widget is a label with the text "Grade: " or "Weight: ", destroy it.
        if widget["text"] == "Grade: " or widget["text"] == "Weight: ":
            widget.destroy()
        # If the widget is an entry field, destroy it.
        elif widget.winfo_class() == "Entry":
            widget.destroy()
    # Add a new field for entering a grade and weight.
    AddFieldForGrade()

# A function that attempts to convert a number to an integer or float and returns the original number if it fails.
def TryIfNumberIsInt(number):
    try:
        # Convert the number to a float.
        number = float(number)
        # If the float is an integer, convert it to an integer and return it.
        if number.is_integer():
            return int(number)
        # Otherwise, return the float.
        return float(number)
    except ValueError:
        # If the number could not be converted to a float, return the original number.
        number = number
    return number

# Create the root window for the GUI.
root = Tk()
# Set the title of the window.
root.title("Grade Calculator by Komkry")
# Set an icon for the window.
root.wm_iconbitmap('graduation-hat.ico')


# Initialize the line number to 0.
lineNum = 0
# Initialize an empty list of entries.
listOfEntrys = []

AddFieldForGrade()

# Window template.
Button(root, text="Calculate", command=lambda: average.config(text="Your average is: " + str(calculateGrade(listOfEntrys)))).grid(row=997, column=2, columnspan=2)
Button(root, text="Add grade", command=AddFieldForGrade).grid(row=997, column=0, columnspan=2)
average = Label(root, text="Your grade average: " + str(calculateGrade(listOfEntrys)))
average.grid(row=998, columnspan=4)
button = Button(root, text="RESET", command=Repeat).grid(row=999, column=0, columnspan=4)

# Start the main loop. This is where the GUI (window) is displayed.
root.mainloop()
