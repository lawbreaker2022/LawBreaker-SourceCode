import json
import os
from natsort import natsorted

if __name__ == "__main__":
    directory = '/media/zhouyuan/MyBookPro/zhouyuan/ga_1/'
    sub_directory = 'intersection1/results_L/'
    files = os.listdir(directory + sub_directory)
    files = natsorted(files)
    for file in files:
        if 'result' in file:
            with open(directory + sub_directory + file) as f:
                content = json.load(f)
                distance = content['minEgoObsDist']
                if distance > 0:
                    print(file.split(sep='-')[0])

