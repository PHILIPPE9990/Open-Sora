import cv2
import os
import numpy as np

def anti_aliasing():
    return (5, 5)

def resize():
    return cv2.INTER_LANCZOS4

def sharpening():
    return np.array([[0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]])

#Resize to 480p
def video_processing(input_path, enable_anti_aliasing=True, enable_resize=True, enable_sharpening=True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_full_path = os.path.join(script_dir, "../../samples/samples/", input_path)
    output_path = os.path.join(script_dir, "../../samples/enhanced/", "enhanced.mp4")
    
    
    for filename in os.listdir(os.path.join(script_dir, "../../samples/enhanced")):
        file_path = os.path.join(os.path.join(script_dir, "../../samples/enhanced"), filename)

        if os.path.isfile(file_path):
            os.remove(file_path) 


    cap = cv2.VideoCapture(input_full_path)
    if not cap.isOpened():
        raise IOError("Could not open input video file")
    
    # Get original properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Set output resolution
    #Resize to 480p if needed
    if enable_resize:
        out_width, out_height = 854, 480
    else:
        out_width, out_height = frame_width, frame_height
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if enable_sharpening:
                frame = cv2.filter2D(frame, -1, sharpening())
            if enable_resize:
                frame = cv2.resize(frame, (out_width, out_height), interpolation=resize())
            if enable_anti_aliasing:
                frame = cv2.GaussianBlur(frame, anti_aliasing(), 0)
            
            out.write(frame)
            
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    
    return "enhanced.mp4"

# #Load a video
# script_dir = os.path.dirname(os.path.abspath(__file__))
# video_path = os.path.join(script_dir, "../../video/")
# cap = cv2.VideoCapture(video_path+"sample_0000.mp4")

# #Width and Height
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# #Video Wiriter
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(video_path+"output1.mp4", fourcc, 24.0, (480, 360))


# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame_shapened = cv2.filter2D(frame, -1, sharpening())
#     frame_resized = cv2.resize(frame_shapened, (480, 360), interpolation=resize())
#     frame_anti_aliased = cv2.GaussianBlur(frame_resized, (3, 3), 0)
#     out.write(frame_anti_aliased)

# # Release the video objects
# cap.release()
# out.release()
# cv2.destroyAllWindows()



    