import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np
import sys
import math
import matplotlib.patches as patches
from matplotlib.widgets import Button

from calculations import read_in_geometry, add_boundary, get_vector_count, set_vector_count, clear_bmxb, add_boundary, get_lines, detect_nearest_collision, euclidean_distance

#GLOBAL VARIABLE
VECTOR_HASH = {}




def draw_geometry(ax):

    LINES = get_lines()
    for line in LINES :
        firstPoint = line[0]
        secondPoint = line[1]

        add_vector_to_graph_points(ax, firstPoint, secondPoint)


def shoot_vector(ax, start_point, theta) :
    
    #find the first collision
    collision_point, theta_reflection, recurse = detect_nearest_collision(start_point, theta)
    
    print(" Collsion Point: ", collision_point, "reflection_theta: ", theta_reflection, "recurse: ", recurse)

    if(collision_point[0] != None and collision_point[1] != None) :
        #draw the vector and collisionn
        add_vector_to_graph_points(ax, start_point, collision_point)

    vc = get_vector_count()    
    set_vector_count(vc + 1)
    if(recurse):
        shoot_vector(ax, collision_point, theta_reflection)

def add_vector_to_graph_points(ax, start_point, end_point, color='red'):
    """
    Add a vector to a Matplotlib axis.

    Parameters:
    - ax (matplotlib.axes._axes.Axes): The Matplotlib axis to which the vector will be added.
    - start_point (tuple): Tuple containing the (x, y) coordinates of the starting point of the vector.
    - end_point (tuple): Tuple containing the (x, y) coordinates of the end point of the vector.
    - color (str, optional): The color of the vector. Default is 'red'.

    Returns:
    - None
    """
    x_start, y_start = start_point
    x_end, y_end = end_point

    # Calculate the components of the vector
    x_component = x_end - x_start
    y_component = y_end - y_start

    # Plot the vector using quiver on the existing axis (ax)
    ax.quiver(x_start, y_start, x_component, y_component, angles='xy', scale_units='xy', scale=1, color=color, width=.002, headaxislength=0, headlength=0)


def add_vector_to_graph(ax, x, y, angle_degrees, length, color='red'):
    """
    Add a vector to a Matplotlib axis.

    Parameters:
    - ax (matplotlib.axes._axes.Axes): The Matplotlib axis to which the vector will be added.
    - x (float): The x-coordinate of the starting point of the vector.
    - y (float): The y-coordinate of the starting point of the vector.
    - angle_degrees (float): The angle of the vector in degrees (measured counterclockwise from the positive x-axis).
    - length (float): The length of the vector.
    - color (str, optional): The color of the vector. Default is 'red'.

    Returns:
    - None
    """
    angle_radians = np.radians(angle_degrees)
    x_component = length * np.cos(angle_radians)
    y_component = length * np.sin(angle_radians)

    # Plot the vector using quiver on the existing axis (ax)
    ax.quiver(x, y, x_component, y_component, angles='xy', scale_units='xy', scale=1, color=color, width=.002, headaxislength=0, headlength=0)

def draw_checkerboard_just_ax(rows, cols, square_size, ax):
    """
    Draw a checkerboard pattern on a Matplotlib axis.

    Parameters:
    - rows (int): Number of rows in the checkerboard.
    - cols (int): Number of columns in the checkerboard.
    - square_size (float): Size of each square in the checkerboard.
    - ax (matplotlib.axes._axes.Axes): The Matplotlib axis on which the checkerboard will be drawn.

    Returns:
    - matplotlib.axes._axes.Axes: The same Matplotlib axis with the checkerboard drawn.
    """

    for row in range(rows):
        for col in range(cols):
            # Set all squares to white
            color = 'white' #if (row + col) % 2 == 0 else '#d3d3d3'
            
            ax.add_patch(plt.Rectangle((col * square_size, row * square_size), square_size, square_size,
                                       facecolor=color))#edgecolor='black'))

    ax.set_xlim(0, cols * square_size)
    ax.set_ylim(0, rows * square_size)
    ax.set_aspect('equal', adjustable='box')

    # Show x and y axes
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Add labels to x and y axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Space')

    return ax



def find_first_intersection_point(x, y, angle_degrees, width, height):
    """
    Find the first intersection point of a vector within the checkerboard grid.

    Parameters:
    - x (float): The x-coordinate of the starting point of the vector.
    - y (float): The y-coordinate of the starting point of the vector.
    - angle_degrees (float): The angle of the vector in degrees (measured counterclockwise from the positive x-axis).
    - width  (int)  : Defines the width of the graph
    - height (int)  : Defines the height of the graph

    Returns:
    - tuple or None: The coordinates of the first intersection point, or None if no intersection point is found within the grid.
    """
    
    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate slope of the vector
    slope = np.tan(angle_radians)

    # Point-slope form of the line equation: y - y1 = m * (x - x1)
    # where (x1, y1) is the starting point of the vector
    line_equation = lambda x_val: slope * (x_val - x) + y
    line_equation_y = lambda y_val: ((y_val - y) / slope) + x

    # Find the next vertical asymptote to reach at x = targetX
    targetX = next((x_val for x_val in np.arange(0, width + 1) if x_val > x), None)

    # Find the first intersection point with horizontal grid lines at y = targetY
    if(angle_degrees < 0) :
        targetY = next((y_val for y_val in np.arange(0, height + 1) if y_val >= y and y_val <= height), None)    
        targetY -= 1
    else:
        targetY = next((y_val for y_val in np.arange(0, height + 1) if y_val > y and y_val <= height), None)        

    # Calculate the coordinates of the intersection points
    first_intersection_point = (targetX, line_equation(targetX)) if targetX is not None else None
    second_intersection_point = (line_equation_y(targetY), targetY) if targetY is not None else None

    #return the closer intersection point
    if(euclidean_distance((x, y), (first_intersection_point)) < euclidean_distance((x, y), (second_intersection_point))) :
        return first_intersection_point
    else:
        return second_intersection_point

def hash_two_points(point1, point2):
    """
    Hash function for two sets of two-dimensional points.

    Args:
    - point1 (tuple): A tuple representing the first point (x1, y1).
    - point2 (tuple): A tuple representing the second point (x2, y2).

    Returns:
    - int: Hash code for the two points.
    """
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must be tuples with two coordinates (x, y)")

    # Choose a scaling factor (adjust as needed based on your specific use case)
    scaling_factor = 1000

    # Convert floating-point values to integers
    x1_int = int(round(point1[0], 12) * scaling_factor)
    y1_int = int(round(point1[1], 12) * scaling_factor)
    x2_int = int(round(point2[0], 12) * scaling_factor)
    y2_int = int(round(point2[1], 12) * scaling_factor)

    # Combine the hash codes of x and y for both points using bitwise XOR
    hash_code = hash(x1_int) ^ hash(y1_int) ^ hash(x2_int) ^ hash(y2_int) + ((x2_int*8) + x1_int**3 + y2_int * y1_int)

    #see if this individual vector has already been added to the graph
    global VECTOR_HASH
    mapping = VECTOR_HASH.get(hash_code)
    if mapping is not None :
        return False
    else :
        VECTOR_HASH[hash_code] = True
        return True

def createArray(ax, startX, startY, theta1, theta2, thetaOne, width, height) :
    """
    Recursively create and draw a series of vectors on a Matplotlib axis.

    Parameters:
    - ax (matplotlib.axes._axes.Axes): The Matplotlib axis on which the vectors will be drawn.
    - startX (float): The x-coordinate of the starting point of the initial vector.
    - startY (float): The y-coordinate of the starting point of the initial vector.
    - theta1 (float): The angle of the first vector in degrees (measured counterclockwise from the positive x-axis).
    - theta2 (float): The angle of the second vector in degrees (measured counterclockwise from the positive x-axis).
    - thetaOne (bool): A boolean indicating whether to use theta1 or theta2 for the initial vector.
    - width  (int)  : Defines the width of the graph
    - height (int)  : Defines the height of the graph

    Returns:
    - None
    """
    
    #decipher you're theta based thetaOne boolean
    if(thetaOne) :
        theta = theta1
        otheta = theta2
    else:
        theta = theta2
        otheta = theta1
    #find next intersection point and distance to that point
    interX, interY = find_first_intersection_point(startX, startY, theta, width, height)
    vectorLength = euclidean_distance((startX, startY), (interX, interY))

    #check to make sure this exact vector hasn't been added to the graph before
    newVector = hash_two_points((startX, startY), (interX, interY))
    if newVector is False:
        return

    #draw the given vector if in graph
    if(startX >= 0 and startY >= 0 and startX <= width and startY <= height and interX >= 0 and interY >= 0 and interX <= width and interY <= height and vectorLength > 1e-10) :
        add_vector_to_graph(ax, startX, startY, theta, vectorLength)

        global VECTOR_COUNT
        VECTOR_COUNT += 1
        #can add to the vector count after we make sure this isn't a duplicate vector and is in range of graph

    #draw the next vector if it is still in the graph
    if( interX < width and interY < height and interY >= 0 ) :
        createArray(ax, interX, interY, theta1, theta2, not thetaOne, width, height)
        createArray(ax, interX, interY, -theta1, -theta2, not thetaOne, width, height)

    #edge case check to reflect vectors at the top of the grid back down
    if( interX < width and interY == height and otheta > 0 ) :
        createArray(ax, interX, interY, -theta1, -theta2, not thetaOne, width, height )


def main():

    def on_button_click(event):
        """
        Updates the GUI when 'Calculate' button is clicked
        """
        update(45)
    
    # Create a graph with a checkerboard pattern
    fig, ax = plt.subplots()
    ax = draw_checkerboard_just_ax(5, 5, 1, ax)
    plt.subplots_adjust(bottom=0.35)

    # Input boxes for theta1 and theta2
    theta1_input = TextBox(plt.axes([0.25, 0.1, 0.65, 0.03]), 'Theta1 (degrees):', initial='0')
    theta2_input = TextBox(plt.axes([0.25, 0.05, 0.65, 0.03]), 'Theta2 (degrees):', initial='45')
    width_input = TextBox(plt.axes([0.25, 0.15, 0.23, 0.03]), 'Width (Boxes):', initial='5')
    height_input = TextBox(plt.axes([0.66, 0.15, 0.24, 0.03]), 'Height (Boxes):', initial='5')
    startPoint_input = TextBox(plt.axes([0.25, 0.2, 0.65, 0.03]), 'Start Point:', initial='1.5')
    button_ax = plt.axes([0.8, 0.25, 0.15, 0.035])  # [left, bottom, width, height]

    #read in the current geometry
    read_in_geometry("traingle_pattern.txt")

    #Calculate button
    button = Button(button_ax, 'Calculate') 
    button.on_clicked(on_button_click)

    #Vector Count Display
    vc = get_vector_count()
    vectorBoxString = "Unique Vector Count: "+ str(vc)
    text_box = plt.text(-1 , 20, vectorBoxString, bbox=dict(facecolor='white', edgecolor='black'))



    # Function to update the plot when input values change
    def update(val):
        """
        Function to update the plot when calculate button is pressed
        """

        try:
            global VECTOR_HASH
            set_vector_count(0)
            VECTOR_HASH.clear()

            ax.clear()
            startPoint = float(startPoint_input.text)
            width = int(width_input.text)
            height = int(height_input.text)

            #draw checkerboard with dimensions (4, 6)

            draw_checkerboard_just_ax(height, width, 1, ax)
            theta1 = float(theta1_input.text)
            theta2 = float(theta2_input.text)
            
            startX = 0
            startY = startPoint

            #createArray(ax, startX, startY, theta1, theta2, True, width, height)
            #createArray(ax, startX, startY, -theta1, -theta2, True, width, height)

            #reset the boundary conditions
            clear_bmxb()
            add_boundary(width, height)

            #draw the geometry
            draw_geometry(ax)

            #shoot the starting vector
            shoot_vector(ax, (startX, startY), theta1)

            text_box.set_text("Unique Vector Count :" + str(get_vector_count())) #str(VECTOR_COUNT))
            plt.grid()
            plt.show()

            # Update your existing plot with the new theta1 and theta2 values
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")


    update(45)


if __name__ == "__main__":
    main()
