import tkinter as tk
from tkinter import Menu, simpledialog, colorchooser
import time
import sympy as sp


class Editor:
    def __init__(self, project_directory, return_to_loader_callback):
        self.quality_scale = 100
        self.root = tk.Tk()
        self.root.geometry("1920x1080")
        self.project_directory = project_directory
        self.return_to_loader_callback = return_to_loader_callback
        self.setup_gui()
        self.load_project()
        self.setup_defaults()

    def setup_defaults(self):
        self.default_functions = ["y = x"]
        self.default_graph_colors = ["blue"]
        self.default_bg_color = "white"
        self.default_tick_spacing = 10
        self.default_animation_speed = 0.1
        self.default_show_tick_marks = True
        self.default_tick_mark_color = "black"
        self.default_axis_line_color = "black"
        self.default_quality = 100

    def save_project(self):
        functions_text = self.functions_entry.get().split("\n") if self.functions_entry.get() else self.default_functions
        graph_colors = self.graph_colors_entry.get().split("\n") if self.graph_colors_entry.get() else self.default_graph_colors
        bg_color = self.bg_color_entry.get() if self.bg_color_entry.get() else self.default_bg_color
        tick_spacing = self.tick_spacing_scale.get()
        quality = self.quality_scale.get()
        animation_speed = float(self.speed_entry.get()) if self.speed_entry.get() else self.default_animation_speed
        show_tick_marks = self.show_tick_marks_var.get()
        tick_mark_color = self.tick_mark_color_entry.get() if self.tick_mark_color_entry.get() else self.default_tick_mark_color
        axis_line_color = self.axis_line_color_entry.get() if self.axis_line_color_entry.get() else self.default_axis_line_color

        with open(f"{self.project_directory}/save.txt", "w") as f:
            f.write(f"functions_text={'|'.join(functions_text)}\n")
            f.write(f"graph_colors={'|'.join(graph_colors)}\n")
            f.write(f"bg_color={bg_color}\n")
            f.write(f"tick_spacing={tick_spacing}\n")
            f.write(f"quality={quality}\n")
            f.write(f"animation_speed={animation_speed}\n")
            f.write(f"show_tick_marks={show_tick_marks}\n")
            f.write(f"tick_mark_color={tick_mark_color}\n")
            f.write(f"axis_line_color={axis_line_color}\n")

    def load_project(self):
        try:
            with open(f"{self.project_directory}/save.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key == "functions_text":
                        self.functions_entry.delete(1.0, tk.END)
                        self.functions_entry.insert(tk.END, value.replace("|", "\n"))
                    elif key == "graph_colors":
                        self.graph_colors_entry.delete(1.0, tk.END)
                        self.graph_colors_entry.insert(tk.END, value.replace("|", "\n"))
                    elif key == "bg_color":
                        self.bg_color_entry.delete(0, tk.END)
                        self.bg_color_entry.insert(0, value)
                    elif key == "tick_spacing":
                        self.tick_spacing_scale.set(int(value))
                    elif key == "quality":
                        self.quality_scale.set(int(value))
                    elif key == "animation_speed":
                        self.speed_entry.delete(0, tk.END)
                        self.speed_entry.insert(0, value)
                    elif key == "show_tick_marks":
                        self.show_tick_marks_var.set(bool(value))
                    elif key == "tick_mark_color":
                        self.tick_mark_color_entry.delete(0, tk.END)
                        self.tick_mark_color_entry.insert(0, value)
                    elif key == "axis_line_color":
                        self.axis_line_color_entry.delete(0, tk.END)
                        self.axis_line_color_entry.insert(0, value)
        except FileNotFoundError:
            pass

    def setup_gui(self):
        self.root.title("Mathematical Video Editor - Editor")
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open New File", command=self.open_new_file)
        file_menu.add_command(label="Save", command=self.save_project)
        file_menu.add_command(label="Return to Loader", command=self.return_to_loader)
        menu_bar.add_cascade(label="File", menu=file_menu)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        inspector_width = int(self.root.winfo_screenwidth() * 0.3)
        self.inspector_frame = tk.Frame(main_frame, width=inspector_width, bg="lightgray")
        self.inspector_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.inspector_frame.pack_propagate(False)

        inspector_label = tk.Label(self.inspector_frame, text="Inspector", font=("Helvetica", 14))
        inspector_label.pack(pady=10)

        functions_label = tk.Label(self.inspector_frame, text="Functions (one per line, e.g., y = x):")
        functions_label.pack(pady=5)
        self.functions_entry = tk.Text(self.inspector_frame, height=5)
        self.functions_entry.pack(pady=5)

        graph_colors_label = tk.Label(self.inspector_frame, text="Graph Colors (one per line):")
        graph_colors_label.pack(pady=5)
        self.graph_colors_entry = tk.Text(self.inspector_frame, height=5)
        self.graph_colors_entry.pack(pady=5)

        bg_color_label = tk.Label(self.inspector_frame, text="Background Color:")
        bg_color_label.pack(pady=5)
        self.bg_color_entry = tk.Entry(self.inspector_frame)
        self.bg_color_entry.pack(pady=5)

        tick_spacing_label = tk.Label(self.inspector_frame, text="Tick Mark Spacing:")
        tick_spacing_label.pack(pady=5)
        self.tick_spacing_scale = tk.Scale(self.inspector_frame, from_=1, to=50, orient=tk.HORIZONTAL)
        self.tick_spacing_scale.pack(pady=5)

        quality_label = tk.Label(self.inspector_frame, text="Quality Of Graph:")
        quality_label.pack(pady=5)
        self.quality_scale = tk.Scale(self.inspector_frame, from_=1, to=100000, orient=tk.HORIZONTAL)
        self.quality_scale.pack(pady=5)

        speed_label = tk.Label(self.inspector_frame, text="Animation Speed (seconds):")
        speed_label.pack(pady=5)
        self.speed_entry = tk.Entry(self.inspector_frame)
        self.speed_entry.pack(pady=5)

        self.show_tick_marks_var = tk.BooleanVar()
        show_tick_marks_check = tk.Checkbutton(self.inspector_frame, text="Show Tick Marks",
                                               variable=self.show_tick_marks_var)
        show_tick_marks_check.pack(pady=5)

        tick_mark_color_label = tk.Label(self.inspector_frame, text="Tick Mark Color:")
        tick_mark_color_label.pack(pady=5)
        self.tick_mark_color_entry = tk.Entry(self.inspector_frame)
        self.tick_mark_color_entry.pack(pady=5)

        axis_line_color_label = tk.Label(self.inspector_frame, text="Axis Line Color:")
        axis_line_color_label.pack(pady=5)
        self.axis_line_color_entry = tk.Entry(self.inspector_frame)
        self.axis_line_color_entry.pack(pady=5)

        rerender_button = tk.Button(self.inspector_frame, text="Rerender", command=self.draw_graph_animation)
        rerender_button.pack(pady=10)

        draw_graph_button = tk.Button(self.inspector_frame, text="Draw a graph animation",
                                      command=self.draw_graph_animation)
        draw_graph_button.pack(pady=10)

        self.video_frame = tk.Frame(main_frame, bg="black")
        self.video_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.video_frame.pack_propagate(False)

        self.preview_label = tk.Label(self.video_frame, text="Video Playback", font=("Helvetica", 14), fg="white",
                                      bg="black")
        self.preview_label.pack(pady=10, expand=True)

        self.root.bind("<Control-plus>", self.zoom_in)
        self.root.bind("<Control-minus>", self.zoom_out)

    def open_new_file(self):
        pass

    def return_to_loader(self):
        self.root.destroy()
        self.return_to_loader_callback()

    def draw_graph_animation(self):
        canvas_width = self.video_frame.winfo_width()
        canvas_height = self.video_frame.winfo_height()

        self.clear_video_frame()

        functions_text = self.functions_entry.get("1.0", tk.END).strip().split("\n")
        graph_colors = self.graph_colors_entry.get("1.0", tk.END).strip().split("\n")
        bg_color = self.bg_color_entry.get() if self.bg_color_entry.get() else self.default_bg_color
        tick_spacing = self.tick_spacing_scale.get()
        quality = self.quality_scale.get()
        animation_speed = float(self.speed_entry.get()) if self.speed_entry.get() else self.default_animation_speed
        show_tick_marks = self.show_tick_marks_var.get()
        tick_mark_color = self.tick_mark_color_entry.get() if self.tick_mark_color_entry.get() else self.default_tick_mark_color
        axis_line_color = self.axis_line_color_entry.get() if self.axis_line_color_entry.get() else self.default_axis_line_color

        self.canvas = tk.Canvas(self.video_frame, width=canvas_width, height=canvas_height, bg=bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill=axis_line_color,
                                width=2)
        self.canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill=axis_line_color,
                                width=2)

        if show_tick_marks:
            for x in range(-10 * tick_spacing, 11 * tick_spacing, tick_spacing):
                x_pixel = x * 20 + canvas_width / 2
                self.canvas.create_line(x_pixel, canvas_height / 2 - 5, x_pixel, canvas_height / 2 + 5,
                                        fill=tick_mark_color)
                self.canvas.create_text(x_pixel, canvas_height / 2 + 10, text=str(x), anchor=tk.N)

            for y in range(-10 * tick_spacing, 11 * tick_spacing, tick_spacing):
                y_pixel = -y * 20 + canvas_height / 2
                self.canvas.create_line(canvas_width / 2 - 5, y_pixel, canvas_width / 2 + 5, y_pixel,
                                        fill=tick_mark_color)
                self.canvas.create_text(canvas_width / 2 - 20, y_pixel, text=str(y), anchor=tk.E)

        for idx, function_text in enumerate(functions_text):
            graph_color = graph_colors[idx] if idx < len(graph_colors) else self.default_graph_colors[0]
            try:
                step_size = 1 / quality
                points = []
                x = sp.symbols('x')
                expr = sp.sympify(function_text.replace("y = ", ""))
                for i in range(-10 * tick_spacing, 11 * tick_spacing):
                    x_normalized = i / tick_spacing
                    y = expr.evalf(subs={x: x_normalized}) * tick_spacing
                    points.append((i * 20 + canvas_width / 2, -y * 20 + canvas_height / 2))

                if len(points) > 1:
                    point_delay = animation_speed / len(points)
                    for i in range(len(points) - 1):
                        p1 = points[i]
                        p2 = points[i + 1]
                        self.canvas.create_line(p1, p2, fill=graph_color, width=2, smooth=True, splinesteps=10)
                        self.root.update()
                        time.sleep(point_delay)
            except Exception as e:
                print(f"Error: {e}")

    def clear_video_frame(self):
        for widget in self.video_frame.winfo_children():
            widget.destroy()

    def zoom_in(self, event):
        self.zoom_level += 0.1
        self.apply_zoom()

    def zoom_out(self, event):
        self.zoom_level = max(0.1, self.zoom_level - 0.1)
        self.apply_zoom()

    def apply_zoom(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        self.canvas.scale("all", center_x, center_y, self.zoom_level, self.zoom_level)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run(self):
        self.root.mainloop()


# Example usage
def return_to_loader_callback():
    print("Returning to loader...")
