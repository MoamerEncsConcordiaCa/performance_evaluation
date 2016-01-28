import sys
import os

__author__ = 'mameri'

def make_dir_out(p_dir_out):
    if not os.path.exists(p_dir_out):
        os.mkdir(p_dir_out)

def read_scores_to_list(p_dir_in):

    top_list = [file_item for file_item in os.listdir(p_dir_in)
                if file_item[-14:] == 'gmm.result.top']
    lines_out = []
    for top_fn in top_list:
        top_fn_full = os.path.join(p_dir_in, top_fn)
        # print os.path.exists(top_fn_full), top_fn_full
        with open(top_fn_full, 'r') as f_h:

            local_line = f_h.readlines()
            sorted_line = sorted(local_line, key=lambda x:float(x.split()[4]), reverse= True )
            lines_out.extend(sorted_line)

    return lines_out


def write_scores_to_file(p_sorted_lines, p_dir_out):
    fn = 'sorted_score.txt'
    full_fn = os.path.join(p_dir_out, fn)
    with open(full_fn, 'w') as f_h:
        for local_line in p_sorted_lines:
            sp_lines = local_line.split()
            score_line = '{0}\t {1}\n'.format(sp_lines[2], sp_lines[4])
            f_h.write(score_line)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv  = sys.argv[1:]
        dir_in = argv[0]
        dir_out = argv[1]

        make_dir_out(dir_out)
        lines = read_scores_to_list(dir_in)
        print len(lines), len(lines)/16
        sorted_lines = lines
        sorted_lines = sorted(lines, key=lambda x:float(x.split()[4]), reverse= True )
        print sorted_lines
        write_scores_to_file(sorted_lines, dir_out)


    else:
        print 'call with input directory of scores with .top files'


