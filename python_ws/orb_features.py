import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30) 

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        img = np.asanyarray(color_frame.get_data())
        plt.imshow(img)
        plt.show()
except KeyboardInterrupt:
    print("Exiting program")
    pipeline.stop()