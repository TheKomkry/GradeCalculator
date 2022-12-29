from tkinter import *

# A function that gets grades from the console.
def getGrades(gradeList:list=[]):
    print("Enter grades and weights.\nTo stop entering grades, press enter.")
    # Initialize a list of grades to the input list of grades.
    grades = gradeList
    # Prompt the user to enter a grade and replace any commas with periods.
    grade = input("Enter grade: ").replace(",", ".")
    # Prompt the user to enter a weight if a grade was entered.
    if grade != "":
        weight = input("Enter weight: ").replace(",", ".")

    # Keep prompting the user to enter grades and weights until they stop providing input.
    while grade != "":
        try:
            # Convert the grade and weight to floats and append them to the list of grades.
            grades.append([float(grade), float(weight)])
        except ValueError:
            # If the grade or weight could not be converted to a float, append 0s to the list of grades.
            grades.append([0, 0])
        # Prompt the user to enter a new grade and weight.
        grade = input("Enter grade: ").replace(",", ".")
        if grade != "":
            weight = input("Enter weight: ").replace(",", ".")
    # Return the list of grades.
    print("Grades entered.\nNow return to the application.")
    return grades

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


def createFileIfItDoesntExist(path: str):
    # Try to open the file in read-only mode
    try:
        with open("settings.txt", "r") as f:
            pass
    except FileNotFoundError:
        # If the file does not exist, create it
        with open("settings.txt", "w") as f:
            pass
        
def getSettingValue(setting_name: str):
    try:
        with open("settings.txt", "r") as f:
            # Read all the lines of the file
            lines = f.readlines()
            # Iterate over each line
            for line in lines:
                # Split the line into key and value
                lineData = line.split(":")
                key = lineData[0]
                # If the key matches the setting name, return the value
                if key == setting_name:
                    # if the line does not have a value, return an empty string, else return the value
                    return "" if len(lineData) < 2 else lineData[1].strip()
    except FileNotFoundError:
        # If the file does not exist, return an empty string
        return ""

def changeSetting(setting: str, value: str):
    # Create the file if it doesn't exist
    createFileIfItDoesntExist("settings.txt")
    # Open the file in read-write mode
    with open("settings.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        found = False
        for line in lines:
            if line.startswith(setting):
                f.write(f"{setting}:{value}\n")
                found = True
            else:
                f.write(line)
        if not found:
            # Add the setting to the last empty line
            f.write(f"{setting}:{value}\n")
        f.truncate()
enteredGrades = getGrades() if getSettingValue("use_console_input") == "True" else []

# Create the root window for the GUI.
root = Tk()
# Set the title of the window.
root.title("Grade Calculator by Komkry")
# Set an icon for the window.
root.wm_iconbitmap('graduation-hat.ico')

# Create a boolean IntVar to bind to the checkbox
use_console_input = IntVar()
use_console_input.set(1 if getSettingValue("use_console_input") == "True" else 0)

# Initialize the line number to 0.
lineNum = 0
# Initialize an empty list of entries.
listOfEntrys = []
# If there are grades in the list of entered grades, add fields for each grade and weight
if len(enteredGrades) > 0:
    for grade, weight in enteredGrades:
        Label(root, text="Grade: ").grid(row=lineNum, column=0)
        gradeEntry = Entry(root)
        gradeEntry.insert(0, TryIfNumberIsInt(grade))
        gradeEntry.grid(row=lineNum, column=1)
        Label(root, text="Weight: ").grid(row=lineNum, column=2)
        weightEntry = Entry(root)
        weightEntry.insert(0, TryIfNumberIsInt(weight))
        weightEntry.grid(row=lineNum, column=3)
        listOfEntrys.append([gradeEntry, weightEntry])
        lineNum += 1
# Otherwise, add a field for entering a grade and weight.
else:
    AddFieldForGrade()

# Window template.
Button(root, text="Calculate", command=lambda: average.config(text="Your average is: " + str(calculateGrade(listOfEntrys)))).grid(row=997, column=2, columnspan=2)
Button(root, text="Add grade", command=AddFieldForGrade).grid(row=997, column=0, columnspan=2)
average = Label(root, text="Your grade average: " + str(calculateGrade(listOfEntrys)))
average.grid(row=998, columnspan=4)
button = Button(root, text="RESET", command=Repeat).grid(row=999, column=0, columnspan=4)
Label(root, text="Use console to input the grades? (requires app restart)").grid(row=1000, column=0, columnspan=2)
Checkbutton(root, text="", variable=use_console_input, command=lambda: changeSetting("use_console_input", "True" if use_console_input.get() == 1 else "False")).grid(row=1000, column=2, columnspan=2)

# Start the main loop. This is where the GUI (window) is displayed.
root.mainloop()
