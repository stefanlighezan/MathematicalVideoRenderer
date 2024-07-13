import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
from VideoEditor.Editor import Editor


class Loader:
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematical Video Editor")
        self.root.geometry("1920x1080")
        self.root.configure(background="#24292e")  # GitHub dark theme background
        self.setup_gui()

    def setup_gui(self):
        self.create_project_list_frame()
        self.create_start_label_and_button()
        self.bind_events()

    def create_project_list_frame(self):
        self.project_list_frame = ttk.Frame(self.root, style="ProjectListFrame.TFrame")
        self.project_list_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)  # Increased padding

        self.project_list_scrollbar = ttk.Scrollbar(self.project_list_frame, orient=tk.VERTICAL)
        self.project_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.project_listbox = tk.Listbox(self.project_list_frame, yscrollcommand=self.project_list_scrollbar.set, font=("Helvetica", 18), width=40, background="#2f363d", foreground="#c9d1d9")  # GitHub dark theme colors
        self.project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.project_list_scrollbar.config(command=self.project_listbox.yview)

        self.populate_project_list()

    def create_start_label_and_button(self):
        self.start_label = ttk.Label(self.root, text="Welcome to Mathematical Video Editor", font=("Helvetica", 24), foreground="#c9d1d9", background="#24292e")  # GitHub dark theme colors
        self.start_label.pack(pady=50)

        self.create_project_button = ttk.Button(self.root, text="Create Project", command=self.create_project, style="CreateProjectButton.TButton")
        self.create_project_button.pack(pady=20)  # Increased padding

    def bind_events(self):
        self.project_listbox.bind("<Double-Button-1>", self.open_project_in_editor)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

    def populate_project_list(self):
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
                editor = Editor(project_directory, self.return_to_loader)
                editor.run()

    def return_to_loader(self):
        self.root.deiconify()  # Show the Loader window again

    def refresh_project_list(self):
        self.project_listbox.delete(0, tk.END)
        self.populate_project_list()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)


def create_instance():
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("ProjectListFrame.TFrame", background="#24292e")
    style.configure("CreateProjectButton.TButton", font=("Helvetica", 18), foreground="#c9d1d9", background="#2f363d")
    app = Loader(root)
    root.mainloop()


if __name__ == "__main__":
    create_instance()