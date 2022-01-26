import os

direct = 'ga_1/'
sub_directs = os.listdir(direct)
for folder in sub_directs:
    sub_direct = direct + folder + '/results/'
    files = os.listdir(direct + sub_direct)
    for file in files:
        if 'test' in file:
            command = 'cyber_recorder play -f ' + file
            os.system(command)