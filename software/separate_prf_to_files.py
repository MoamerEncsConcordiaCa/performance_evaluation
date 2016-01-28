import os
import sys

__author__ = 'mameri'

def make_dir_out(p_dir_out):
    if not os.path.exists(p_dir_out):
        os.mkdir(p_dir_out)

def write_on_separate_files(p_dir_out, p_file_in):
    with open(p_file_in, 'r') as f_h:
        prf_lines = f_h.readlines()
        file_num = 0
        for i, line in enumerate(prf_lines):
            if 'PROF' in line:
                # print i, line
                split_line = line.split()
                prof = split_line[1].split(':')[1]

                file_out = os.path.join(p_dir_out, '{0}_.prf'.format(prof))
                h = int(split_line[5])
                # print h, file_out
                with open(file_out, 'a') as out_h:
                    out_h.writelines(prf_lines[i:i+h])

                file_num += 1
            else:
                pass
        print 'num of words:', file_num


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv  = sys.argv[1:]
        file_in = argv[0]
        dir_out = argv[1]

        make_dir_out(dir_out)
        write_on_separate_files(dir_out, file_in)

    else:
        print 'call with input prf file and out_directory'


