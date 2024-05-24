# 동영상에서 유효한 시간에 대해 라벨링을 작성하는 도구입니다.
# labeldata.csv에 있는 파일을 입력받습니다.
# label_timeline_{라벨항목}.csv로 저장됩니다.
import os
import csv
import cv2
import datetime
import math
import time

ROOT_PATH = os.getcwd()
INPUT_PATH = "renamed_videos"
OUTPUT_PATH = "cutted_videos"
TIMELINE_DATA = "valid_timeline_data.csv"

def read(csvfile):
    result = []
    with open(csvfile, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for line in reader:
            result.append(line)
    return result[1:]

def cut_track(videofile, start, end):
    video = cv2.VideoCapture(os.path.join(ROOT_PATH, INPUT_PATH, videofile))
    fps = round(video.get(cv2.CAP_PROP_FPS))
    extracted_frames = []
    for cur_frame in range(int(start) * fps, int(end) * fps):
        video.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        ret, frame = video.read()
        if not ret:
            break
        extracted_frames.append(frame)
    video.release()
    gen_vidoe(videofile, extracted_frames)

def gen_vidoe(videofile, frames):
    video = cv2.VideoWriter(os.path.join(ROOT_PATH, OUTPUT_PATH, videofile), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        video.write(frame)
    video.release()

def main():
    data = read(TIMELINE_DATA)
    data_length = len(data)
    for idx in range(len(data)):
        if os.path.isfile(os.path.join(ROOT_PATH, INPUT_PATH, data[idx][0])):
            print(f"GEN {idx + 1}/{data_length}")
            cut_track(data[idx][0], data[idx][1], data[idx][2])



        
    
main()