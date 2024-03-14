import pyrealsense2 as rs
import numpy as np

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth,640,480,rs.format.z16,30) 
config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30) 

pipeline.start(config)

try:
    while True:

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_scale = depth_frame.get_units() # 1mm scale for D455
        
        depth_camera_intrinsics = depth_frame.profile.as_video_stream_profile().get_intrinsics()
        color_camera_intrinsics = color_frame.profile.as_video_stream_profile().get_intrinsics()
        depth_to_color_extrinsics = depth_frame.profile.get_extrinsics_to(color_frame.profile) 
        color_to_depth_extrinsics = color_frame.profile.get_extrinsics_to(depth_frame.profile)
        
        # print('Depth Intrinsics:')
        # print(depth_camera_intrinsics)
        # print('Color Intrinsics:')
        # print(color_camera_intrinsics)
        # print('Depth to Color Extrinsics:')
        # print(depth_to_color_extrinsics)
        # print('Color to Depth Extrinsics:')
        # print(color_to_depth_extrinsics)
        # print('=====================================')
        # np_depth = np.asanyarray(depth_frame.get_data())
        # u,v = 325,201
        # depth_val = depth_frame.get_distance(u,v) # in m
        # # calculate real world coords
        # x = (u-camera_intrinsics.ppx)*depth_val/camera_intrinsics.fx
        # y = (v-camera_intrinsics.ppy)*depth_val/camera_intrinsics.fy
        # z = depth_val

        # u,v = 201,325
        # print(f"Pixels: {u,v}, scale : {depth_scale} calc depth: {depth_val} m, arr depth: {np_depth[v][u]} real world coord {x,y,z}")

except KeyboardInterrupt:
    print("Exiting program")
    pipeline.stop()