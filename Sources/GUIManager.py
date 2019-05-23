import tkinter as tk
import tkinter.scrolledtext as scroll_text
from TaskManager import TaskManager
from tkinter.filedialog import askopenfilename

"""
Code by Lachlan Woods (lsw1@hw.ac.uk)
Files can not be copied and/or distributed without receiving permission from Lachlan Woods

GUIManager: Creates and displays a GUI if the --gui flag is set. Different tasks can be run by clicking buttons
that correspond to each task.
"""

class GUIManager:

    def __init__(self, input_doc: str, input_user: str, file: str, display):
        """
        initializer function. Sets up the GUI
        :param input_doc: The doc ID to display in the document ID input field on launch
        :param input_user: the user ID to display in the user ID input field on launch
        :param file: the file path of the json data to load
        :param display: A DisplayData object. This will be used to complete all tasks
        """
        # initilise class variables
        self.task_manager = TaskManager()  # create a new TaskManager object
        self.file_path = file
        self.display = display
        self.root = tk.Tk()
        self.root.title("issuu Data Visualiser")

        # create frames for gui sections
        self.input_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.root)
        self.output_frame = tk.Frame(self.root)
        self.input_frame.pack()
        self.button_frame.pack()
        self.output_frame.pack(expand=True, fill='both')

        # create input gui controls
        tk.Label(self.input_frame, text="Enter document ID:").grid(row=0)
        tk.Label(self.input_frame, text="Enter user ID (optional):").grid(row=1)
        self.doc_input = tk.Entry(self.input_frame, width=100, text=input_doc)
        self.user_input = tk.Entry(self.input_frame, width=100, text=input_user)
        self.doc_input.insert(0, input_doc)
        if input_user: # if a user ID was entered
            self.user_input.insert(0, input_user)
        self.file_path_text = tk.StringVar(value = "File: " + self.file_path)
        self.file_path_label = tk.Label(self.input_frame, textvariable=self.file_path_text).grid(row=2)
        self.file_button = tk.Button(self.input_frame, text="Change File", command=self.change_file)
        self.doc_input.grid(row=0, column=1)
        self.user_input.grid(row=1, column=1)
        self.file_button.grid(row=2, column=1, sticky=tk.W)

        # create buttons for each task
        self.t2a_button = tk.Button(self.button_frame, text="Views by Country (task 2a)", command=lambda: self.task_button_clicked("2a"))
        self.t2b_button = tk.Button(self.button_frame, text="Views by Continent (task 2b)", command=lambda: self.task_button_clicked("2b"))
        self.t3a_button = tk.Button(self.button_frame, text="Views by Web Browser (task 3a)", command=lambda: self.task_button_clicked("3a"))
        self.t3b_button = tk.Button(self.button_frame, text="Views by Shortened Web Browser (task 3b)", command=lambda: self.task_button_clicked("3b"))
        self.t4d_button = tk.Button(self.button_frame, text="Print 'also likes' List (task 4d)", command=lambda: self.task_button_clicked("4d"))
        self.t5_button = tk.Button(self.button_frame, text="Display 'also likes' Graph (task 5)", command=lambda: self.task_button_clicked("5"))

        # layout the buttons in a grid
        self.t2a_button.grid(row=0, column=0)
        self.t2b_button.grid(row=0, column=1)
        self.t3a_button.grid(row=0, column=2)
        self.t3b_button.grid(row=0, column=3)
        self.t4d_button.grid(row=0, column=4)
        self.t5_button.grid(row=0, column=5)

        # create a scrolling console output
        self.output_console = scroll_text.ScrolledText(self.output_frame, height=20)
        self.output_console.pack(expand=True, fill='both')

    def display_gui(self):
        """Display the gui"""
        tk.mainloop()

    def task_button_clicked(self, task: str):
        """
        Callback function for when a task button is clicked
        :param task: A string specifying the task to run
        """
        if not self.user_input.get():  # treat an empty userID filed as a None value, rather than an empty string
            uid = None
        else:
            uid = self.user_input.get()
        self.task_manager.run_task(task, self.doc_input.get(), uid, self.file_path, self.display)

    def append_to_console(self, message: str):
        """
        Append a mesage to the gui console
        :param message: The message to display
        """
        self.output_console.insert(tk.END, message + "\n")

    def change_file(self):
        """
        Callback function for when a new file is selected
        """
        new_path = askopenfilename(filetypes=[('JSON files', '.json'), ('all files', '.*')])
        if new_path:  # a new file was selected
            self.file_path_text.set("File: " + new_path)
            self.file_path = new_path


