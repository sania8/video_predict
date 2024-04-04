import streamlit as st
import zipfile
import os
import cv2
import shutil
import base64
from PIL import Image
#set app name

# Set favicon
st.set_page_config(
        page_title="Video_frame_predictor",
        page_icon="chart_with_upwards_trend"
    )
def extract_frames(uploaded_file, output_path):
    video_bytes = uploaded_file.read()
    video_path = os.path.join(output_path, "uploaded_video.mp4")
    with open(video_path, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()
    count = 0
    while success:
        frame_path = os.path.join(output_path, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, image)  # Save frame as JPEG file
        st.image(Image.open(frame_path), caption=f"Frame {count + 1}")  # Display frame
        success, image = cap.read()
        count += 1
    cap.release()

    return count
#link the fontawsome 
css_example = '''
<!-- Import Font Awesome CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<!-- Use Font Awesome icons -->
<i class="fa-solid fa-square"></i>
<i class="fa-solid fa-dragon"></i>
<i class="fa-solid fa-paw"></i>
'''
st.write(css_example, unsafe_allow_html=True)
st.markdown("""
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-vNtQSlSCF83C5NcQklm8CwYiuPAxnqSmrMtVfu2TrS+duYq37D8tMbAoqx/MbLV58gVz2lPGTlBKHpxWrnM3dQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    </head>
""", unsafe_allow_html=True)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-right : 0.2rem;
                    
                }
        </style>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-container"><p style="font-size:30px; color:purple;"><b>Welcome to the app!</b></p></div>', unsafe_allow_html=True)
def main():
    col1 = st.sidebar
    with col1:

        st.markdown('<h1><i class="fas fa-question-circle" style="color:green;"></i> How to Use</h1>', unsafe_allow_html=True)
        st.markdown("""
            <ol>
                <li>Upload videos/video using the file uploader below.</li>
                <li>Click the link '<a href="./uploaded_videos.zip">Download the predicted frames</a>' to download the predicted frames.</li>
            </ol>
            """, unsafe_allow_html=True)
        st.markdown('''<p style="font-size:30px;"><b>Note:</b></p>''' ,unsafe_allow_html=True )
        st.markdown('''<p style="font-size:20px;">If uploading multiple videos, compress them into a zip file before uploading</p>''' ,unsafe_allow_html=True )
    st.write('The model takes in videos as input and returns the predicted frames by learning using sequence-to-sequence learning.')
    st.image('second.png', width=400)
    
    uploaded_file = st.file_uploader("", type=["mp4", "avi", "mov"])
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
                num_frames = extract_frames(uploaded_file, temp_dir)
                
                # Set flag to indicate frames have been extracted
                frames_extracted = True

    # Display download button if frames have been extracted
    if frames_extracted:
        st.success("Frames extracted successfully!")
        if st.button("Download Frames"):
            # Create a directory to store frames
            frames_dir = "extracted_frames"
            os.makedirs(frames_dir, exist_ok=True)
            # Move extracted frames to the directory
            for file in os.listdir(temp_dir):
                shutil.move(os.path.join(temp_dir, file), frames_dir)
            # Create a compressed file from the directory
            shutil.make_archive(frames_dir, 'zip', frames_dir)
            # Read the compressed file
            with open(f"{frames_dir}.zip", "rb") as f:
                zip_bytes = f.read()
            # Download the compressed file
            b64 = base64.b64encode(zip_bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download="extracted_frames.zip">Download extracted frames</a>'
            st.markdown(href, unsafe_allow_html=True)
            # Remove the directory and compressed file
            shutil.rmtree(frames_dir)
            os.remove(f"{frames_dir}.zip")
    st.markdown('<p id="footer" style="text-align: center; color:#8B4000;"><b>Developed at Murthy Labs</b></p>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
