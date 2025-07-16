import cv2
import numpy as np


def create_video(frames, output_filename='Artemis.avi', fps=2, quality=95):
    """
    Create a video from a list of frames.

    Parameters:
    frames (list): List of frames (numpy arrays)
    output_filename (str): Name of the output video file
    fps (int): Frames per second
    quality (int): Video quality (0-100)

    Returns:
    None
    """
    if not frames:
        print("No frames to process.")
        return

    # Get the dimensions of the first frame
    height, width = frames[0].shape[:2]

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    for frame in frames:
        # Ensure the frame is in the correct format (BGR)
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Write the frame
        out.write(frame)

    # Release the VideoWriter
    out.release()

    print(f"Video saved as {output_filename}")

# Example usage:
# Assuming F is your list of frames (numpy arrays)
# create_video(F, 'Artemis.avi', fps=2)
