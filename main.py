import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision

from src.config import get_config
from src.lights import LightsManager

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = vision.GestureRecognizer
GestureRecognizerOptions = vision.GestureRecognizerOptions
VisionRunningMode = vision.RunningMode
GestureRecognizerResult = vision.GestureRecognizerResult


def draw_landmarks_on_image(rgb_image, detection_result, margin=10, font_size=1, font_thickness=1, handedness_text_color=(88, 205, 54)):
    """_summary_
    Code from:
    https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb
    """
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - margin

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    font_size, handedness_text_color, font_thickness, cv2.LINE_AA)

    return annotated_image


def list_webcam_ports(max_index=10):
    index = 0
    arr = []
    for _ in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
    return arr


def act(result: GestureRecognizerResult, lights: LightsManager, light: int):
    if len(result.gestures) > 0:
        category_name = result.gestures[0][0].category_name
        match category_name:
            case "Thumb_Up":
                print("Increase intensity")
                lights.change_brightness(light, 254)
            case "Thumb_Down":
                print("Decrease intensity")
                lights.change_brightness(light, 50)
            case "Open_Palm":
                print("Turn off")
                lights.turn_off(light)
            case "Closed_Fist":
                print("Turn on")
                lights.turn_on(light)


def main():
    config = get_config()
    lights = LightsManager(
        bridge=config['lights']['bridge'], username=config['lights']['username'])
    light = config['lights']['light']

    model = 'models/gesture_recognizer.task'
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1,
    )

    with GestureRecognizer.create_from_options(options) as recognizer:
        process_this_frame = True
        gesture_recognition_result = None

        available_webcam_indexes = list_webcam_ports()
        if len(available_webcam_indexes) == 0:
            raise Exception("No webcam found")

        webcam_index = available_webcam_indexes[0]
        video_capture = cv2.VideoCapture(webcam_index)

        while True:
            # Read the frame
            ret, frame = video_capture.read()

            # Process every other frame
            if process_this_frame:
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB, data=frame)
                frame_timestamp_ms = int(
                    video_capture.get(cv2.CAP_PROP_POS_MSEC))
                gesture_recognition_result = recognizer.recognize_for_video(
                    mp_image, frame_timestamp_ms)

                act(gesture_recognition_result, lights, light)

            process_this_frame = not process_this_frame

            # Display the results
            annotated_image = draw_landmarks_on_image(
                frame, gesture_recognition_result)

            # Display the resulting image
            cv2.imshow('Video', annotated_image)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
