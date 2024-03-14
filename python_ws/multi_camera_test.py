import pyrealsense2 as rs
import numpy as np
import cv2

# Define pipelines for different cameras

pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_stream(rs.stream.depth,640,480,rs.format.z16,30) 
config_cam1.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30) 

pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_stream(rs.stream.depth,640,480,rs.format.z16,30) 
config_cam2.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30) 

# Start the pipelines
pipe_cam1.start(config_cam1)
pipe_cam2.start(config_cam2)

try:
    while True:

        frames_cam1 = pipe_cam1.wait_for_frames()
        frames_cam2 = pipe_cam2.wait_for_frames()
        
        depth_frame_cam1 = frames_cam1.get_depth_frame()
        depth_frame_cam2 = frames_cam2.get_depth_frame()

        color_frame_cam1 = frames_cam1.get_color_frame()
        color_frame_cam2 = frames_cam2.get_color_frame()

        if not depth_frame_cam1 or not color_frame_cam1:
            print("Camera 1 streams failed")
            continue

        if not depth_frame_cam2 or not color_frame_cam2:
            print("Camera 2 streams failed")
            continue
        
        # Convert to np arrays
        depth_img_cam1 = np.asanyarray(depth_frame_cam1.get_data())
        depth_img_cam2 = np.asanyarray(depth_frame_cam2.get_data())
        color_img_cam1 = np.asanyarray(color_frame_cam1.get_data())
        color_img_cam2 = np.asanyarray(color_frame_cam2.get_data())
        
        cv2.namedWindow('cam1-color',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('cam1-color',color_img_cam1)
        cv2.namedWindow('cam2-color',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('cam2-color',color_img_cam2)
        cv2.namedWindow('cam1-depth',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('cam1-depth',depth_img_cam1)
        cv2.namedWindow('cam2-depth',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('cam2-depth',depth_img_cam2)
        cv2.waitKey(1)
except KeyboardInterrupt:
    print("Interrupted! Closing program")
except Exception as e:
    print(e)
finally:
    pipe_cam1.stop()
    pipe_cam2.stop()