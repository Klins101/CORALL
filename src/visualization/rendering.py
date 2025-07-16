# rendering.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

# Function to animate ship
def animate_ship(x, y, psi, loa, bol, cpa, color):
    L3 = 2*loa / 3
    W2 = 2*bol / 2

    # Calculate positions of the ship's corners
    x_mr = x - L3 * np.cos(psi)
    y_mr = y - L3 * np.sin(psi)

    x_ar = x_mr + W2 * np.sin(psi)
    y_ar = y_mr - W2 * np.cos(psi)

    x_al = x_mr - W2 * np.sin(psi)
    y_al = y_mr + W2 * np.cos(psi)

    x_fr = x + L3 * np.cos(psi) + W2 * np.sin(psi)
    y_fr = y + L3 * np.sin(psi) - W2 * np.cos(psi)

    x_fl = x + L3 * np.cos(psi) - W2 * np.sin(psi)
    y_fl = y + L3 * np.sin(psi) + W2 * np.cos(psi)

    x_fn = x + 2 * L3 * np.cos(psi)
    y_fn = y + 2 * L3 * np.sin(psi)

    # Vertices for the polygon
    vertices = 4*np.array([[x_ar, y_ar], [x_fr, y_fr], [x_fn, y_fn], [x_fl, y_fl], [x_al, y_al]])
    
    ship_polygon = Polygon(vertices, closed=True, edgecolor='black', facecolor=color)

    plt.gca().add_patch(ship_polygon)  # Add polygon to plot
    plt.axis('equal')  # Ensure equal scaling
    #plt.show(block=True) 

def animate_static_obstacle(xob, yob, cpa_ob, obs_col):
    inner_circle = Circle((xob, yob), cpa_ob, facecolor=obs_col, edgecolor='k')
    plt.gca().add_patch(inner_circle)  # Add inner circle

    outer_circle = Circle((xob, yob), cpa_ob * 2, fill=False, linestyle=':', linewidth=1.5, edgecolor=obs_col)
    plt.gca().add_patch(outer_circle)  # Add outer circle
    plt.axis('equal')

    #plt.gca().set_aspect('equal', 'box')  # Set aspect ratio
    #plt.gca().set_xlim(xob - cpa_ob * 2.5, xob + cpa_ob * 2.5)  # Set x limits for obstacle
    #plt.gca().set_ylim(yob - cpa_ob * 2.5, yob + cpa_ob * 2.5)  # Set y limits for obstacle