import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import winsound
import random
import queue
from tkinter import Button


# Add five buttons to the top line of the window
decoration = tk.Label(text="").grid(row=0, column=0)
point_button = []
sound_queue = queue.Queue()
def play_sound(frequency, duration):
    sound_queue.put((frequency, duration))
def process_sound_queue():
    while not sound_queue.empty():
        frequency, duration = sound_queue.get()
        winsound.Beep(frequency, duration)
def schedule_sound_processing():
    process_sound_queue()
    window.after(100, schedule_sound_processing)  # Check the queue every 100 ms

COLORS = {
    "yellow": (255, 255, 0),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}
for i in range(5):
    button_temp = tk.Button(text="Points: " + str(i + 1), padx=40)
    button_temp.grid(row=0, column=i + 1)
    point_button.append(button_temp)

def i_suppose_i_have_earned_so_much_points(amount_of_points):
    for i in range(5):
        point_button[i].configure(bg='gray')
    time.sleep(1)
    for i in range(amount_of_points):
        point_button[i].configure(bg='green')
        winsound.Beep(440 + i * 100, 500)

class IslandApp:
    def __init__(self, window):
        self.lock = threading.Lock()

        self.window = window
        self.window.title("Island Ditching")
        self.points_awarded = False

        self.ernest_ditch_matrix = np.zeros((100, 1))
        self.kernest_ditch_matrix = np.zeros((100, 1))
        self.pool_matrix = np.zeros((20, 60))
        self.modified_positions = np.zeros((100, 1), dtype=bool)
        self.create_island_scene()

        self.ernest_btn = ttk.Button(window, text="Send Monkey to Ernest", command=self.send_monkey_ernest)
        self.ernest_btn.grid(row=2, column=0)

        self.kernest_btn = ttk.Button(window, text="Send Monkey to Kernest", command=self.send_monkey_kernest)
        self.kernest_btn.grid(row=2, column=1)

        self.multiple_ernest_btn = ttk.Button(window, text="Send 10 Monkeys to Ernest",
                                              command=self.send_multiple_monkeys_to_ernest)
        self.multiple_ernest_btn.grid(row=3, column=0)

        self.multiple_kernest_btn = ttk.Button(window, text="Send 10 Monkeys to Kernest",
                                               command=self.send_multiple_monkeys_to_kernest)
        self.multiple_kernest_btn.grid(row=3, column=1)

        self.smart_ernest_btn = ttk.Button(window, text="Send Smart Monkeys to Ernest",
                                           command=self.start_smart_monkeys_to_ernest)
        self.smart_ernest_btn.grid(row=4, column=0)

        self.smart_kernest_btn = ttk.Button(window, text="Send Smart Monkeys to Kernest",
                                            command=self.start_smart_monkeys_to_kernest)
        self.smart_kernest_btn.grid(row=4, column=1)
        self.debug_btn = ttk.Button(window, text="debug", command=self.print_flag_status)
        self.debug_btn.grid(row=4, column=1)

        self.stop_digging_event = threading.Event()
        self.stop_digging_event.set()  # By default, allow digging

   

    def create_island_scene(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        ocean = plt.Rectangle((-150, -150), 300, 300, color='blue')
        self.ax.add_artist(ocean)

        island = plt.Circle((0, 0), 100, color='lightyellow')
        self.ax.add_artist(island)

        pool = plt.Rectangle((-30, -10), 60, 20, color='aqua')
        self.ax.add_artist(pool)

        self.ax.set_xlim(-150, 150)
        self.ax.set_ylim(-150, 150)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, columnspan=2)
        i_suppose_i_have_earned_so_much_points(1)

    def fill_ditch(self, ditch_matrix):
        ditch_matrix.fill(1)

    def get_darker_color(self, color_name_or_rgb, depth):
            if isinstance(color_name_or_rgb, str):
                base_color = COLORS.get(color_name_or_rgb)
                if not base_color:
                    raise ValueError(f"No RGB mapping found for color name {color_name_or_rgb}")
            else:
                base_color = color_name_or_rgb

            r, g, b = base_color
            factor = 1 - depth * 0.1  # Assuming you want to decrease the color by 10% per depth unit
            return (r * factor / 255, g * factor / 255, b * factor / 255)
    def check_digging_permission(self):
            # ... your code ...
            return True  # This is just a placeholder. Replace with your actual logic

    def dig_ditch(self, ditch_matrix, x_pos, color, monkeys=1):
        delay = 1 / monkeys
        for _ in range(monkeys):
            if not self.check_digging_permission():  # If digging isn't allowed, exit
                return
            time.sleep(delay)
            with self.lock:  # Ensure thread safety
                i = random.randint(0, 94)
                if ditch_matrix[i, 0] < 2:
                    ditch_matrix[i, 0] += 1
                    play_sound(300, 500)
                    current_color = self.get_darker_color(color, ditch_matrix[i, 0])
                    self.ax.add_patch(plt.Rectangle((x_pos, 5 + i), 1, 1, color=current_color))
                    self.canvas.draw()
                    print(f"Dig ditch {ditch_matrix}")

    def fill_ditch(self, ditch_matrix):
        with self.lock:  # Ensure thread safety
            ditch_matrix.fill(1)
    def modify_point(self, point, ax):  # Add ax as an argument
        if self.ernest_ditch_matrix[point, 0] < 2 and not self.modified_positions[point, 0]:
            print(f'Modifying point {point}')
            self.ernest_ditch_matrix[point, 0] += 1
            self.modified_positions[point, 0] = True

            # Drawing logic
            current_color = self.get_darker_color((1, 0.6, 0.6), self.ernest_ditch_matrix[point, 0])
            ax.add_patch(plt.Rectangle((-25, 5 + point), 1, 1, color=current_color))  # Use ax to draw
        else:
            print(f'Point {point} already modified or value >= 2')

    def send_smart_monkeys_to_ernest(self):
        print(self.ernest_ditch_matrix)
        monkey_count = 0
        while True:  # Keep sending monkeys until a break condition is met
            monkey_count += 1
            starting_point = 0  # Start from the pool side
            print(f'Monkey {monkey_count} starting at point {starting_point}')
            current_point = starting_point
            while current_point < len(self.ernest_ditch_matrix):  # Proceed towards the sea
                if not self.check_digging_permission():
                    print('Digging permission denied')
                    return
                with self.lock:
                    if self.ernest_ditch_matrix[current_point, 0] < 2:
                        self.modify_point(current_point, self.ax)  # use self.ax instead of ax
                        current_point += 1  # Move towards the sea
                    else:
                        print(f'Point {current_point} already modified or value >= 2')
                        break  # Stop digging if the point has already been modified or value >= 2
                    # Pause for a brief moment to allow the display to update
                self.canvas.draw()  # update the canvas to reflect the changes
                
                # Check if the ditch has reached the sea
                if self.ernest_ditch_matrix[-1, 0] > 0:
                    print("The ditch has reached the sea!")
                    break  # Break out of the while loop when the ditch reaches the sea
    def send_monkey_ernest(self):
        monkey_thread = threading.Thread(target=self.dig_ditch, args=(self.ernest_ditch_matrix, -25, (1, 0.6, 0.6)))
        monkey_thread.start()

    def send_monkey_kernest(self):
        monkey_thread = threading.Thread(target=self.dig_ditch, args=(self.kernest_ditch_matrix, 24, (0.8, 0.52, 0.25)))
        monkey_thread.start()

    def send_multiple_monkeys_to_ernest(self, number_of_monkeys=10):
        def thread_target():
            for _ in range(number_of_monkeys):
                starting_point = random.randint(0, 94)
                left_ditch_work = np.sum(self.ernest_ditch_matrix[0:starting_point])
                right_ditch_work = np.sum(self.ernest_ditch_matrix[starting_point:])
                dig_range = range(starting_point, -1, -1) if left_ditch_work < right_ditch_work else range(starting_point, 95)
                self.send_monkey(self.ernest_ditch_matrix, -25, 'yellow', dig_range)
        threading.Thread(target=thread_target).start()
    def send_multiple_monkeys_to_kernest(self, number_of_monkeys=10):
        def thread_target():
            for _ in range(number_of_monkeys):
                starting_point = random.randint(0, 94)
                left_ditch_work = np.sum(self.kernest_ditch_matrix[0:starting_point])
                right_ditch_work = np.sum(self.kernest_ditch_matrix[starting_point:])
                dig_range = range(starting_point, -1, -1) if left_ditch_work < right_ditch_work else range(starting_point, 95)
                self.send_monkey(self.kernest_ditch_matrix, 24, 'yellow', dig_range)
        threading.Thread(target=thread_target).start()
    def send_smart_monkeys_to_kernest(self):
        print(self.kernest_ditch_matrix)
        monkey_count = 0
        while True:  # Keep sending monkeys until a break condition is met
            monkey_count += 1
            starting_point = 0  # Start from the pool side
            print(f'Monkey {monkey_count} starting at point {starting_point}')
            current_point = starting_point
            while current_point < len(self.kernest_ditch_matrix):  # Proceed towards the sea
                if not self.check_digging_permission():
                    print('Digging permission denied')
                    return
                with self.lock:
                    if self.kernest_ditch_matrix[current_point, 0] < 2:
                        self.modify_point_kernest(current_point, self.ax)  # use self.ax instead of ax
                        current_point += 1  # Move towards the sea
                    else:
                        print(f'Point {current_point} already modified or value >= 2')
                        break  # Stop digging if the point has already been modified or value >= 2
                    # Pause for a brief moment to allow the display to update
                self.canvas.draw()  # update the canvas to reflect the changes

                # Check if the ditch has reached the sea
                if self.kernest_ditch_matrix[-1, 0] > 0:
                    print("The ditch has reached the sea!")
                    break  # Break out of the while loop when the ditch reaches the sea
    def modify_point_kernest(self, point, ax):
        if self.kernest_ditch_matrix[point, 0] < 2 and not self.modified_positions[point, 0]:
            print(f'Modifying point {point}')
            self.kernest_ditch_matrix[point, 0] += 1
            self.modified_positions[point, 0] = True

            # Drawing logic
            current_color = self.get_darker_color((0.8, 0.52, 0.25), self.kernest_ditch_matrix[point, 0])
            ax.add_patch(plt.Rectangle((24, 5 + point), 1, 1, color=current_color))  # Adjusted coordinates for Kernest
        else:
            print(f'Point {point} already modified or value >= 2')
    def print_flag_status(self):
            print(f'Ernesti Access Achieved: {self.ernesti_access_achieved}')
            print(f'Kernesti Access Achieved: {self.kernesti_access_achieved}')

    def start_smart_monkeys_to_ernest(self):
        monkey_thread = threading.Thread(target=self.send_smart_monkeys_to_ernest)
        monkey_thread.start()

    def start_smart_monkeys_to_kernest(self):
        monkey_thread = threading.Thread(target=self.send_smart_monkeys_to_kernest)
        monkey_thread.start()

def seawater_access(ditch_matrix):
    """Check if seawater has access to the ditch."""
    # Check if any element in the last row of the ditch matrix is greater than 0
    return np.any(ditch_matrix[-1, :] > 0)

def seawater_thread(app):
    while True:
        time.sleep(0.1)  # Check every 0.1 second
        with app.lock:  # Ensure thread safety
            ernesti_access = seawater_access(app.ernest_ditch_matrix)
            kernesti_access = seawater_access(app.kernest_ditch_matrix)
            if ernesti_access and not app.ernesti_access_achieved:
                print("Ernesti ditch has connected to the sea!")
                play_sound(500, 500)
                app.ernesti_access_achieved = True  # Set a flag to indicate Ernesti's ditch access
                app.fill_ditch(app.ernest_ditch_matrix)
                
                    
  # Play sound effect for water filling the ditch
                if kernesti_access and not app.kernesti_access_achieved:
                    print("Kernesti ditch has connected to the sea!")
                    play_sound(500, 500)
                    app.kernesti_access_achieved = True  # Set a flag to indicate Kernesti's ditch access
                    app.fill_ditch(app.kernest_ditch_matrix)



# Create a function to print the pool status message
def print_pool_status():
    to_fill = 20 * 60 - app.pool_matrix.sum()
    fill_amount = min(20, to_fill)
    print(f"Pool to fill: {to_fill}, Fill amount: {fill_amount}")



# Modify the pool_thread function to remove the print statement for status
def pool_thread(app):
    total_time = 20.0  # Total time to fill the pool in seconds
    fill_rate = 20 * 60 / total_time  # Units to fill per second to meet the target

    timer = 0  # Initialize a timer variable
    while True:
        time.sleep(0.1)  # Check every 0.1 second
        timer += 0.1  # Increment the timer by 0.1 seconds

        with app.lock:  # Ensure thread safety
            if app.ernesti_access_achieved or app.kernesti_access_achieved:
                # Calculate the amount to fill based on the fill_rate
                to_fill = fill_rate * timer
                fill_amount = min(20, to_fill)  # Filling 20 units at a time, but don't overflow
                app.pool_matrix[: fill_amount // 60, : fill_amount % 60] = 1
                if fill_amount > 0:
                    play_sound(600, 500)  # Play sound effect for water filling the pool

            if timer >= total_time:  # Check if 20 seconds have elapsed
                timer = 0  # Reset the timer to 0

            if app.pool_matrix.sum() == 20 * 60:  # If the pool is full
                if app.ernesti_access_achieved:
                    play_sound(300, 10000)  # Low beep for 10 seconds if Ernest's ditch finished first
                elif app.kernesti_access_achieved:
                    play_sound(800, 10000)  # High beep for 10 seconds if Kernest's ditch finished first

                i_suppose_i_have_earned_so_much_points(5)  # Award 5 points
                break  # Exit the loop to stop the thread


if __name__ == "__main__":
    window = tk.Tk()
    app = IslandApp(window)
    app.ernesti_access_achieved = False  # Initialize flags
    app.kernesti_access_achieved = False  # Initialize flags
    sea_thread = threading.Thread(target=seawater_thread, args=(app,))
    pool_fill_thread = threading.Thread(target=pool_thread, args=(app,))
    sea_thread.start()
    pool_fill_thread.start()
    app.print_flag_status()
    schedule_sound_processing()
    window.mainloop()
