from questions import QuestionTasks
from tkinter import *
from tkinter import messagebox, filedialog
import argparse

# Class Variables:
filename = ''  # issuu_sample.JSON
visitorUUID = ''  # 67522a690d21b074
task = ''
docUUID = ''  # 130524154519-719ec9ea2b17493bb14aa34e60014380
# cw2.py -d 130524154519-719ec9ea2b17493bb14aa34e60014380 -t 4 -f "C:\Users\XXX\Documents\Industrial Programming\CW2\Sample JSON Files\issuu_cw2.json"

# Out of buttonTask for performance reasons; this way Static dict is only built once!
switcher = {
    '2a': lambda: QuestionTasks(filename, docUUID, visitorUUID).visualizeCountries(),
    '2b': lambda: QuestionTasks(filename, docUUID, visitorUUID).visualizeContinents(),
    '3a': lambda: QuestionTasks(filename, docUUID, visitorUUID).visualizeUnformattedBrowsers(),
    '3b': lambda: QuestionTasks(filename, docUUID, visitorUUID).visualizeFormattedBrowsers(),
    '4': lambda: QuestionTasks(filename, docUUID, visitorUUID).getTop10Readers(),
    '5': lambda: QuestionTasks(filename, docUUID, visitorUUID).alsoLikeTop10(visitorUUID),
    '6': lambda: QuestionTasks(filename, docUUID, visitorUUID).alsoLikeGraph(visitorUUID),
    '7': lambda: GUI()
}


class GUI:
    """
        This class creates a GUI using the Tkinter library
        On initialization the window is created and the default layout is set.
        The task buttons are given a single method to use rather than one each, unlike the user + doc ID ones.
    """

    # Button methods:
    def visitorUUIDClicked(self):
        """
            Method that will set class visitorUUID to matching entry provided in textbox.
            If a userID has already been supplied, User is able to remove entry and set visitorUUID back to None.
        """
        global visitorUUID
        if self.window.visitor_uuid_btn.cget('text') == 'Remove':
            visitorUUID = ''
            self.window.visitor_uuid_btn.configure(text='Submit visitor UUID')
            self.window.visitor_uuid_lbl.configure(text='No Visitor UUID', fg='blue')
            return
        if self.window.visitor_uuid_txtBox.get() == '':  # Error checking: cant submit empty UUID field
            messagebox.showwarning('Invalid Input', 'Please check you''ve entered a valid visitor UUID.')
            return
        visitorUUID = self.window.visitor_uuid_txtBox.get()
        self.window.visitor_uuid_lbl.configure(text=visitorUUID, fg='green')
        self.window.visitor_uuid_btn.configure(text='Remove')
        return

    def documentUUIDClicked(self):
        """
            Method that will set class documentID to matching entry provided in textbox.
            Unlike visitorUUID, this entry cannot be removed once entered, only changed to another document ID.
        """
        if self.window.document_uuid_txtBox.get() == '':  # Error checking: cant submit empty doc UUID field
            messagebox.showwarning('Invalid Input', 'Please check you''ve entered a valid document UUID.')
            return
        global docUUID
        docUUID = self.window.document_uuid_txtBox.get()
        self.window.document_uuid_lbl.configure(text=docUUID, fg='green')
        self.window.document_uuid_btn.configure(text='Change document UUID')
        return

    def openJSON(self):
        """
            Method that will set class filename to filepath selected in explorer window.
            Upon receiving a valid filepath, method will make all task buttons usable.
        """
        global filename
        filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"),))
        if filename:
            self.window.json_file_lbl.configure(text='File selected!')
            self.window.json_file_lbl.configure(fg='green')
            for button in self.window.task_buttons:
                button.configure(state='normal')

    def task(self, task):
        """
            The Task Execution method.
            Firstly ensures task has been provided/not null, then makes sure that relevant entries are filled
            depending on task being executed.
            Fetches task method from class Switcher Dictionary and executes.
            Upon termination of task, will either exit program, print error message or task specific data.
        """
        if task is None:
            messagebox.showwarning('Exception Encountered',
                                   'Sorry, but this button is broken. Please restart the program.')
            self.window.destroy()  # No use in keeping a broken application open...
        if docUUID == '' and task not in ['3a', '3b', '4']:
            messagebox.showwarning("Warning", "This task requires a valid document ID.")
            return
        func = switcher.get(task, lambda: "Invalid Task")
        result = func()
        if result is not None:
            if task == '4' and isinstance(result,
                                          dict):  # Special case here as we are printing results of dictionary, which is expected behaviour
                messagebox.showinfo("Result of Task 4", message="User ID : Time spent reading (in ms) "
                                                                '\n' '%s' % result)
                return
            if task == '5' and isinstance(result, dict):
                messagebox.showwarning("Result of Task 5", message="Document ID : Number of Unique Readers "
                                                                   '\n' '%s' % result)
                return
            else:
                messagebox.showwarning("Warning", result)

    def __init__(self):
        # GUI was created using help from this tutorial:
        # https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Create-your-first-GUI-application
        # Creating the Main Window
        self.window = Tk()
        self.window.title("Industrial Programming CW2")

        # Labels and Textboxes:
        self.window.visitor_uuid_lbl = Label(self.window, text="Please enter a visitor UUID:")
        self.window.document_uuid_lbl = Label(self.window, text="Please enter a document UUID:")
        self.window.json_file_lbl = Label(self.window, text="Please select a JSON file as input:", fg="red")
        self.window.visitor_uuid_lbl.grid(column=0, row=0)
        self.window.document_uuid_lbl.grid(column=0, row=1)
        self.window.json_file_lbl.grid(column=0, row=2)

        self.window.visitor_uuid_txtBox = Entry(self.window, width=20)
        self.window.document_uuid_txtBox = Entry(self.window, width=20)
        self.window.visitor_uuid_txtBox.grid(column=1, row=0)
        self.window.document_uuid_txtBox.grid(column=1, row=1)

        self.window.visitor_uuid_btn = Button(self.window, text='Submit visitor ID', command=self.visitorUUIDClicked)
        self.window.visitor_uuid_btn.grid(column=2, row=0)
        self.window.document_uuid_btn = Button(self.window, text='Submit document UUID',
                                               command=self.documentUUIDClicked)
        self.window.document_uuid_btn.grid(column=2, row=1)
        self.window.json_file_btn = Button(self.window, text='Select JSON file', command=self.openJSON)
        self.window.json_file_btn.grid(column=2, row=2)

        # Task button arrangement
        self.window.task_separator_lbl = Label(self.window, text="Tasks", font='bold')
        self.window.task_separator_lbl.grid(column=1, row=3)
        self.window.task_buttons = []
        self.window.task2a_btn = Button(self.window, text='Task 2a', command=lambda: self.task('2a'), state='disabled')
        self.window.task2b_btn = Button(self.window, text='Task 2b', command=lambda: self.task('2b'), state='disabled')
        self.window.task3a_btn = Button(self.window, text='Task 3a', command=lambda: self.task('3a'), state='disabled')
        self.window.task3b_btn = Button(self.window, text='Task 3b', command=lambda: self.task('3b'), state='disabled')
        self.window.task4_btn = Button(self.window, text='Task 4', command=lambda: self.task('4'), state='disabled')
        self.window.task5_btn = Button(self.window, text='Task 5', command=lambda: self.task('5'), state='disabled')
        self.window.task6_btn = Button(self.window, text='Task 6', command=lambda: self.task('6'), state='disabled')
        self.window.task_buttons.append(self.window.task2a_btn)
        self.window.task_buttons.append(self.window.task2b_btn)
        self.window.task_buttons.append(self.window.task3a_btn)
        self.window.task_buttons.append(self.window.task3b_btn)
        self.window.task_buttons.append(self.window.task4_btn)
        self.window.task_buttons.append(self.window.task5_btn)
        self.window.task_buttons.append(self.window.task6_btn)

        self.window.task2a_btn.grid(column=0, row=4, pady=10)
        self.window.task2b_btn.grid(column=1, row=4, pady=10)
        self.window.task3a_btn.grid(column=2, row=4, pady=10)
        self.window.task3b_btn.grid(column=0, row=5, pady=10)
        self.window.task4_btn.grid(column=1, row=5, pady=10)
        self.window.task5_btn.grid(column=2, row=5, pady=10)
        self.window.task6_btn.grid(column=0, row=6, pady=10)

        # Running the GUI:
        self.window.mainloop()


class commandLine:  # Note that https://docs.python.org/3/library/getopt.html recommends argparse instead at the bottom
    """
        This class creates a commandLine object, which is called whenever parameters are entered in the cmdline.
        On initialization a argparser obj is created, which is then provided commands to store.
        Args are parsed into a args object to store them.
        main(self) is then executed and basic error detection is used, making sure all mandatory params have values etc.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CommandLine interface for F20SC CW2.")
        self.parser.add_argument('-u', "--userID", type=str, help="(Optional) ID of user")
        self.parser.add_argument('-d', type=str, help="(Mandatory) ID of Document")
        self.parser.add_argument('-t', type=str, help="(Mandatory) ID of task")
        self.parser.add_argument('-f', type=str, help="(Mandatory) Filepath of JSON data")
        self.args = self.parser.parse_args()
        self.main()

    def main(self):
        """
            Method called on instance execution.
            Reads in + verifies parameter entries, stores them in their respective class values and executes task
        """
        global visitorUUID
        global docUUID
        global filename
        # print(self.args)
        if self.args.userID:  # A user ID has been supplied...
            visitorUUID = self.args.userID
        if not self.args.t:
            print("Please enter a valid task ID")
            sys.exit()
        if not self.args.d and self.args.t not in ['3a', '3b', '4']:
            print("Please enter a valid document ID.")
            sys.exit()
        if not self.args.f:
            print(
                "Please enter a valid path to the file. It may help to put it in the same directory as this program.")
            sys.exit()
        docUUID = self.args.d
        filename = self.args.f
        self.cmdLineTask(self.args.t)

    def cmdLineTask(self, task):
        """
            The Task Execution method.
            Firstly ensures task has been provided/not null, then makes sure that relevant entries are filled
            depending on task being executed.
            Fetches task method from class Switcher Dictionary and executes.
            Upon termination of task, will either exit program, print error message or task specific data.
        """
        if task is None:
            print("Exception Encountered: a task hasn't been passed")
            sys.exit()  # No use in keeping a broken application open...
        if docUUID == '' and task not in ['3a', '3b', '4']:  # Only these tasks don't require a doc uuid
            print("Warning: This task requires a valid document ID.")
            sys.exit()
        func = switcher.get(task, lambda: "Invalid Task")
        result = func()
        if task == '7':  # Special case for GUI task
            return
        if result is not None:
            if task == '4' and isinstance(result, dict):  # Special case here as we are printing results of
                # dictionary, which is expected behaviour
                print("Result of Task 4 => User ID : Time spent reading (in ms) "
                      '\n' '%s' % result)
                return
            if task == '5' and isinstance(result, dict):
                print("Result of Task 5 => Document ID : Number of Other Readers "
                      '\n' '%s' % result)
                return
            print("Error: \'%s\'" % result)


# This is where the program actually begins execution...
if len(sys.argv) == 1:  # If there's more than one argument user is looking for cmdline interface
    GUI()
    sys.exit()
else:
    commandLine()
    sys.exit()
