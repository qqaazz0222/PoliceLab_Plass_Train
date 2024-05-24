# 동영상에서 유효한 시간에 대해 라벨링을 작성하는 도구입니다.
# labeldata.csv에 있는 파일을 입력받습니다.
# label_timeline_{라벨항목}.csv로 저장됩니다.
import os
import csv
import cv2
import pandas as pd
import datetime
import math
import time

ROOT_PATH = os.getcwd()
VIDEO_PATH = "renamed_videos"
LABEL_DATA = "labeldata.csv"
OUTPUT_DATA = []
OUTPUT_NAME = "label_timeline.csv"
SELECTED_LABEL = ""
BREAK_STATE = False

def gen_output_file():
    f = open(OUTPUT_NAME,'w', newline='')
    wr = csv.writer(f)
    wr.writerow(['filename','start', 'end'])

def get_label_map(csv):
    label_col = csv['label']
    label_list = label_col.tolist()
    label_map = sorted(set(label_list))
    print(f"[LABEL_MAP] : {label_map}")
    return label_map

def select_label(label_map):
    global OUTPUT_NAME, SELECTED_LABEL
    while True:
        input_label = input(" - 작업하실 라벨 항목을 입력해주세요 : ")
        if input_label in label_map:
            SELECTED_LABEL = input_label
            OUTPUT_NAME = f"label_timeline_{input_label}.csv"
            break
        else:
            print(" - 유효하지 않은 라벨 항목입니다.")
    print(f"[LABEL SELECTED!] Selected Label : {SELECTED_LABEL}, Output Filename : {OUTPUT_NAME}")
        

def process_labeling(label_data_csv):
    gen_output_file()
    for idx, ser in label_data_csv.iterrows():
        if BREAK_STATE:
            break
        filename = ser["filename"] + ".mp4"
        label = str(ser["label"]).strip()
        if label == SELECTED_LABEL:
            print("-------------------------------------------------------------------------")
            target_path = os.path.join(ROOT_PATH, VIDEO_PATH, filename)
            labeling_video(target_path)


def labeling_video(file):
    global OUTPUT_NAME, BREAK_STATE
    f = open(OUTPUT_NAME,'a', newline='')
    wr = csv.writer(f)
    video = cv2.VideoCapture(file)
    video_name = file.split("/")[-1]
    fps = round(video.get(cv2.CAP_PROP_FPS))
    total_fps = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_time = math.floor(total_fps/fps)
    cur_time = 0
    valid_timeline = []
    print(f" - 작업중인 파일 : {file}")
    print(f" - 총 동영상 길이 : {video_time}초 / 총 프레임 수 : {total_fps}")
    for cur_frame in range(0, total_fps, fps):
        if BREAK_STATE:
            break
        video.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        ret, frame = video.read()
        if ret:
            print(f" - [현재 시간] : {cur_time}")
            text = f"{cur_time} / {video_time}"
            org = (50,100)
            fontFace = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 2
            color = (0, 0, 255)
            thickness = 4
            lineType = cv2.LINE_AA
            cv2.putText(frame, text, org, fontFace, fontScale, color, thickness, lineType)
            cv2.imshow('Labeling', frame)
            print(" - 유효성을 입력하세요(yes: 1, no: 2) : ")
            while True:
                key = cv2.waitKey(0)
                if key == ord('1'):
                    valid_timeline.append(cur_time)
                    break
                if key == ord('2'):
                    break
                if key == ord('q'):
                    BREAK_STATE = True
                    break
            cur_time += 1
        else:
            break
    timelines = get_range(valid_timeline)
    for tl in timelines:
        if tl[1] - tl[0] > 0:
            print("- 작성됨", video_name, timelines)
            wr.writerow([video_name, tl[0], tl[1]])
    f.close()

def get_range(arr):
    result = []
    temp = []
    prev = -2
    for t in arr:
        if t != prev + 1:
            if len(temp) > 0:
                result.append(temp)
                temp = []
            temp = [t, t]
        else:
            temp[1] = t
        if t == arr[-1]:
            result.append(temp)
        prev = t
    return result

def main():
    global OUTPUT_FILE, SELECTED_LABEL, BREAK_STATE
    VIDEOS = os.listdir(os.path.join(ROOT_PATH, VIDEO_PATH))
    label_data_csv = pd.read_csv(LABEL_DATA)
    LABEL_MAP = get_label_map(label_data_csv)
    select_label(LABEL_MAP)
    if os.path.isfile(OUTPUT_NAME):
        check = input(f"[WARNING!!!] 이미 파일이 존재합니다. 작업을 시작하면 기존 파일은 삭제됩니다. 시작하시겠습니까? (yes/no)")
        if check == 'yes':
            process_labeling(label_data_csv)
            print("작업이 완료되었습니다.")
        else:
            print("작업이 취소되었습니다.")
    else:
        process_labeling(label_data_csv)
        print("작업이 완료되었습니다.")
    


        
    
main()