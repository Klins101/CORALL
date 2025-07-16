import numpy as np

def nautical_to_meters(nm_value):
    return nm_value * 1852

obstacle_cases = {
    "Case 1": [[[nautical_to_meters(6), nautical_to_meters(0)], 180]],
    "Case 2": [[[nautical_to_meters(5), nautical_to_meters(-2.14)], 90]],
    "Case 3": [[[nautical_to_meters(3), nautical_to_meters(0)], 0]],
    "Case 4": [[[nautical_to_meters(3.44), nautical_to_meters(1.55 + 0.08 )], 295]],
    "Case 5": [[[nautical_to_meters(5), nautical_to_meters(-2.0-0.14)], 90], [[nautical_to_meters(7-0.05), nautical_to_meters(0)], 180]],
    "Case 6": [[[nautical_to_meters(3.4), nautical_to_meters(-1.5 + 0.03)], 45], [[nautical_to_meters(3), nautical_to_meters(-0.35-0.04)], 10]],
    "Case 7": [[[nautical_to_meters(3), nautical_to_meters(0)], 0], [[nautical_to_meters(3.4), nautical_to_meters(-1.5+0.01)], 45]],
    "Case 8": [[[nautical_to_meters(5), nautical_to_meters(-2.13)], 90], [[nautical_to_meters(7), nautical_to_meters(0)], 180]],
    "Case 9": [[[nautical_to_meters(3.4), nautical_to_meters(-1.5 + 0.03)], 45], [[nautical_to_meters(5), nautical_to_meters(-2.1 - 0.05)], 90]],
    "Case 10": [[[nautical_to_meters(3), nautical_to_meters(0.35)], 350], [[nautical_to_meters(4.4), nautical_to_meters(-2.1 + 0.20)], 90]],
    "Case 11": [[[nautical_to_meters(5), nautical_to_meters(2.1)], -90], [[nautical_to_meters(3.4), nautical_to_meters(-1.5)], 45]],
    "Case 12": [[[nautical_to_meters(7), nautical_to_meters(0)], 180], [[nautical_to_meters(3), nautical_to_meters(0.3+0.05)], -10], [[nautical_to_meters(3.44), nautical_to_meters(-1.55+0.05)], 45]],
    "Case 13": [[[nautical_to_meters(6), nautical_to_meters(0)], 180], [[nautical_to_meters(3), nautical_to_meters(0.3+0.05)], 350], [[nautical_to_meters(3.4), nautical_to_meters(1.5+0.05)], 295]],
    "Case 14": [[[nautical_to_meters(3.4), nautical_to_meters(-1.5)], 45], [[nautical_to_meters(3), nautical_to_meters(-0.4)], 10], [[nautical_to_meters(5), nautical_to_meters(-2.1-0.05)], 90]],
    "Case 15": [[[nautical_to_meters(3), nautical_to_meters(0)], 0], [[nautical_to_meters(3.4), nautical_to_meters(-1.5)], 45], [[nautical_to_meters(5), nautical_to_meters(-2.1-0.05)], 90]],
    "Case 16": [[[nautical_to_meters(3.4), nautical_to_meters(1.5-0.03)], -45], [[nautical_to_meters(5), nautical_to_meters(2.1 + 0.04)], -90], [[nautical_to_meters(5), nautical_to_meters(-2.1 + -0.05)], 90]],
    "Case 17": [[[nautical_to_meters(3), nautical_to_meters(0)], 0], [[nautical_to_meters(3), nautical_to_meters(0.3+0.05)], -10], [[nautical_to_meters(3.4), nautical_to_meters(-1.5)], 45]],
    "Case 18": [[[nautical_to_meters(3.3), nautical_to_meters(-0.3 - 0.1)], 10], [[nautical_to_meters(3.4), nautical_to_meters(-1.5+0.05)], 45], [[nautical_to_meters(6.5), nautical_to_meters(-1.5)], 135]],
    "Case 19": [[[nautical_to_meters(3), nautical_to_meters(-0.3 - 0.07)], 10], [[nautical_to_meters(3), nautical_to_meters(0.3+0.05)], -10], [[nautical_to_meters(6.5), nautical_to_meters(-1.5-0.03)], 135]],
    "Case 20": [[[nautical_to_meters(3), nautical_to_meters(0)], 0], [[nautical_to_meters(3), nautical_to_meters(-0.3-0.05)], 10], [[nautical_to_meters(4.4), nautical_to_meters(-2.1 + 0.25)], 90]],
    "Case 21": [[[nautical_to_meters(3-0.3), nautical_to_meters(-0.3-0.05)], 10], [[nautical_to_meters(3-0.3), nautical_to_meters(0.3+0.02)], -10], [[nautical_to_meters(4.4), nautical_to_meters(-1.9)], 90]],
    "Case 22": [[[nautical_to_meters(3), nautical_to_meters(0)], 0], [[nautical_to_meters(3.94), nautical_to_meters(-1.6-0.13)], 45], [[nautical_to_meters(5), nautical_to_meters(-2.01-0.15)], 90]],
    "Case 23": [[[nautical_to_meters(4.243), nautical_to_meters(2.243)], -75]],
    
}

# Function to get obstacles for a specific case
def get_obstacles(case_number):
    case_key = f"Case {case_number}"
    return obstacle_cases.get(case_key, [])


def get_obstacle_data(case_number):
    """
    Convert obstacle case data to simulation format
    Args:
        case_number (int): The case number to use (1-22)
    Returns:
        Xob, Yob (lists): X and Y positions in meters
        Vob (list): Velocities in m/s 
        psiob (numpy array): Angles in radians
    """
    # Get obstacle data for the case
    obstacles = get_obstacles(case_number)
    
    # Initialize empty lists
    Xob = []
    Yob = []
    psiob = []
    
    # Default velocity (you may want to adjust this)
    Vob = [18.52] * len(obstacles)  # Assuming 9.5 m/s for all obstacles
    
    # Extract positions and angles from obstacles
    for obstacle in obstacles:
        position = obstacle[0]  # Get [x,y] position
        angle = obstacle[1]    # Get angle in degrees
        
        Xob.append(position[0])  # X position in meters
        Yob.append(position[1])  # Y position in meters
        psiob.append(np.radians(angle))  # Convert angle to radians
    
    return Xob, Yob, Vob, np.array(psiob)

