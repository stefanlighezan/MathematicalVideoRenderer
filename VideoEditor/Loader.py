import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar
import os
from VideoEditor.Editor import Editor  # Assuming Editor.py is in the same directory as Loader.py


class Loader:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Mathematical Video Editor")
        self.root.geometry("800x600")
        self.root.attributes("-fullscreen", True)

        # Create a frame to hold project list and scrollbar
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Calculate the width for the project list (15% of the screen width)
        screen_width = self.root.winfo_screenwidth()
        listbox_width = int(screen_width * 0.15)

        # Create scrollbar
        scrollbar = Scrollbar(frame, orient=tk.VERTICAL, width=listbox_width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create listbox for projects
        self.project_listbox = Listbox(frame, yscrollcommand=scrollbar.set, font=("Helvetica", 12), width=listbox_width)
        self.project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar to work with listbox
        scrollbar.config(command=self.project_listbox.yview)

        # Populate project list (for demo, you can fetch actual projects here)
        self.populate_project_list()

        # Bind double click event to open project in Editor
        self.project_listbox.bind("<Double-Button-1>", self.open_project_in_editor)

        # Bind fullscreen handling
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Example label and button for creating projects
        start_label = tk.Label(self.root, text="Welcome to Mathematical Video Editor", font=("Helvetica", 20))
        start_label.pack(pady=50)

        create_project_button = tk.Button(self.root, text="Create Project", command=self.create_project)
        create_project_button.pack()

    def populate_project_list(self):
        # For demo purposes, populate the list with example projects
        projects_dir = os.path.join(os.path.dirname(__file__), "Projects")
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        projects = [name for name in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, name))]
        projects.sort(key=lambda x: os.path.getmtime(os.path.join(projects_dir, x)), reverse=True)

        for project in projects:
            self.project_listbox.insert(tk.END, project)

    def create_project(self):
        project_name = simpledialog.askstring("Create Project", "Enter project name:")
        if project_name:
            project_directory = os.path.join(os.path.dirname(__file__), "Projects", project_name)
            try:
                os.makedirs(project_directory)
                messagebox.showinfo("Project Created", f"Project '{project_name}' created successfully!")
                self.refresh_project_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create project: {e}")

    def open_project_in_editor(self, event):
        selected_index = self.project_listbox.curselection()
        if selected_index:
            project_name = self.project_listbox.get(selected_index)
            project_directory = os.path.join(os.path.dirname(__file__), "Projects", project_name)
            if os.path.exists(project_directory):
                self.root.withdraw()  # Hide the Loader window
                open_editor(project_directory)

    def refresh_project_list(self):
        # Clear and repopulate the project list
        self.project_listbox.delete(0, tk.END)
        self.populate_project_list()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)


def open_editor(project_directory):
    editor_app = Editor(project_directory)
    editor_app.run()


def create_instance():
    root = tk.Tk()
    app = Loader(root)
    root.mainloop()
