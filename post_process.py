from file_index import index_recording, index_data
from select_bug_file import select_bug_test_cases

if __name__ == "__main__":
    direct = '/media/zhouyuan/MyBookPro/zhouyuan/ga_2/'
    index_recording(direct)
    index_data(direct)
    select_bug_test_cases(direct)