#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('pip install --user opencv-python')


# In[9]:


import os
import matplotlib.pyplot as plt
import cv2
import numpy as np


# In[10]:


#cut frames and extracting them in to a directory file 


# In[11]:


video_file = r"C:\Users\idanb\OneDrive\Desktop\IMG_0 (1).MOV"
output_directory = os.path.join(os.path.dirname(video_file), "IMG_0 (1)_frames")
panorama_directory = os.path.join(os.path.dirname(video_file), "Panorama")
exclude_files = ['panorama.jpg', 'manual_panorama.jpg']

def extract_frames(video_file):
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_file}")
        return
    
    frame_rate = 2  # Frames every 0.5 seconds
    frame_count = 0
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    output_directory = os.path.join(os.path.dirname(video_file), f"{video_name}_frames")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    print(f"Frames will be saved in: {output_directory}")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_count += 1
        if frame_count % int(cap.get(cv2.CAP_PROP_FPS) / frame_rate) == 0:
            output_file = os.path.join(output_directory, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_file, frame)
            print(f"Frame {frame_count} has been extracted and saved as {output_file}")
    
    cap.release()
    print(f"Finished extracting frames. Total frames extracted: {frame_count}")


# In[12]:


#loading the images from the directory and return a list of loaded images


# In[13]:


def load_images_from_folder(folder, exclude_files=[]):
    images = []
    files = sorted([f for f in os.listdir(folder) if f not in exclude_files])
    for filename in files:
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# In[20]:


def display_images_grid(images, grid_size=(3, 3)):
    fig, axes = plt.subplots(grid_size[0], grid_size[1], figsize=(15, 15))
    axes = axes.flatten()
    
    for img, ax in zip(images, axes):
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img_rgb)
            ax.axis('off')

    # Hide any remaining empty subplots
    for ax in axes[len(images):]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

folder_path = r"C:\Users\idanb\OneDrive\Desktop\IMG_0 (1)_frames"   # Replace with your folder path
exclude_files = []  # Add any files you want to exclude

images = load_images_from_folder(folder_path, exclude_files)
display_images_grid(images, grid_size=(5, 10))



# In[28]:


#enhancing the images in the list to improve the preformence of the all proccess


# In[29]:


def enhance_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)
    return image


# In[30]:


#Resize images to ensure they are of manageable size


# In[31]:


def resize_images(images, max_width=1000):  
    resized_images = []
    for img in images:
        height, width = img.shape[:2]
        if width > max_width:
            new_height = int(height * (max_width / width))
            img = cv2.resize(img, (max_width, new_height))
        resized_images.append(img)
    return resized_images


# In[32]:


#Crop the largest rectangular region from the panorama without black borders


# In[33]:


def crop_panorama(panorama):
    gray = cv2.cvtColor(panorama, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    
    x, y, w, h = cv2.boundingRect(contour)
    cropped = panorama[y:y+h, x:x+w]
    return cropped


# In[34]:


#Stitch a list of images into a panorama using SIFT for feature detection


# In[35]:


def stitch_images(images):
    stitcher = cv2.Stitcher_create()
    status, pano = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        print(f"Error during stitching: {status}")
        return None
    return pano


# # Converting the video into frames

# In[36]:


# Ensure the panorama directory exists
if not os.path.exists(panorama_directory):
    os.makedirs(panorama_directory)

# Extract frames from the video
extract_frames(video_file)

# Load images from the folder
images = load_images_from_folder(output_directory, exclude_files)

# Resize images to ensure they are of manageable size
resized_images = resize_images(images)

# Enhance images (optional, depending on your use case)
enhanced_images = [enhance_image(img) for img in resized_images]

# Stitch the enhanced images
stitched_image = stitch_images(enhanced_images)

# Crop the stitched panorama to remove black borders
if stitched_image is not None:
    cropped_image = crop_panorama(stitched_image)
    panorama_file = os.path.join(panorama_directory, 'panorama.jpg')
    cv2.imwrite(panorama_file, cropped_image)
    print(f"Panorama created and saved as {panorama_file}")
    # Display the cropped image
    plt.figure(figsize=(20, 10))
    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
else:
    print("Stitching failed.")


# In[ ]:





# In[ ]:




