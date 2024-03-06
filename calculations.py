import math

VECTOR_COUNT = 0
LINES = []
MXBLINES = []
BOUNDARY_MXBLINES = []


def clear_bmxb() :
    BOUNDARY_MXBLINES.clear()

def set_vector_count(value) :
    global VECTOR_COUNT
    VECTOR_COUNT = value

def get_vector_count() :
    return VECTOR_COUNT

def get_lines() :
    return LINES

def is_within_error(actual_value, expected_value, error_margin):
    """
    Check if the actual value is within the specified error margin of the expected value.

    Parameters:
    - actual_value (float): The actual value to check.
    - expected_value (float): The expected (target) value.
    - error_margin (float): The acceptable error margin.

    Returns:
    - bool: True if within error margin, False otherwise.
    """
    return abs(actual_value - expected_value) <= error_margin

def add_boundary(width, height):

    #MXBLINES.append((m, b, y1, y2, x1, x2))  
    BOUNDARY_MXBLINES.append((0, 0, 0, 0, 0, width, False)) 
    BOUNDARY_MXBLINES.append((float('inf'), 0, 0, height, 0, 0, False ))
    BOUNDARY_MXBLINES.append((0, height, height, height, 0, width, False))
    BOUNDARY_MXBLINES.append((float('inf'), width, 0, height, width, width, False))

def read_in_geometry(filename) :

    filename = "geometries/" + filename

    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read each line from the file
            lines = file.readlines()

        # Process each line and extract x, y coordinates
        for line_number, line in enumerate(lines, start=1):
            try:
                # Split the line into two pairs of x and y coordinates
                x1, y1, x2, y2 = map(float, line.strip().split())
                print(x1, y1, x2, y2)

                # Now you can use x1, y1, x2, y2 in your code as needed
                #print(f"Line {line_number}: Point 1 ({x1}, {y1}), Point 2 ({x2}, {y2})")
                
                #add the lines to the global list of all lines
                global LINES, MXBLINES
                LINES.append(((x1, y1), (x2, y2)))

                # Calculate the slope (m)
                if x2 - x1 != 0:
                    m = (y2 - y1) / (x2 - x1)
                    # Calculate the y-intercept (b)
                    b = y1 - m * x1
                else:
                    # Handle the case of a vertical line (undefined slope)
                    m = float('inf')
                    b = x2
                
                #add each line to the list in slope intercept
                MXBLINES.append((m, b, y1, y2, x1, x2, True))            

            except ValueError:
                # Handle errors related to parsing the lines
                print(f"Error in line {line_number}: Invalid format. Each line must contain four values.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def detect_nearest_collision(start_point, theta):

    #get the x and y starting points
    startX = start_point[0]
    startY = start_point[1]

    #check if theta is a vertical line with infinite slope
    if(is_within_error(theta, 90, 1e-10)) :
        m1 = float('inf')
        b1 = startX
    elif(is_within_error(theta, -90, 1e-10)) :
        m1 = float('-inf')
        b1 = startX
    else :
        # get the radians and respective slope from the starting point
        radians = math.radians(theta)
        m1 = math.tan(radians)
        #print("Radioans", radians, "theta", theta, "m1", m1)
        b1 = startY - m1 * startX

    #print("Theta", theta, m1 ,", m1,",b1, ", b1")

    #set starting values for the loop
    closestCollisionDistance = 1e10
    xCollision = None
    yCollision = None
    mCollision = None
    recurse = False

    #print(MXBLINES)
    allLines = MXBLINES + BOUNDARY_MXBLINES
    for line in allLines: 
        
        #line takes the format (slope, y-intercept, y1, y2, x1, x2) - non vertical lines
        #                      (slope(inf), x-intercept, y1, y2, x1, x2) - vertical lines

        m2 = line[0]
        b2 = line[1]

        #print("checking line with slope: ", m2, "and y intercept: ", b2)
        # Check if the lines are parallel
        if m1 == m2 or (m1 == float('inf') and m2 == float('-inf')):
            continue

        # Calculate the intersection point given both lines are not vertical
        if(m2 != float('inf') and m1 != float('inf') and m1 != float('-inf')) :
            x = (b2 - b1) / (m1 - m2)
            y = (m1 * x) + b1
        # Calculate the intersection given that m1 is vertical --b1 = x intersection
        elif(m2 != float('inf')) :
            x = b1
            y = (m2 * x) + b2
        # Calculate the intersection given that m2 is vertical -- b2 = x-intersection
        else :
            x = b2
            y = (m1 * x) + b1
            
        #get the range the line is operating within
        upperY = max(line[2], line[3])
        lowerY = min(line[2], line[3])
        upperX = max(line[4], line[5])
        lowerX = min(line[4], line[5])

        #only want to register collisions within the appropriate range of the function
        if((y >= upperY + 1e-12) or (y <= lowerY -  1e-12) or (x >= upperX + 1e-12) or (x <= lowerX - 1e-12)) :
            continue

        #only want to register collisions within the direction of the slope
        if (theta > 0) :
            if(startY > y ):
                continue
        else :
            if(startY < y) :
                continue
        
        if(x < startX) :
            continue

        distance = euclidean_distance(start_point, (x, y))
        #print("Collision :", x, y, "Distance: ", distance)

        #only collide if it's a certain distance away
        if distance > 1e-10 and distance < closestCollisionDistance :
            closestCollisionDistance = distance
            xCollision = x
            yCollision = y
            mCollision = m2
            recurse = line[6]


    theta_reflection = reflection_line(slope_to_degrees(m1), slope_to_degrees(mCollision))

    return (xCollision, yCollision), theta_reflection, recurse

def slope_to_degrees(slope):
    if(slope == float('inf')):
        return 90
    
    return math.degrees(math.atan(slope))

def reflection_line(incoming_angle_degrees, reflector_angle_degrees):
    """
    Calculate the angle of reflection based on the law of reflection.

    Parameters:
    - incoming_angle_degrees (float): Angle of incidence in degrees.
    - reflector_angle_degrees (float): Angle of the reflector in degrees.

    Returns:
    - float: Angle of reflection in degrees.
    """
    # Calculate the angle of incidence
    angle_of_incidence = (incoming_angle_degrees - reflector_angle_degrees)

    answer = (angle_of_incidence * - 1) + reflector_angle_degrees
    #print("Refelction Theta: ", answer, "incoming: ", incoming_angle_degrees, "reflective angle: ", reflector_angle_degrees)
    return (angle_of_incidence * - 1) + reflector_angle_degrees

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points in a two-dimensional space.

    Parameters:
    - point1 (tuple): A tuple representing the coordinates (x1, y1) of the first point.
    - point2 (tuple): A tuple representing the coordinates (x2, y2) of the second point.

    Returns:
    - float: The Euclidean distance between the two points.
    """

    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance