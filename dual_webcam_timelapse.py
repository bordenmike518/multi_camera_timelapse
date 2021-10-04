import cv2
import time
import os
from datetime import datetime

lights_on  = 7
lights_off = 1

length  = 5 # seconds
hours   = 18
minutes = hours * 60
fps     = 60
timelapse_delta = minutes / (length * fps) # Take photo every 3.6 minutes

camera_enabled = False
timelapses_made = False

def enable_camera(camera):
    for i in range(2):
        camera[i] = cv2.VideoCapture(i)
        camera[i].set(3, 1280)
        camera[i].set(4, 720)
    camera_enabled = True

def disable_camera(camera):
    for i in range(2):
        camera[i].release
    camera_enabled = False
        

def create_timelapse(dir_name):
    '''
        Need to get a list of all file names, sort, then save as video.
        Fix save location as were it is does not work!
    '''
    for i in range(2):
        video = cv2.VideoWriter(datetime.now() + '_timelapse_cam'+str(i), 0, fps, (1280, 720))
        dir_cam = dir_name + '/cam'+str(i)+'/'
        for _, _, filename in os.walk(dir_cam):
            video.write(cv2.imread(os.path.join(dir_cam, filename)))
    timelapse_made = True

def main():
    date_time = datetime.now()

    camera = [None, None]
    frame  = [None, None]

    while(True):
        hour = datetime.today().hour
        if(not(lights_off <= hour < lights_on)):
            if(not camera_enabled):
                enable_camera(camera)
            timelapse_made = False
            dir_name = datetime.today().strftime('%Y%m%d') + '_timelapse'
            if(datetime.today().day > date_time.day or not os.path.isdir(dir_name)):
                date_time = datetime.now();
                os.mkdir(dir_name)
                os.mkdir(dir_name + '/camera_0')
                os.mkdir(dir_name + '/camera_1')
            for i in range(2):
                _, frame[i] = camera[i].read()
                time.sleep(0.5)
                image_name = datetime.today().strftime('%Y%m%d_%H:%M:%S_cam'+str(i)+'.jpg')
                cv2.imwrite(dir_name+'/camera_'+str(i)+'/'+image_name, frame[i])
        elif(not timelapses_made):
            if (camera_enabled):
                disable_camera(camera)
            #create_timelapse(dir_name)

        time.sleep(timelapse_delta * 60)
        

if __name__ == '__main__':
    main()
