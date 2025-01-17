import cv2
import os
import numpy as np

# #Super-sampling + Low-pass filter
def anti_aliasing():
    return (5, 5)

#Upscaling 
def resize():
    return cv2.INTER_LANCZOS4

#Sharpening
def sharpening():
    return np.array([[0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]])


#Load a video
script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, "../video/")
cap = cv2.VideoCapture(video_path+"sample_0001.mp4")

#Width and Height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Video Wiriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_path+"output1.mp4", fourcc, 24.0, (480, 360))


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_shapened = cv2.filter2D(frame, -1, sharpening())
    frame_resized = cv2.resize(frame_shapened, (480, 360), interpolation=resize())
    frame_anti_aliased = cv2.GaussianBlur(frame_resized, (3, 3), 0)
    out.write(frame_anti_aliased)

# Release the video objects
cap.release()
out.release()
cv2.destroyAllWindows()



    