import sys
import os

__author__ = 'mameri'

'''

Report the max score for each sample in the score file

'''

def make_dir_out(p_dir_out):
    if not os.path.exists(p_dir_out):
        os.mkdir(p_dir_out)

def get_score_file_list(p_dir_in):
    top_list = [file_item for file_item in os.listdir(p_dir_in)
                if file_item[-14:] == 'gmm.result.top']
    return top_list

def merge_max_score(p_dir_in, p_file_in_list,  p_dir_out, p_file_out, p_file_sorted_out):

    file_in_full =[ os.path.join(p_dir_in, file_in) for file_in in p_file_in_list ]
    file_out_full =  os.path.join(dir_out, p_file_out)

    file_handle_list  = map(lambda file_i: open(file_i), file_in_full)
    lines_list = [file_handle.readlines() for file_handle in file_handle_list]
    word_count = len(lines_list[0])
    class_count = len(lines_list)

    map(lambda file_i: file_i.close(), file_handle_list)

    score_max_list = []
    with open(file_out_full, 'w') as f_out:
        for word_j in range(0,word_count):
            score_of_word_j = []
            for class_i in range(0, class_count):
                score_of_word_j.append(lines_list[class_i][word_j].split() )
            sorted_word_list = sorted(score_of_word_j, key=lambda x:float(x[4]), reverse=True)
            word_j_max = sorted_word_list[0]
            # print reduce(lambda x, y : max(x[4], y[4]), score_of_word_j)
            max_word_str = word_j_max[2][: word_j_max[2].find('_')]
            word_j_max_str = '{0} {1}\n'.format(max_word_str, word_j_max[4])
            f_out.write(word_j_max_str)
            score_max_list.append(word_j_max_str)

    sorted_score_max_list= sorted(score_max_list, key= lambda x: float(x.split()[1]), reverse=True)
    file_out_full_sorted =  os.path.join(dir_out, p_file_sorted_out)
    with open(file_out_full_sorted, 'w') as f_sorted:
        f_sorted.writelines(sorted_score_max_list)

    # print file_handle_list[0].readline()
    # print file_handle_list[0].readline()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv  = sys.argv[1:]
        dir_in = argv[0]
        dir_out = argv[1]

        make_dir_out(dir_out)
        score_file_list = get_score_file_list(dir_in)
        print len(score_file_list), score_file_list[:]
        merge_max_score(dir_in, score_file_list, dir_out, 'max_score.txt', 'max_score_sorted.txt')
        # lines = read_scores_to_list(dir_in)
        # print len(lines), len(lines)/16
        # sorted_lines = lines
        # sorted_lines = sorted(lines, key=lambda x:float(x.split()[4]), reverse= True )
        # print sorted_lines
        # write_scores_to_file(sorted_lines, dir_out)

    else:
        print 'call in_score_dir out_score_dir '



