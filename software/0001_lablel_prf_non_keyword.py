import os
import sys

__author__ = 'mameri'
'''
Set all prof to the same lexicon.

'''

def replace_prof_with(p_label, p_file_in, p_file_out):
    with open(p_file_in, 'r') as f_in:
        prf_lines = f_in.readlines()

        with open(p_file_out, 'w') as f_out:
            for i, line in enumerate(prf_lines):
                if 'PROF' in line:
                    split_line = line.split()
                    prof = split_line[1].split(':')[1]
                    h = int(split_line[5])
                    header = line.replace(prof, p_label)
                    f_out.write(header)
                    f_out.writelines(prf_lines[i+1:i+1+h])
                else:
                    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv  = sys.argv[1:]
        file_in = argv[0]
        file_out = argv[1]
        label = 'non-keyword'
        if len(argv) > 3:
            label = argv[2]
        replace_prof_with(label, file_in, file_out)
    else:
        print 'call input_file output_file non_keyworkd_label'


