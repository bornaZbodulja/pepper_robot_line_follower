#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2

class LineFollower():

    def __init__(self):
        self.vision_bridge = CvBridge()
        self.sensitivity = 15
        self.image_subscriber = rospy.Subscriber("/pepper_robot/camera/front/image_raw", Image, self.image_callback)
        self.velocity_publisher = rospy.Publisher("/pepper_robot/cmd_vel", Twist, queue_size=10)
        #self.processed_image_publisher = rospy.Publisher("/processed_image", Image, queue_size=10)

    def image_callback(self, data):
        
        try:
            converted_image = self.vision_bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

        except CvBridgeError:
            pass

        height, width, channels = converted_image.shape
        width_crop_decrement = width/4
        croped_image = converted_image[300:height, width_crop_decrement:(width-width_crop_decrement)]
        hsv_image = cv2.cvtColor(croped_image, cv2.COLOR_RGB2HSV)

        lower_white = np.array([0, 0, 255-self.sensitivity], dtype=np.uint8)
        upper_white = np.array([255, self.sensitivity, 255], dtype=np.uint8)

        filtered_image = cv2.inRange(hsv_image, lower_white, upper_white)

        #processed_image = self.vision_bridge.cv2_to_imgmsg(filtered_image, "passthrough")
        #self.processed_image_publisher.publish(processed_image)

        cv2.imshow('filtered_image', filtered_image)

        moments = cv2.moments(filtered_image, False)
        try:
            cx, cy = moments['m10']/moments['m00'], moments['m01']/moments['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2

        self.velocity_controller(cx, cy, width/2)

    def velocity_controller(self, cx, cy, width):
        error_x = cx - width/2
        vel = Twist()
        vel.linear.x = 0.1
        vel.angular.z = -error_x/100
        rospy.loginfo("Center of the line: {:.2f}, {:.2f}, error_x: {:.2f}".format(cx, cx, error_x))
        self.velocity_publisher.publish(vel)


def main():
    rospy.init_node("line_folowe")
    lineFollower = LineFollower()
    try: 
        rospy.spin()

    except rospy.ROSInterruptException: pass

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()