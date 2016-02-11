import os, sys
'''
Put default value, if there is a 0 in the feature vector
'''
def correct_meta_file(meta_file, meta_out_file):
    with open(meta_file, 'r') as f_in:
        with open(meta_out_file, 'w') as f_out:

            for line in f_in:
                if 'horizontal = 1;vertical = 1;orientation = 1;' in line:
                    line_new = line.replace('horizontal = 1;vertical = 1;orientation = 1;',
                                            'horizontal = 1;vertical = 3;orientation = 8;')
                    f_out.write(line_new)
                else:
                    f_out.write(line)


def correct_feature_file(featrue_file, feature_out_file):
    with open(featrue_file, 'r') as f_in:
        with open(feature_out_file, 'w') as f_out:
            for line in f_in:
                if line == '0\n':
                    line_new = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \n'
                    f_out.write(line_new)
                else:
                    f_out.write(line)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv  = sys.argv[1:]
        meta_file = argv[0]
        feature_file = argv[1]
        meta_out_file = argv[2]
        feature_out_file  = argv[3]

        correct_meta_file(meta_file, meta_out_file)
        correct_feature_file(feature_file, feature_out_file)

        # lines = read_scores_to_list(dir_in)
        # print len(lines), len(lines)/16
        # sorted_lines = lines
        # sorted_lines = sorted(lines, key=lambda x:float(x.split()[4]), reverse= True )
        # print sorted_lines
        # write_scores_to_file(sorted_lines, dir_out)

    else:
        print 'call meta_file feature_file meta_out featuer_out'



