import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import winsound
import random

class IslandApp:

    def __init__(self, window):
        self.window = window
        self.window.title("Island Ditching")

        # Ditch matrices initialized to zeros
        self.ernest_ditch_matrix = np.zeros((100, 1))
        self.kernest_ditch_matrix = np.zeros((100, 1))

        # Create the island visualization
        self.create_island_scene()

        # Buttons to initiate digging
        self.ernest_btn = ttk.Button(window, text="Send Monkey to Ernest", command=self.send_monkey_ernest)
        self.ernest_btn.grid(row=2, column=0)

        self.kernest_btn = ttk.Button(window, text="Send Monkey to Kernest", command=self.send_monkey_kernest)
        self.kernest_btn.grid(row=2, column=1)

    def create_island_scene(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        # Ocean
        ocean = plt.Rectangle((-150, -150), 300, 300, color='blue')
        self.ax.add_artist(ocean)

        # Island
        island = plt.Circle((0, 0), 100, color='lightyellow')
        self.ax.add_artist(island)

        # Pool
        pool = plt.Rectangle((-30, -10), 60, 20, color='aqua')
        self.ax.add_artist(pool)

        self.ax.set_xlim(-150, 150)
        self.ax.set_ylim(-150, 150)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, columnspan=2)

    def dig_ditch(self, ditch_matrix, x_pos, color):
        # Choose a random starting point between the pool (0) and the sea (90)
        start_point = np.random.randint(0, 91)

        # If the starting point is closer to the sea, we dig towards the sea first
        if start_point > 45:
            for i in range(start_point, 90):  # Dig from starting point to the sea
                self.dig_at_point(i, ditch_matrix, x_pos, color)

            for i in range(start_point - 1, -1, -1):  # Dig from starting point back to the pool
                self.dig_at_point(i, ditch_matrix, x_pos, color)

        # If the starting point is closer to the pool, we dig towards the pool first
        else:
            for i in range(start_point, -1, -1):  # Dig from starting point back to the pool
                self.dig_at_point(i, ditch_matrix, x_pos, color)

            for i in range(start_point + 1, 90):  # Dig from starting point to the sea
                self.dig_at_point(i, ditch_matrix, x_pos, color)

    def dig_at_point(self, i,ditch_matrix, x_pos, color):
        if ditch_matrix[i, 0] == 0:
            ditch_matrix[i, 0] = 1
        else:
            ditch_matrix[i, 0] -= 1
            color = self.get_darker_color(color)
        self.ax.add_patch(plt.Rectangle((x_pos, 5 + i), 1, 1, color=color))
        self.canvas.draw()

    def dig_ditch(self, ditch_matrix, x_pos, color):
        starting_point = random.randint(0, 94)
        for i in range(starting_point, starting_point+6):  # Monkey digs 6 units from a random starting point
            time.sleep(0.1)
            if ditch_matrix[i, 0] < 2:  # Let’s assume they can dig up to 2 times at the same place
                ditch_matrix[i, 0] += 1
                current_color = self.get_darker_color(color, ditch_matrix[i, 0])
                self.ax.add_patch(plt.Rectangle((x_pos, 5+i), 1, 1, color=current_color))
                self.canvas.draw()

    def get_darker_color(self, base_color, depth):
        r, g, b = base_color
        factor = 0.5 ** depth  # Decreasing the brightness exponentially per digging event
        return r * factor, g * factor, b * factor

    def send_monkey_ernest(self):
        monkey_thread = threading.Thread(target=self.dig_ditch, args=(self.ernest_ditch_matrix, -25, (1, 0.6, 0.6)))  # light red
        monkey_thread.start()

    def send_monkey_kernest(self):
        monkey_thread = threading.Thread(target=self.dig_ditch, args=(self.kernest_ditch_matrix, 24, (0.8, 0.52, 0.25)))  # light brown
        monkey_thread.start()


if __name__ == "__main__":
    window = tk.Tk()
    app = IslandApp(window)
    window.mainloop()
