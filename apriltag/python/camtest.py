#!/usr/bin/env python

'''Demonstrate Python wrapper of C apriltag library by running on camera frames.'''
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import cv2
import apriltag

# for some reason pylint complains about members being undefined :(
# pylint: disable=E1101

def main():

    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltag Python bindings')
    parser2 = ArgumentParser(
        description='test apriltag Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    parser2.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=1,
                        help='Movie to load or integer ID of camera device')

    apriltag.add_arguments(parser)

    apriltag.add_arguments(parser2)

    options = parser.parse_args()
    options2 = parser2.parse_args()


    try:
        cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
    except ValueError:
        cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)


    window = 'Camera'
    cv2.namedWindow(window)

    window2 = 'Camera2'
    cv2.namedWindow(window2)
 
    # set up a reasonable search path for the apriltag DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    
    detector = apriltag.Detector(options, searchpath = apriltag._get_demo_searchpath())
    detector2 = apriltag.Detector(options2, searchpath = apriltag._get_demo_searchpath())

    while True:

        success, frame = cap.read()
        success2, frame2 = cap2.read()

        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        detections, dimg = detector.detect(gray, return_image=True)
        detections2, dimg2 = detector2.detect(gray2, return_image=True)
        
        num_detections = len(detections)
        num_detections2 = len(detections2)
        
        #print('Detected {} tags with camera 1.\n'.format(num_detections))
        #print('Detected {} tags with camera 2.\n'.format(num_detections2))
        
        for i, detection in enumerate(detections):
            #print('Detection {} of {}:'.format(i+1, num_detections))
            #print()
            #print(detection.tostring(indent=2))
            #print()
            #print(detection.tag_id)
            # print(detection.center)
            #print(detection.corners[1])
            #print(detection.corners)
            #     'DetectionBase','tag_family, tag_id, hamming, goodness, decision_margin,'homography, center, corners')
            #
            #print(detection.corners[0][0])
            #print(detection.corners[0][1])
            #print(detection.corners[2])
            #print(detection.corners[3])
            
            top_edge_x = detection.corners[0][0] - detection.corners[1][0]
            top_edge_y = detection.corners[0][1] - detection.corners[1][1]
            #print("top_x: ", top_edge_x)
            #print("top_y: ", top_edge_y)
            
            right_edge_x = detection.corners[1][0] - detection.corners[2][0]
            right_edge_y = detection.corners[1][1] - detection.corners[2][1]
            #print("right_x: ", right_edge_x)
            #print("right_y: ", right_edge_y)         
            
            bottom_edge_x = detection.corners[2][0] - detection.corners[3][0]
            bottom_edge_y = detection.corners[2][1] - detection.corners[3][1]
            print("bottom_x: ", bottom_edge_x)
            print("bottom_y: ", bottom_edge_y)
            
            left_edge_x = detection.corners[3][0] - detection.corners[0][0]
            left_edge_y = detection.corners[3][1] - detection.corners[0][1]
            print("left_x: ",left_edge_x)
            print("left_y: ", left_edge_y)
            
            
            dot_product_TR = top_edge_x * right_edge_x + top_edge_y * right_edge_y
            print("TR: ", dot_product_TR)
            
            dot_product_RB = right_edge_x * bottom_edge_x + right_edge_y * bottom_edge_y
            print("RB: ", dot_product_RB)
                        
            dot_product_BL = bottom_edge_x * left_edge_x + bottom_edge_y * left_edge_y
            print("BL: ", dot_product_BL)

            dot_product_LT = left_edge_x * top_edge_x + left_edge_y * top_edge_y
            print("LT: ", dot_product_LT)
            
            if(dot_product_TR < 0 and dot_product_LT > 0):
                print("Closer to the right edge than the left edge")
            if(dot_product_TR > 0 and dot_product_LT < 0):
                print("Closer to the left edge than the right edge")
            print("Angle Approximation: ", max(abs(dot_product_TR), abs(dot_product_LT))/8000*80)

            #top_edge = ()
            #right_edge = ()
            #bottom_edge = ()
            
            # center will be 0 on left and 600 on right
            # center will be 0 on top and 500 on top

        #for i, detection2 in enumerate(detections2):
            #print('Detection2 {} of {}:'.format(i+1, num_detections2))
            #print()
            #print(detection2.tostring(indent=2))
          #  print()

        overlay = frame // 2 + dimg[:, :, None] // 2
        #overlay2 = frame2 // 2 + dimg2[:, :, None] // 2

        cv2.imshow(window, overlay)
        #cv2.imshow(window2, overlay2)

        k = cv2.waitKey(1)
 
        if k == 27:
            break

if __name__ == '__main__':
    main()
