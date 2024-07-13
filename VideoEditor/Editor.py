import tkinter as tk


class Editor:
    def __init__(self, project_directory):
        self.root = tk.Tk()
        self.project_directory = project_directory
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Mathematical Video Editor - Editor")
        self.root.attributes("-fullscreen", True)

        # Example: Display project directory in editor
        project_label = tk.Label(self.root, text=f"Project Directory: {self.project_directory}",
                                 font=("Helvetica", 16))
        project_label.pack(pady=50)

        # Example: Add more GUI components for the editor

    def run(self):
        self.root.mainloop()
