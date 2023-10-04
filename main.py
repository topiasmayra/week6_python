import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import time

# Create a Tkinter window
window = tk.Tk()
window.title("Exercise 5")
window.geometry("700x700")

# Add five buttons to the top line of the window
decoration = tk.Label(window, text="").grid(row=0, column=0)
point_button = []

for i in range(5):
    button_temp = tk.Button(window, text="Points: " + str(i + 1), padx=40)
    button_temp.grid(row=0, column=i + 1)
    point_button.append(button_temp)

def i_suppose_i_have_earned_so_much_points(amount_of_points):
    for i in range(5):
        point_button[i].configure(bg='gray')
    time.sleep(1)
    for i in range(amount_of_points):
        point_button[i].configure(bg='green')
        winsound.Beep(440 + i * 100, 500)


# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Create the ocean as a blue background
ocean = plt.Rectangle((-1, -1), 2, 2, color='blue')
ax.add_artist(ocean)

# Create the island as a white circle
island = plt.Circle((0, 0), 1, color='white')
ax.add_artist(island)

# Create the sandy beach as a lighter shade of yellow
beach = plt.Circle((0, 0), 0.95, color='lightyellow')
ax.add_artist(beach)

# Define the pool as a 20x60 matrix filled with zeros
pool_height = 20
pool_width = 60
pool_matrix = np.zeros((pool_height, pool_width))



# Position the pool on the island
pool_x, pool_y = 0, 0
pool_width, pool_length = 0.2, 0.6

# Position the ditches on the island with the previous orientation
ernest_ditch_x, ernest_ditch_y = pool_x - pool_length / 2, pool_y
kernest_ditch_x, kernest_ditch_y = pool_x + pool_length / 2, pool_y

# Adjust the orientation of the ditches to face north
ernest_ditch_orientation = plt.Line2D((ernest_ditch_x, ernest_ditch_x), (0, 1.2), lw=2, color='red')
kernest_ditch_orientation = plt.Line2D((kernest_ditch_x, kernest_ditch_x), (0, 1.2), lw=2, color='red')
ax.add_artist(ernest_ditch_orientation)
ax.add_artist(kernest_ditch_orientation)

# Plot the pool
pool_rect = plt.Rectangle((pool_x - pool_length/2, pool_y - pool_width/2), pool_length, pool_width, color='cyan', alpha=0.7)
ax.add_artist(pool_rect)

# Set the limits and aspect ratio
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')

# Add labels for reference
plt.text(ernest_ditch_x - 0.3, ernest_ditch_y + 0.2, "Ernest", color='red')
plt.text(kernest_ditch_x + 0.2, kernest_ditch_y + 0.2, "Kernest's", color='red')

# Hide axes
ax.axis('off')

# Create a canvas to embed the Matplotlib plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, columnspan=6)  # Adjust the row and column as needed

import numpy as np

# Define the size of the ditches
ditch_length = 100
ditch_width = 1

# Create the matrices for Ernest's ditch and Kernest's ditch
ernest_ditch_matrix = np.zeros((ditch_length, ditch_width))
kernest_ditch_matrix = np.zeros((ditch_length, ditch_width))

# Draw Ernest's ditch (set the values to 1)
ernest_ditch_matrix[10:110, :] = 1  # For example, starting from row 10 to row 109

# Draw Kernest's ditch (set the values to 1)
kernest_ditch_matrix[20:120, :] = 1  # For example, starting from row 20 to row 119


# Start the Tkinter event loop
window.mainloop()
