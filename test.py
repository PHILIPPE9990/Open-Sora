import cv2, os

# Open the video file

script_dir = os.path.dirname(os.path.abspath(__file__))
        #need to change later
video_path = os.path.join(script_dir, "../video/")

cap = cv2.VideoCapture(video_path+"sample_0000.mp4")

# Get the video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video
out = cv2.VideoWriter(video_path+"output.mp4", fourcc, 30.0, (256, 144))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame with anti-aliasing
    frame_resized = cv2.resize(frame, (256, 144), interpolation=cv2.INTER_LANCZOS4)

    # Write the processed frame to the output video
    out.write(frame_resized)

# Release the video objects
cap.release()
out.release()
cv2.destroyAllWindows()
