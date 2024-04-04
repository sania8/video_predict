import streamlit as st
import zipfile
import os
import cv2
import shutil
import base64
from PIL import Image

# Function to extract frames at a specific frame rate
def extract_frames(uploaded_file, output_path, frame_rate):
    video_bytes = uploaded_file.read()
    video_path = os.path.join(output_path, "uploaded_video.mp4")
    with open(video_path, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()
    count = 0
    frame_interval = int(cap.get(cv2.CAP_PROP_FPS) / frame_rate)
    while success:
        if count % frame_interval == 0:
            frame_path = os.path.join(output_path, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, image)  # Save frame as JPEG file
            st.image(Image.open(frame_path), caption=f"Frame {count + 1}")  # Display frame
        success, image = cap.read()
        count += 1
    cap.release()

    return count

# App UI
def main():
    st.set_page_config(
        page_title="Video_frame_predictor",
        page_icon="chart_with_upwards_trend"
    )
    st.markdown('<div class="custom-container"><p style="font-size:30px; color:purple;"><b>Welcome to the app!</b></p></div>', unsafe_allow_html=True)
    
    col1 = st.sidebar
    with col1:
        st.markdown('<h1><i class="fas fa-question-circle" style="color:green;"></i> How to Use</h1>', unsafe_allow_html=True)
        st.markdown("""
            <ol>
                <li>Upload videos/video using the file uploader below.</li>
                <li>Select the frame rate (frames per second).</li>
                <li>Click the 'Extract Frames' button to extract frames from the video.</li>
            </ol>
            """, unsafe_allow_html=True)
        st.markdown('''<p style="font-size:30px;"><b>Note:</b></p>''' ,unsafe_allow_html=True )
        st.markdown('''<p style="font-size:20px;">If uploading multiple videos, compress them into a zip file before uploading</p>''' ,unsafe_allow_html=True )
    
    uploaded_file = st.file_uploader("", type=["mp4", "avi", "mov"])
    frame_rate = st.sidebar.number_input("Frame Rate (fps)", min_value=1, step=1, value=1)
    
    # Initialize frames_extracted flag
    frames_extracted = False
    
    if uploaded_file is not None:
        st.write("Video uploaded successfully!")
        if st.button("Extract Frames"):
            with st.spinner("Extracting frames..."):
                # Create temporary directory to store frames
                temp_dir = "temp_frames"
                os.makedirs(temp_dir, exist_ok=True)

                # Extract frames from uploaded video and display them
                num_frames = extract_frames(uploaded_file, temp_dir, frame_rate)
                
                # Set flag to indicate frames have been extracted
                frames_extracted = True

    # Display download button if frames have been extracted
    if frames_extracted:
        st.success("Frames extracted successfully!")
    
    st.markdown('<p id="footer" style="text-align: center; color:#8B4000;"><b>Developed at Murthy Labs</b></p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
