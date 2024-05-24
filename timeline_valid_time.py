import os
import csv

ROOT_PATH = os.getcwd()
INPUT_PATH = "labeling"
OUTPUT_PATH = "valid_labeling"
DEFAULT_VALID_TIME = 5

def read(filename):
    result = []
    with open(os.path.join(ROOT_PATH, INPUT_PATH, f'{filename}.csv'), 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for line in reader:
            result.append(line)
    return result[1:]

def check_valid(data):
    result = []
    for row in data:
        if int(row[2]) - int(row[1]) >= 5:
            result.append(row)
    return result

def write(filename, data):
    with open(os.path.join(ROOT_PATH, OUTPUT_PATH, f'{filename}_valid.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    labelfiles = os.listdir(os.path.join(ROOT_PATH, INPUT_PATH))
    for labelfile in labelfiles:
        filename = labelfile.split(".")[0]
        data = read(filename)
        valid_data = check_valid(data)
        write(filename, valid_data)

main()