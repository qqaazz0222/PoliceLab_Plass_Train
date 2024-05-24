# 파일 목록을 라벨데이터로 만드는 파일입니다.
# labeldata.csv로 저장됩니다.
import os
import csv

ROOT_PATH = os.getcwd()
VIDEO_PATH = "renamed_videos"
OUTPUT_DATA = []
OUTPUT_NAME = "labeldata.csv"
OUTPUT_FILE = open(OUTPUT_NAME,'w', newline="")

original_videos = os.listdir(os.path.join(ROOT_PATH, VIDEO_PATH))
wr = csv.writer(OUTPUT_FILE)

for video in original_videos:
    temp = video.split("_")
    filename = video.split(".")[0]
    label = ""
    if len(temp) == 3:
        label = temp[1]
    else:
        label = temp[1] + "_" + temp[2]
    row = [filename, label]
    OUTPUT_DATA.append(row)
wr.writerows(OUTPUT_DATA)
print(f"File Saved! ( path: {os.path.join(ROOT_PATH, OUTPUT_NAME)})")
OUTPUT_FILE.close()