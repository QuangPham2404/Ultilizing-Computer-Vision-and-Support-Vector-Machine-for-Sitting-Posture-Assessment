import cv2 as cv
import mediapipe as mp
import numpy as np
import os

# Load the tools
mp_pose = mp.solutions.pose

# Landmark indices for nose, shoulders, and elbows
LANDMARK_INDEX = [0, 11, 12, 13, 14]

# Create display window
win_name = "display"
cv.namedWindow(win_name, cv.WINDOW_NORMAL)

# Get video stream from webcam
video_stream = cv.VideoCapture(0)

#constant
calibration_in_process = True

y_nose_shoulders_calibrated = 0
y_nose_elbows_calibrated = 0
y_shoulders_elbows_calibrated = 0
x_nose_shoulders_left_calibrated = 0
x_nose_shoulders_right_calibrated = 0
x_nose_shoulders_elbows_left_calibrated = 0
x_nose_shoulders_elbows_right_calibrated = 0
calibrated_values = []

correct_posture_data = []
incorrect_posture_data = []

#functions to calculate values for posture classification
# Function to calculate the average y distance of the nose and shoulders
def get_y_nose_shoulders(landmarks):
    nose_y = landmarks[0][1]
    shoulder1_y = landmarks[1][1]
    shoulder2_y = landmarks[2][1]
    distance_y_nose_shoulder1 = abs(nose_y - shoulder1_y)
    distance_y_nose_shoulder2 = abs(nose_y - shoulder2_y)
    avg_distance_y_nose_shoulders = round((distance_y_nose_shoulder1 + distance_y_nose_shoulder2)/2, 8)
    return avg_distance_y_nose_shoulders

# Function to calculate the average y distance of the nose and elbows
def get_y_nose_elbows(landmarks):
    nose_y = landmarks[0][1]
    elbow1_y = landmarks[3][1]
    elbow2_y = landmarks[4][1]
    distance_y_nose_elbow1 = abs(nose_y - elbow1_y)
    distance_y_nose_elbow2 = abs(nose_y - elbow2_y)
    avg_distance_y_nose_elbows = round((distance_y_nose_elbow1 + distance_y_nose_elbow2)/2, 8)
    return avg_distance_y_nose_elbows

# Function to calculate the average y distance of the shoulders and elbows
def get_y_shoulders_elbows(landmarks):
    shoulder1_y = landmarks[1][1]
    shoulder2_y = landmarks[2][1]
    elbow1_y = landmarks[3][1]
    elbow2_y = landmarks[4][1]
    distance_y_shoulder1_elbow1 = abs(elbow1_y - shoulder1_y)
    distance_y_shoulder2_elbow2 = abs(elbow2_y - shoulder2_y)
    avg_distance_y_shoulders_elbows = round((distance_y_shoulder1_elbow1 + distance_y_shoulder2_elbow2)/2, 8)
    return avg_distance_y_shoulders_elbows

# Function to calculate the average x distance of the nose and shoulders on the left side
def get_x_nose_shoulders_left(landmarks):
    nose_x = landmarks[0][0]
    shoulder1_x = landmarks[1][0]
    distance_x_nose_shoulder1 = abs(nose_x - shoulder1_x)
    return round(distance_x_nose_shoulder1, 8)

# Function to calculate the average x distance of the nose and shoulders on the right side
def get_x_nose_shoulders_right(landmarks):
    nose_x = landmarks[0][0]
    shoulder2_x = landmarks[2][0]
    distance_x_nose_shoulder2 = abs(nose_x - shoulder2_x)
    return round(distance_x_nose_shoulder2, 8)

# Function to calculate the average x distance of the nose and shoulders on the left side
def get_x_nose_elbows_left(landmarks):
    nose_x = landmarks[0][0]
    elbow1_x = landmarks[3][0]
    distance_x_nose_elbow1 = abs(nose_x - elbow1_x)
    return round(distance_x_nose_elbow1, 8)

# Function to calculate the average x distance of the nose and shoulders on the right side
def get_x_nose_elbows_right(landmarks):
    nose_x = landmarks[0][0]
    elbow2_x = landmarks[4][0]
    distance_x_nose_elbow2 = abs(nose_x - elbow2_x)
    return round(distance_x_nose_elbow2, 8)


def write_list_to_file(input_list, file_path):
    """
    Writes each sublist of a list to a .txt file, each sublist on a new line.

    Parameters:
    input_list (list of lists): The list containing sublists to write to the file.
    file_path (str): The path to the .txt file where the sublists will be written.

    Returns:
    None
    """
    try:
        with open(file_path, 'w') as file:
            for sublist in input_list:
                file.write(f"{', '.join(map(str, sublist))}\n")
        print(f"List successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def combine_files(input_dir, output_data_file, output_tag_file):
    """
    Combines all files ending with '_data.txt' into a single file and all files 
    ending with '_tag.txt' into another single file.

    Parameters:
    - input_dir (str): Directory containing the input files.
    - output_data_file (str): Path for the combined data file.
    - output_tag_file (str): Path for the combined tag file.

    Returns:
    None
    """
    data_lines = []
    tag_lines = []

    # Iterate through files in the directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if filename.endswith("_data.txt"):
            with open(file_path, 'r') as f:
                data_lines.extend(f.readlines())
        elif filename.endswith("_tag.txt"):
            with open(file_path, 'r') as f:
                tag_lines.extend(f.readlines())

    # Write combined data lines to the output data file
    with open(output_data_file, 'w') as f:
        f.writelines(data_lines)

    # Write combined tag lines to the output tag file
    with open(output_tag_file, 'w') as f:
        f.writelines(tag_lines)

    print(f"Combined data written to {output_data_file}")
    print(f"Combined tags written to {output_tag_file}")


# Create the Mediapipe Pose tool
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    
    while video_stream.isOpened():
        success, frame = video_stream.read()
        if not success:
            print("Video stream interrupted")
            break

        #detect key pressed
        key = cv.waitKey(1) & 0xFF  # Capture the key pressed (if any)

        # To improve the performance of the detector, set the writable flag of the frame to False
        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        #frame = cv.flip(frame, 1)

        # Get results, convert coords to pixel coords
        result = pose.process(frame)

        # Convert the writable flag back to True for annotation
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        
        # Check if landmarks are detected
        if result.pose_landmarks:
            frame_h, frame_w = frame.shape[:2]
            # Initialize a NumPy array for the landmarks
            landmarks = np.zeros((len(LANDMARK_INDEX), 2), dtype=np.int32)
            
            for i, index in enumerate(LANDMARK_INDEX):
                landmark = result.pose_landmarks.landmark[index]
                landmarks[i] = [int(landmark.x * frame_w), int(landmark.y * frame_h)]
            
            #print("Landmark Coordinates:", landmarks)

            # Draw circles on the landmarks
            for coords in landmarks:
                cv.circle(frame, tuple(coords), 4, (250, 100, 100), -1)

            '''# Optionally, draw lines connecting specific landmarks
            cv.line(frame, tuple(landmarks[0]), tuple(landmarks[1]), (225, 0, 0), 2)
            cv.line(frame, tuple(landmarks[0]), tuple(landmarks[2]), (225, 0, 0), 2)'''

            if calibration_in_process:
                text = "Calibration in progress"
                cv.putText(frame, text, (50, 100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)

                # get calibrated values
                y_nose_shoulders_calibrated = get_y_nose_shoulders(landmarks)
                y_nose_elbows_calibrated = get_y_nose_elbows(landmarks)
                y_shoulders_elbows_calibrated = get_y_shoulders_elbows(landmarks)
                x_nose_shoulders_left_calibrated = get_x_nose_shoulders_left(landmarks)
                x_nose_shoulders_right_calibrated = get_x_nose_shoulders_right(landmarks)
                x_nose_elbows_left_calibrated = get_x_nose_elbows_left(landmarks)
                x_nose_elbows_right_calibrated = get_x_nose_elbows_right(landmarks)

                if key == ord("2"):
                    calibrated_values.append(y_nose_shoulders_calibrated)
                    calibrated_values.append(y_nose_elbows_calibrated)
                    calibrated_values.append(y_shoulders_elbows_calibrated)
                    calibrated_values.append(x_nose_shoulders_left_calibrated)
                    calibrated_values.append(x_nose_shoulders_right_calibrated)
                    calibrated_values.append(x_nose_elbows_left_calibrated)
                    calibrated_values.append(x_nose_elbows_right_calibrated)
                    calibration_in_process = False
                    print(calibrated_values)

            else:
                ratio_y_nose_shoulders = round(get_y_nose_shoulders(landmarks)/calibrated_values[0], 4)
                ratio_y_nose_elbows = round(get_y_nose_elbows(landmarks)/calibrated_values[1], 4)
                #ratio_y_shoulders_elbows = round(get_y_shoulders_elbows(landmarks)/calibrated_values[2], 4)
                ratio_x_nose_shoulders_left = round(get_x_nose_shoulders_left(landmarks)/calibrated_values[3], 4)
                ratio_x_nose_shoulders_right = round(get_x_nose_shoulders_right(landmarks)/calibrated_values[4], 4)
                #ratio_x_nose_elbows_left = round(get_x_nose_elbows_left(landmarks)/calibrated_values[5], 4)
                #ratio_x_nose_elbows_right = round(get_x_nose_elbows_right(landmarks)/calibrated_values[6], 4)

                #capturing data for normal postures
                if key == ord("0"): 
                    correct_posture_data.append([ratio_y_nose_shoulders, ratio_y_nose_elbows, ratio_x_nose_shoulders_left, ratio_x_nose_shoulders_right])

                #capturing data for abnormal postures
                elif key == ord("1"): 
                    incorrect_posture_data.append([ratio_y_nose_shoulders, ratio_y_nose_elbows, ratio_x_nose_shoulders_left, ratio_x_nose_shoulders_right])

                else:
                    pass


        # Show the annotated frame
        cv.imshow(win_name, frame)

        # Break loop on 'Esc' key
        if key == ord("q"):
            break


video_stream.release()
cv.destroyAllWindows()

# write the data to files
name = input("Enter the name of the participant: ")
write_list_to_file(correct_posture_data + incorrect_posture_data, f"{name}_data.txt")

correct_posture_tag_list = [0] * len(correct_posture_data)
incorrect_posture_tag_list = [1] * len(incorrect_posture_data)
with open(f"{name}_tag.txt", 'w') as file:
    for element in correct_posture_tag_list + incorrect_posture_tag_list:
        file.write(str(element) + '\n')

combine_files(
    input_dir="./input_files",
    output_data_file="combined_data.txt",
    output_tag_file="combined_tags.txt"
)
