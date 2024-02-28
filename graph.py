import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np
import sys
import math

def add_vector_to_graph(ax, x, y, angle_degrees, length, color='red'):
    angle_radians = np.radians(angle_degrees)
    x_component = length * np.cos(angle_radians)
    y_component = length * np.sin(angle_radians)

    # Plot the vector using quiver on the existing axis (ax)
    ax.quiver(x, y, x_component, y_component, angles='xy', scale_units='xy', scale=1, color=color, headaxislength=0, headlength=0)

# Example: Create a graph with a checkerboard pattern
def draw_checkerboard(rows, cols, square_size):
    fig, ax = plt.subplots()

    for row in range(rows):
        for col in range(cols):
            # Set all squares to white
            # color = 'white'
            color = 'black'

            ax.add_patch(plt.Rectangle((col * square_size, row * square_size), square_size, square_size,
                                       edgecolor='black', facecolor=color, color='#0099FF'))

    ax.set_xlim(0, cols * square_size)
    ax.set_ylim(0, rows * square_size)
    ax.set_aspect('equal', adjustable='box')

    # Show x and y axes
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Add labels to x and y axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Space')

    return fig, ax

def draw_checkerboard_just_ax(rows, cols, square_size, ax):

    for row in range(rows):
        for col in range(cols):
            # Set all squares to white
            color = 'white'

            ax.add_patch(plt.Rectangle((col * square_size, row * square_size), square_size, square_size,
                                       edgecolor='black', facecolor=color,color='#0099FF'))

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

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def find_first_intersection_point(x, y, angle_degrees, vector_length, grid_size):
    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate slope of the vector
    slope = np.tan(angle_radians)
    # print("CurrentX: ", x)
    # print("CurrentY: ", y)
    # print("angle_degrees", angle_degrees)
    # print("slope: ", slope)


    # Point-slope form of the line equation: y - y1 = m * (x - x1)
    # where (x1, y1) is the starting point of the vector
    line_equation = lambda x_val: slope * (x_val - x) + y
    line_equation_y = lambda y_val: ((y_val - y) / slope) + x

    # Find intersection points with vertical and horizontal grid lines
    x_intercept = np.arange(0, grid_size + 1)
    y_intercept = line_equation(x_intercept)

    # Find the smallest positive intersection points along the x-axis and y-axis
    first_x_intersection = next((x_val for x_val in x_intercept if x_val > x), None)
    # print("TargetX", first_x_intersection)
    first_y_intersection = next((y_val for y_val in y_intercept if y_val > y and y_val <= grid_size), None)

    # Find the first intersection point with horizontal grid lines
    
    if(angle_degrees < 0) :
        y_intercept_horizontal = next((y_val for y_val in np.arange(0, grid_size + 1) if y_val >= y and y_val <= grid_size), None)    
        y_intercept_horizontal -= 1
    else:
        y_intercept_horizontal = next((y_val for y_val in np.arange(0, grid_size + 1) if y_val > y and y_val <= grid_size), None)    

    
    # print("TargetY: ", y_intercept_horizontal)

    # Calculate the coordinates of the first intersection point
    first_y_intersection = (line_equation_y(y_intercept_horizontal), y_intercept_horizontal) if y_intercept_horizontal is not None else None


    # Calculate the coordinates of the first intersection point
    first_intersection_point = (first_x_intersection, line_equation(first_x_intersection))
    second_intersection_point = first_y_intersection

    if(euclidean_distance((x, y), (first_intersection_point)) < euclidean_distance((x, y), (second_intersection_point))) :
        # print("point found: ", first_intersection_point)
        return first_intersection_point
    else:
        # print("point found: ", second_intersection_point)
        return second_intersection_point



def createArray(ax, startX, startY, theta1, theta2, checkSize, thetaOne, grid_size) :

    if(thetaOne) :
        theta = theta1
    else:
        theta = theta2


    #find next intersection point and distance to that point
    interX, interY = find_first_intersection_point(startX, startY, theta, 2, grid_size)
    vectorLength = euclidean_distance((startX, startY), (interX, interY))

    #draw the given vector
    add_vector_to_graph(ax, startX, startY, theta, vectorLength)

    #draw the next vector if it is still in the graph
    if(interX < checkSize and interY < checkSize and interY >= 0 ) :
        
        createArray(ax, interX, interY, theta1, theta2, checkSize, not thetaOne, grid_size)
        createArray(ax, interX, interY, -theta1, -theta2, checkSize, not thetaOne, grid_size)

def main():
    # Create a graph with a checkerboard pattern
    fig, ax = draw_checkerboard(5, 5, 1)
    plt.subplots_adjust(bottom=0.35)

    # Input boxes for theta1 and theta2
    theta1_input = TextBox(plt.axes([0.25, 0.1, 0.65, 0.03]), 'Theta1 (degrees):', initial='45')
    theta2_input = TextBox(plt.axes([0.25, 0.05, 0.65, 0.03]), 'Theta2 (degrees):', initial='45')
    gridSize_input = TextBox(plt.axes([0.25, 0.15, 0.65, 0.03]), 'Width (Boxes):', initial='5')
    startPoint_input = TextBox(plt.axes([0.25, 0.2, 0.65, 0.03]), 'Start Point:', initial='2.5')


    # Function to update the plot when input values change
    def update(val):
        try:
            ax.clear()
            gridSize = int(gridSize_input.text)
            startPoint = float(startPoint_input.text)

            draw_checkerboard_just_ax(gridSize, gridSize, 1, ax)
            theta1 = float(theta1_input.text)
            theta2 = float(theta2_input.text)
            
            startX = 0
            startY = startPoint

            createArray(ax, startX, startY, theta1, theta2, gridSize, True, gridSize)
            createArray(ax, startX, startY, -theta1, -theta2, gridSize, True, gridSize)
            x_grid_lines, y_grid_lines = find_first_intersection_point(0, 2.5, theta1, 2, gridSize)
            
            # print("Intersection points with vertical grid lines:", x_grid_lines)
            # print("Intersection points with horizontal grid lines:", y_grid_lines)
            
            plt.grid()
            # plt.show()
            print("done updating")
            # Update your existing plot with the new theta1 and theta2 values
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    # Register the update function with each input box
    theta1_input.on_submit(update)
    theta2_input.on_submit(update)
    gridSize_input.on_submit(update)
    startPoint_input.on_submit(update)

    update(45)
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
