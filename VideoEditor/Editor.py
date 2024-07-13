import math
import tkinter as tk
from tkinter import Menu, simpledialog, colorchooser
import time

class Editor:
    def __init__(self, project_directory, return_to_loader_callback):
        self.root = tk.Tk()
        self.root.geometry("1920x1080")
        self.project_directory = project_directory
        self.return_to_loader_callback = return_to_loader_callback
        self.setup_gui()

        # Default values
        self.default_function = "y = x"
        self.default_graph_color = "blue"
        self.default_bg_color = "white"
        self.default_tick_spacing = 10
        self.default_animation_speed = 0.1
        self.default_show_tick_marks = True
        self.default_tick_mark_color = "black"
        self.default_axis_line_color = "black"
        self.default_quality = 100

        # Initialize input fields with default values
        self.function_entry.insert(0, self.default_function)
        self.graph_color_entry.insert(0, self.default_graph_color)
        self.bg_color_entry.insert(0, self.default_bg_color)
        self.tick_spacing_scale.set(self.default_tick_spacing)
        self.speed_entry.insert(0, str(self.default_animation_speed))
        self.show_tick_marks_var.set(self.default_show_tick_marks)
        self.tick_mark_color_entry.insert(0, self.default_tick_mark_color)
        self.axis_line_color_entry.insert(0, self.default_axis_line_color)
        self.quality_scale.set(self.default_quality)

    def setup_gui(self):
        self.root.title("Mathematical Video Editor - Editor")

        # Create menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open New File", command=self.open_new_file)
        file_menu.add_command(label="Return to Loader", command=self.return_to_loader)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Main frames layout
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Inspector frame (30% width)
        inspector_width = int(self.root.winfo_screenwidth() * 0.3)
        self.inspector_frame = tk.Frame(main_frame, width=inspector_width, bg="lightgray")
        self.inspector_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.inspector_frame.pack_propagate(False)  # Prevent resizing based on contents

        # Inspector label
        inspector_label = tk.Label(self.inspector_frame, text="Inspector", font=("Helvetica", 14))
        inspector_label.pack(pady=10)

        # Function entry
        function_label = tk.Label(self.inspector_frame, text="Function (e.g., y = x):")
        function_label.pack(pady=5)
        self.function_entry = tk.Entry(self.inspector_frame)
        self.function_entry.pack(pady=5)

        # Graph color entry
        graph_color_label = tk.Label(self.inspector_frame, text="Graph Color:")
        graph_color_label.pack(pady=5)
        self.graph_color_entry = tk.Entry(self.inspector_frame)
        self.graph_color_entry.pack(pady=5)

        # Background color entry
        bg_color_label = tk.Label(self.inspector_frame, text="Background Color:")
        bg_color_label.pack(pady=5)
        self.bg_color_entry = tk.Entry(self.inspector_frame)
        self.bg_color_entry.pack(pady=5)

        # Tick mark spacing
        tick_spacing_label = tk.Label(self.inspector_frame, text="Tick Mark Spacing:")
        tick_spacing_label.pack(pady=5)
        self.tick_spacing_scale = tk.Scale(self.inspector_frame, from_=1, to=50, orient=tk.HORIZONTAL)
        self.tick_spacing_scale.pack(pady=5)

        # Quality of graph
        quality_label = tk.Label(self.inspector_frame, text="Quality Of Graph:")
        quality_label.pack(pady=5)
        self.quality_scale = tk.Scale(self.inspector_frame, from_=1, to=100000, orient=tk.HORIZONTAL)
        self.quality_scale.pack(pady=5)

        # Animation speed
        speed_label = tk.Label(self.inspector_frame, text="Animation Speed (seconds):")
        speed_label.pack(pady=5)
        self.speed_entry = tk.Entry(self.inspector_frame)
        self.speed_entry.pack(pady=5)

        # Show tick marks
        self.show_tick_marks_var = tk.BooleanVar()
        show_tick_marks_check = tk.Checkbutton(self.inspector_frame, text="Show Tick Marks",
                                               variable=self.show_tick_marks_var)
        show_tick_marks_check.pack(pady=5)

        # Tick mark color
        tick_mark_color_label = tk.Label(self.inspector_frame, text="Tick Mark Color:")
        tick_mark_color_label.pack(pady=5)
        self.tick_mark_color_entry = tk.Entry(self.inspector_frame)
        self.tick_mark_color_entry.pack(pady=5)

        # Axis line color
        axis_line_color_label = tk.Label(self.inspector_frame, text="Axis Line Color:")
        axis_line_color_label.pack(pady=5)
        self.axis_line_color_entry = tk.Entry(self.inspector_frame)
        self.axis_line_color_entry.pack(pady=5)

        # Rerender button
        rerender_button = tk.Button(self.inspector_frame, text="Rerender", command=self.draw_graph_animation)
        rerender_button.pack(pady=10)

        # Inspector button for drawing graph animation
        draw_graph_button = tk.Button(self.inspector_frame, text="Draw a graph animation", command=self.draw_graph_animation)
        draw_graph_button.pack(pady=10)

        # Video playback frame (70% remaining space, right side)
        self.video_frame = tk.Frame(main_frame, bg="black")
        self.video_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.video_frame.pack_propagate(False)  # Prevent resizing based on contents

        # Placeholder labels for video playback
        self.preview_label = tk.Label(self.video_frame, text="Video Playback", font=("Helvetica", 14), fg="white", bg="black")
        self.preview_label.pack(pady=10, expand=True)

    def open_new_file(self):
        # Placeholder for opening a new file
        pass

    def return_to_loader(self):
        self.root.destroy()  # Destroy the Editor window
        self.return_to_loader_callback()

    def draw_graph_animation(self):
        canvas_width = self.video_frame.winfo_width()
        canvas_height = self.video_frame.winfo_height()

        # Clear previous animation
        self.clear_video_frame()

        # Retrieve input values
        function_text = self.function_entry.get() if self.function_entry.get() else self.default_function
        graph_color = self.graph_color_entry.get() if self.graph_color_entry.get() else self.default_graph_color
        bg_color = self.bg_color_entry.get() if self.bg_color_entry.get() else self.default_bg_color
        tick_spacing = self.tick_spacing_scale.get()
        quality = self.quality_scale.get()
        animation_speed = float(self.speed_entry.get()) if self.speed_entry.get() else self.default_animation_speed
        show_tick_marks = self.show_tick_marks_var.get()
        tick_mark_color = self.tick_mark_color_entry.get() if self.tick_mark_color_entry.get() else self.default_tick_mark_color
        axis_line_color = self.axis_line_color_entry.get() if self.axis_line_color_entry.get() else self.default_axis_line_color

        # Create canvas for animation
        canvas = tk.Canvas(self.video_frame, width=canvas_width, height=canvas_height, bg=bg_color)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Draw axis lines
        canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill=axis_line_color, width=2)  # X-axis
        canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill=axis_line_color, width=2)  # Y-axis

        # Draw tick marks on the axes if enabled
        if show_tick_marks:
            for x in range(-10 * tick_spacing, 11 * tick_spacing, tick_spacing):
                x_pixel = x * 20 + canvas_width / 2
                canvas.create_line(x_pixel, canvas_height / 2 - 5, x_pixel, canvas_height / 2 + 5, fill=tick_mark_color)
                canvas.create_text(x_pixel, canvas_height / 2 + 10, text=str(x), anchor=tk.N)

            for y in range(-10 * tick_spacing, 11 * tick_spacing, tick_spacing):
                y_pixel = -y * 20 + canvas_height / 2
                canvas.create_line(canvas_width / 2 - 5, y_pixel, canvas_width / 2 + 5, y_pixel, fill=tick_mark_color)
                canvas.create_text(canvas_width / 2 - 20, y_pixel, text=str(y), anchor=tk.E)

        # Draw graph animation with improved quality
        try:
            # Calculate step size based on quality
            step_size = 1 / quality
            prev_x = None
            prev_y = None
            for x in range(-10 * tick_spacing, 11 * tick_spacing):
                x_normalized = x / tick_spacing
                # Evaluate function
                function_text = function_text.replace("y = ", "")
                y = eval(function_text.replace("x", str(x_normalized)))
                if prev_x is not None and prev_y is not None:
                    canvas.create_line(prev_x, prev_y, x * 20 + canvas_width / 2, -y * 20 + canvas_height / 2,
                                       fill=graph_color, width=2)
                    self.root.update()
                    time.sleep(animation_speed)
                prev_x = x * 20 + canvas_width / 2
                prev_y = -y * 20 + canvas_height / 2
        except Exception as e:
            print(f"Error: {e}")

    def clear_video_frame(self):
        # Clear previous content in video frame
        for widget in self.video_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

# Example usage
def return_to_loader_callback():
    print("Returning to loader...")
