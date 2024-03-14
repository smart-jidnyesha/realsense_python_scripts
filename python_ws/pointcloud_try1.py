import cv2
import numpy as np
import pyrealsense2 as rs

# Setup
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth,rs.format.z16,30)
config.enable_stream(rs.stream.color,rs.format.bgr8,30)

# Start streaming
pipeline.start(config)

# Get intrinsics and profile
profile = pipeline.get_active_profile()
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
width,height = depth_intrinsics.width, depth_intrinsics.height
vertices=None
# Processing blocks
pc = rs.pointcloud()
aligner = rs.align(rs.stream.color)

try:
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = aligner.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frsame()

        if not depth_frame or not color_frame:
            continue

        else:
            color_img = np.asanyarray(color_frame.get_data())
            depth_img = np.asanyarray(depth_frame.get_data())

            points = pc.calculate(depth_frame)
            pc.map_to(color_frame)

            # Point cloud data to array
            v = points.get_vertices()

            vertices = np.asanyarray(v).view(np.float32).reshape(-1,3) # XYZ
        
        if vertices is not None:
            print("Depth: "+str(np.shape(depth_img)))
            print("Color: "+str(np.shape(color_img)))
            print("Vertices: "+str(np.shape(vertices)))
            raise KeyboardInterrupt


except KeyboardInterrupt:
    print("Exit")
    pipeline.stop()


