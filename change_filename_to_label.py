# 파일 이름을 라벨명으로 변경하는 파일입니다.
# 파일-라벨은 file_label.csv로부터 받아옵니다.
import os
import shutil
import pandas as pd

ROOT_PATH = os.getcwd()
INPUT_PATH = "original_videos"
OUTPUT_PATH = "renamed_videos"
LABEL_MAP = ["normal","biting","choking_cloth","choking_hand","hittingbody","hittinghead_floor","hittinghead_wall","kicking_wall","punching_floor","punching_wall","scratching_arm","scratching_neck","selfharm_tool"]
COUNT = {"normal" : 1, "biting" : 1, "choking_cloth" : 1, "choking_hand" : 1, "hittingbody" : 1, "hittinghead_floor" : 1, "hittinghead_wall" : 1, "kicking_wall" : 1, "punching_floor" : 1, "punching_wall" : 1, "scratching_arm" : 1, "scratching_neck" : 1, "selfharm_tool":1}
ERROR = []

csv = pd.read_csv('file_label.csv')
original_videos = os.listdir(os.path.join(ROOT_PATH, INPUT_PATH))
total = len(csv)

for idx, ser in csv.iterrows():
    filename = ser["filename"] + ".mp4"
    label = ser["label"]
    cam = ser["cam"]
    if filename in original_videos:
        rename = f"{cam}_{label}_{COUNT[label]}.mp4"
        original_file_path = os.path.join(ROOT_PATH, INPUT_PATH, filename)
        renamed_file_path = os.path.join(ROOT_PATH, OUTPUT_PATH, rename)
        shutil.copy2(original_file_path, renamed_file_path)
        print(f"[{idx}/{total}] Success!! ( {filename} -> {rename} )")
        COUNT[label] += 1
    else:
        ERROR.append(filename)
        print(f"[{idx}/{total}] Error!! ( {filename} )")

print(f"[ERROR] : {ERROR}")
print(f"[RESULT] Changed: {total - len(ERROR)}, Error: {len(ERROR)}")
print(f"[COUNT]: {COUNT}")

# run results
# [RESULT] Changed: 2193, Error: 0
# [COUNT]: {'normal': 627, 'biting': 161, 'choking_cloth': 92, 'choking_hand': 71, 'hittingbody': 131, 'hittinghead_floor': 148, 'hittinghead_wall': 146, 'kicking_wall': 78, 'punching_floor': 137, 'punching_wall': 145, 'scratching_arm': 206, 'scratching_neck': 201, 'selfharm_tool': 63}