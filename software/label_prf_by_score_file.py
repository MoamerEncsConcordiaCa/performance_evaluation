import os
import sys

__author__ = 'mameri'

def label_prf_by_score_files(p_file_score, p_file_in, p_file_out):
    with open(p_file_in, 'r') as f_in:
        prf_lines = f_in.readlines()

    with open(p_file_score, 'r') as f_score:
        score_lines = f_score.readlines()

    word_i = 0
    with open(p_file_out, 'w') as f_out:
        for i, line in enumerate(prf_lines):
            if 'PROF' in line:
                split_line = line.split()
                prof = split_line[1].split(':')[1]
                h = int(split_line[5])
                # score_line = score_lines[word_i].split()
                word_i += 1
                # print score_line
                print i, word_i
                # score_value = float(score_line[1])
                label = prof
                # if score_value > 0:
                #     label = score_line[0]
                header = line.replace(prof, label)

                f_out.write(header)
                f_out.writelines(prf_lines[i+1:i+1+h])
            else:
                pass



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

        file_score = argv[0]
        file_in = argv[1]
        file_out = argv[2]

        label_prf_by_score_files(file_score, file_in, file_out)

    else:
        print 'call score_file input_file output_file '


