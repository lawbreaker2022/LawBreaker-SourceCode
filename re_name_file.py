import os

direct = '/media/zhouyuan/MyBookPro/zhouyuan/random_1/'
sub_folders = os.listdir(direct)
sub_folders = sorted(sub_folders)
for folder in sub_folders:
    sub_folder = direct + folder + '/data/'
    files = os.listdir(sub_folder)

    for file in files:
        first_spilt = file.split(sep='-')[0]
        if len(first_spilt) > 6:
            old_name = sub_folder + file
            data_str = file[6:16]
            new_data_str = data_str[6:10] + '-' + data_str[3:5] + '-' + data_str[0:2]
            new_file = file[0:6] + '-' + new_data_str + file[16:]
            new_name = sub_folder + new_file
            os.rename(old_name, new_name)


