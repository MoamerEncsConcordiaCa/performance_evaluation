
import sys, os
import shutil
import importlib
from os.path import expanduser

sys.path.append('config')

__author__ = 'mameri'

'''
performance evaluation by Trec_eval
'''


def extract_param_form_file_name (p_prop_item) :

    cv_list = ''
    keyword_list = ''
    target_list = ''
    alg_list = ''
    cn_list = ''
    ce_list = ''
    alpha_list = ''

    splited_prop_item = p_prop_item.split('_')

    cv_str = p_prop_item[:p_prop_item.find('_train_')]
    if not cv_str in cv_list:
        cv_list = (cv_str)

    key_str = p_prop_item[ p_prop_item.find('_train_') + 7: p_prop_item.find(splited_prop_item[-9]) - 1]
    if not key_str in keyword_list:
        keyword_list = (key_str)

    target_str = splited_prop_item[-9]
    if not target_str in target_list:
        target_list = (target_str)

    alg_str = splited_prop_item[-8]
    if not alg_str in alg_list:
        alg_list = (alg_str)

    cn_str = splited_prop_item[-6]
    if not cn_str in cn_list:
        cn_list = (cn_str)

    ce_str = splited_prop_item[-4]
    if not ce_str in ce_list:
        ce_list = (ce_str)

    alpha_str = splited_prop_item[-2]
    if not alpha_str in alpha_list:
        alpha_list = (alpha_str)

    return [ cv_list, keyword_list, target_list, alg_list, cn_list, ce_list, alpha_list ]

def read_file_data(p_file_name):

    if not os.path.exists(p_file_name):
        print 'file {0} \n does not exist'.format(p_file_name)
        return

    file_h = open(p_file_name, 'r')
    lines_read =  file_h.readlines()
    file_h.close()


    results_by_keyword_id ={}

    if len(lines_read) < 1:
        return results_by_keyword_id

    for line_item in lines_read:

        splited_line = line_item.split()
#         print splited_line
        #print 'file', p_file_name
        source_id = splited_line[0].split('|')[2]

        target_ids = splited_line[1:]
        one_row_dict = {}

        for target_item in target_ids:

            [id_mixed, value_str] =  target_item.split(',')

            id_target =  id_mixed.split('|')[2]
            value_float =  float(value_str)

            one_row_dict[id_target] = value_float

#         print one_row_dict
        results_by_keyword_id[source_id]  = one_row_dict

#     print p_file_name
    return results_by_keyword_id


def save_all_param_to_file(p_analysis_dict, p_dir):

    analysis_file_name = p_dir + '/performance_all.txt'
    file_h = open(analysis_file_name, 'w')

    key_cv_norm_list = p_analysis_dict.keys()
    key_cv_norm_list.sort()

    for key_cv_norm_item in key_cv_norm_list:

        value_cv_norm = p_analysis_dict.get(key_cv_norm_item, [])

        file_h.write('________________________________________________\n')
        file_h.write(str(key_cv_norm_item) + '\n')

        max_roc = 0
        max_pr_re = 0

        value_cv_norm.sort(key =lambda x: x[6])

        for cv_norm_item in value_cv_norm:

            [ cv, norm ,alg  , cn , ce , alpha, score_dict]  = cv_norm_item

            print cv , norm, alg , cn , ce, alpha

            pr_re = score_dict[0]['pr_re']
            roc = score_dict[1]['map']
            if pr_re >  max_pr_re:
                max_pr_re = pr_re
            if roc > max_roc:
                max_roc = roc

            file_h.write('{0}, {1}, pr_re:{2:5}, map:{3:5}\n'.format(cn, ce, pr_re, roc))



        file_h.write('MAX\n')
        file_h.write('pr_re:{0:5}, map:{1:5}\n'.format( max_pr_re, max_roc))



    file_h.close()



def compute_min_per_key_word_list(keyword_score_dict):

    min_score_list = []

    key_id_list = keyword_score_dict.keys()

    target_id_list = keyword_score_dict[key_id_list[0]]

    for target_id_item in target_id_list:
        score_per_key_list = [ keyword_score_dict[key_id][target_id_item] for key_id in key_id_list ]
        score_min = min(score_per_key_list)

        target_trim = target_id_item[:-4]
        key_trim = key_id[:-4]

        min_score_list.append([score_min, target_trim, key_trim])


    return min_score_list


def transcribe_score_ids(p_score_id_list, p_all_word_list):
    transcribe_list = []

    for score in p_score_id_list:
        s_value = score[0]
        first_str = p_all_word_list[ score[1]  ]
        second_str = p_all_word_list[ score[2] ]

        s1_l = first_str.split('-')
        s2_l = second_str.split('-')

        s1_l_c = [el for el in s1_l if len(el) ==1]
        s2_l_c = [el for el in s2_l if len(el) ==1]

        is_equal = True
        if len(s2_l_c) == 0 and len(s1_l_c) == 0:
            is_equal = (second_str == first_str)
        else:

            str_1 = ''.join(s1_l_c)
            str_2 = ''.join(s2_l_c)
            is_equal = (str_1 == str_2)
        #end if len
        # if (first_str == second_str) != is_equal :
        #     print first_str , second_str , is_equal, first_str== second_str
        score_id_trans = [score[0], is_equal, score[1], score[2] ]

        transcribe_list.append(score_id_trans)


    return transcribe_list

def make_rel_file(score_id_list_transcribed, file_rel, cv):

    if len(score_id_list_transcribed) == 0:
        return

    file_h  = open(file_rel, 'w')

    for score_item in score_id_list_transcribed:
        [value, is_equal, id1, id2 ]  = score_item

        id1_id2 = id1 + id2
        rel = 0
        if is_equal:
            rel = 1

        str_line = '{0} 0 {1} {2}\n'.format(cv, id1_id2, rel)

        file_h.write(str_line)

    file_h.close()


def make_top_file(score_id_list_transcribed, file_top, cv):

    if len(score_id_list_transcribed) == 0:
        return

    file_h  = open(file_top, 'w')

    for score_item in score_id_list_transcribed:
        [value, is_equal, id1, id2 ]  = score_item

        id1_id2 = id1 + id2
        rel = 0
        if is_equal:
            rel = 1
        value = -value
        str_line = '{0} Q0 {1} 0 {2} hws\n'.format(cv, id1_id2, value)

        file_h.write(str_line)

    file_h.close()

def get_map_rpc(file_result):

    file_h =open (file_result, 'r')

    lines = file_h.readlines()

    file_h.close()
    map_val =0
    r_pr =0


    for line in lines:
        if 'map' in line and 'all' in line:
            map_val = float( line.split()[2] )

        if 'Rprec' in line and 'all' in line:
            r_pr = float( line.split()[2] )

    return [map_val, r_pr]

def get_plot_data(file_result, file_plot):

    file_h =open (file_result, 'r')

    lines = file_h.readlines()

    file_h.close()


    file_h_plot = open(file_plot, 'w')

    for line in lines:
        if 'iprec_at_recall_' in line:
            # print line
            line_split = line.split()
            if line_split[1] == 'all' :
                pr_val = float( line_split[2])
                recal_val = float(line_split[0].replace('iprec_at_recall_', ''))

                str_line = '{0} {1}\n'.format(recal_val, pr_val)
                file_h_plot.write(str_line)

    file_h_plot.close()


    return


def get_plot_gnup(file_plot, file_gnup, file_png, param_db):

    file_h = open(file_gnup, 'w')

    file_h.write('set terminal png font "Arial, 18" \n')
    file_h.write('set output "{0}" \n'.format(file_png) )
    file_h.write('set style data lines\n')
    file_h.write('set xtics nomirror\n')

    file_h.write('set ytics nomirror\n')
    file_h.write('set grid\n')
    file_h.write('set border 3\n')
    file_h.write('set key outside right\n')
    file_h.write('set size square\n' )
    file_h.write('set title "{0}" \n'.format(param_db))
    file_h.write('set ylabel "Precision" \n')
    file_h.write('set xlabel "Recall"  \n')
    file_h.write('plot [0:1][0:1] "{0}" w lp t "tR"\n'.format(file_plot) )

    file_h.close()

def get_plot_gnup_list(file_plot_list, file_gnup, file_png, p_title, p_leg_list):

    file_h = open(file_gnup, 'w')

    file_h.write('set terminal png font "Arial, 18" \n')
    file_h.write('set output "{0}" \n'.format(file_png) )
    file_h.write('set style data lines\n')
    file_h.write('set xtics nomirror\n')

    file_h.write('set ytics nomirror\n')
    file_h.write('set grid\n')
    file_h.write('set border 3\n')
    file_h.write('set key outside right\n')
    file_h.write('set size square\n' )
    file_h.write('set title "{0}" \n'.format(p_title))
    file_h.write('set ylabel "Precision" \n')
    file_h.write('set xlabel "Recall"  \n')

    l_i = 0
    for file_plot in file_plot_list:
        if l_i == 0:
            file_h.write('plot [0:1][0:1] "{0}" w lp t "{1}" '.format(file_plot, p_leg_list[l_i]) )
        else:
            file_h.write(', "{0}" w lp t "{1}" '.format(file_plot, p_leg_list[l_i]) )

        l_i += 1

    file_h.write('\n')

    file_h.close()

def compute_performance(p_result_fn, p_title):

    print '###################compute_performance()########################'

    file_rel = os.path.join(p_result_fn+ '.rel')

    file_top = os.path.join(p_result_fn + '.top')

    file_result = os.path.join(p_result_fn + '._res')

    file_plot = os.path.join(p_result_fn + '.plot')

    file_gnup = os.path.join(p_result_fn + '.gnup')

    file_png = os.path.join(p_result_fn + '.plot.png')

    cur_path = os.path.abspath( os.curdir)
    print(os.listdir(cur_path))


    cmd = 'trec_eval -q {0} {1} > {2}'.format(file_rel, file_top, file_result)
    print 'running ', cmd, '\\n\\n'
    os.system(cmd)


    [map_val, r_pr] = get_map_rpc(file_result)
    print map_val, r_pr
    get_plot_data(file_result, file_plot)

    get_plot_gnup(file_plot, file_gnup, file_png,p_title )

    cmd = "gnuplot {0}".format(file_gnup)
    print 'running ', cmd
    os.system(cmd)


    return [{'pr_re': r_pr},  {'map' : map_val}, {'plot':file_plot}]

def read_keyword_list(keyword_file):
    ret_list= []
    file_h = open(keyword_file, 'r')
    lines = file_h.readlines()

    for line in lines:
        if '_begin_' in line or '_end_' in line:
            continue

        ret_list.append(line.rstrip('\t\r\n '))

    file_h.close()

    return  ret_list


def process_params(fields):

    print '####################### process_params() ################################'
    score_dir = fields.get('score_dir', [])
    states = fields.get('states')
    mixtures = fields.get('mixtures')
    jump = fields.get('jump')[0]
    loop = fields.get('loop')
    vec_size = fields.get('vec_size')[0]

    if loop == True:
        loop = 1
    else:
        loop = 0

    #file_list = os.listdir(score_dir)

    home = expanduser("~")
    temp_dir = os.path.join(home, 'Desktop', '_temp_')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    print 'params: ',  states, mixtures, range(states[0], states[1]+ 1)
    report_fn = os.path.join(temp_dir, 'all_report.txt')
    file_h_all = open(report_fn, 'w')
    #print file_list



    for state in range(states[0], states[1] +1):
        leg_list = []
        plot_list = []

        for mixture in range(mixtures[0], mixtures[1] + 1):

            model_name = 'hmmset_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model'.\
                format(state, jump, loop,vec_size, mixture)

            for norm in ['gmm', 'plain']:

                result_fn = model_name + '.' + norm + '.result'
                title = 's{0}_m{1}_{2}'.format(state, mixture, norm)

                #copy files to the temp dir
                file_rel = os.path.join(score_dir, result_fn+ '.rel')
                file_top = os.path.join(score_dir, result_fn + '.top')
                shutil.copy(file_rel, temp_dir)
                shutil.copy(file_top, temp_dir)

                param_fn = os.path.join(temp_dir, result_fn)
                performance_val = compute_performance(param_fn, title)

                file_h_all.write('s:{0},m{1},n:{2}\t '.format(state, mixture, norm))
                file_h_all.write(str(performance_val[0:1])+ '\n')


                plot_file_data = performance_val[2].get('plot', '')
                leg_str = 's:{0},m:{1},{2}'.format(state, mixture, norm)

                plot_list.append(plot_file_data)
                leg_list.append(leg_str)

            #end for
        #end for
        gplot_all_fn = os.path.join(temp_dir, 'all{0}.gnuplot'.format(state))
        png_all_fn = os.path.join(temp_dir, 'all{0}.png'.format(state))
        get_plot_gnup_list(plot_list, gplot_all_fn, png_all_fn, 'state{0}'.format(state), leg_list)
        break

    file_h_all.close()

    cmd = "gnuplot {0}".format(gplot_all_fn)
    print 'running ', cmd
    os.system(cmd)


def extract_keyword_score_rel_file(p_file_rel,p_keyword,  p_working_dir, p_out_fn ):

    file_h = open(p_file_rel, 'r')
    lines = file_h.readlines()
    file_h.close()

    out_rel_fn = os.path.join(p_working_dir, p_out_fn)
    file_out_h = open(out_rel_fn, 'w')
    for line_item in lines:
        split_list = line_item.split()
        hmm_obs_lis = split_list[2].split('_')
        if p_keyword in hmm_obs_lis[0]:
            file_out_h.write(line_item)

    file_out_h.close()

    #print(out_rel_fn)

def extract_keyword_score_top_file(p_file_top, p_keyword,  p_working_dir , p_out_fn):

    file_h = open(p_file_top, 'r')
    lines = file_h.readlines()
    file_h.close()

    out_top_fn = os.path.join(p_working_dir, p_out_fn)
    file_out_h = open(out_top_fn, 'w')
    for line_item in lines:
        split_list = line_item.split()
        hmm_obs_lis = split_list[2].split('_')
        if p_keyword in hmm_obs_lis[0]:
            file_out_h.write(line_item)

    file_out_h.close()


def extract_score_rel_file(p_file_rel,  p_working_dir, p_out_fn ):

    file_h = open(p_file_rel, 'r')
    lines = file_h.readlines()
    file_h.close()

    out_rel_fn = os.path.join(p_working_dir, p_out_fn)
    file_out_h = open(out_rel_fn, 'w')
    for line_item in lines:
        file_out_h.write(line_item)

    file_out_h.close()

    #print(out_rel_fn)

def extract_score_top_file(p_file_top,  p_working_dir , p_out_fn):

    file_h = open(p_file_top, 'r')
    lines = file_h.readlines()
    file_h.close()

    out_top_fn = os.path.join(p_working_dir, p_out_fn)
    file_out_h = open(out_top_fn, 'w')
    for line_item in lines:
        file_out_h.write(line_item)

    file_out_h.close()




def process_params_per_key(fields, p_keyword_list, p_workin_dir):
    print '####################### process_params_per_key() ################################'

    score_dir = fields.get('score_dir', [])
    states = fields.get('states')
    mixtures = fields.get('mixtures')
    jump = fields.get('jump')[0]
    loop = fields.get('loop')
    vec_size = fields.get('vec_size')[0]

    if loop:
        loop = 1
    else:
        loop = 0

    # report_fn = os.path.join(temp_dir, 'all_report.txt')
    # file_h_all = open(report_fn, 'w')

    for keyword_item in p_keyword_list:

        print 'processing keyword', keyword_item
        keyword_dir = os.path.join(p_workin_dir, keyword_item)
        if not os.path.exists(keyword_dir):
            os.mkdir(keyword_dir)

        report_file_al = os.path.join(keyword_dir, 'all_report.txt')
        file_h_all = open(report_file_al, 'w')
        for norm in ['gmm', 'plain']:
            norm_dir = os.path.join(keyword_dir, norm)
            if not os.path.exists(norm_dir):
                os.mkdir(norm_dir)

            plot_list = []
            leg_list = []

            for state in range(states[0], states[1] +1):
                for mixture in range(mixtures[0], mixtures[1] + 1):

                    model_name = 'hmmset_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model'.\
                    format(state, jump, loop,vec_size, mixture)

                    result_fn = model_name + '.' + norm + '.result'

                    #copy files to the temp dir
                    file_rel = os.path.join(score_dir, result_fn+ '.rel')
                    file_top = os.path.join(score_dir, result_fn + '.top')

                    extract_keyword_score_rel_file(file_rel, keyword_item,  norm_dir, result_fn + '.rel')
                    extract_keyword_score_top_file(file_top, keyword_item,  norm_dir, result_fn + '.top')

                    param_fn = os.path.join(norm_dir, result_fn)


                    title = 's{0}_m{1}_{2}'.format(state, mixture, norm)
                    performance_val = compute_performance(param_fn, title)

                    file_h_all.write('s:{0},m{1},n:{2}\t '.format(state, mixture, norm))
                    file_h_all.write(str(performance_val[0:2])+ '\n')


                    plot_file_data = performance_val[2].get('plot', '')
                    leg_str = 's:{0},m:{1},{2}'.format(state, mixture, norm)

                    plot_list.append(plot_file_data)
                    leg_list.append(leg_str)
            #end state
            gplot_all_fn = os.path.join(keyword_dir, 'key{0}_{1}.gnuplot'.format(keyword_item,norm))
            png_all_fn = os.path.join(keyword_dir, 'key{0}_{1}.png'.format(keyword_item, norm))
            get_plot_gnup_list(plot_list, gplot_all_fn, png_all_fn, 'state{0}'.format(state), leg_list)

            cmd = "gnuplot {0}".format(gplot_all_fn)
            print 'running ', cmd
            os.system(cmd)


        file_h_all.close()


    return

def process_params_general(fields, p_workin_dir):
    print '####################### process_params_per_key() ################################'

    score_dir = fields.get('score_dir', [])
    states = fields.get('states')
    mixtures = fields.get('mixtures')
    jump = fields.get('jump')[0]
    loop = fields.get('loop')
    vec_size = fields.get('vec_size')[0]

    if loop:
        loop = 1
    else:
        loop = 0


    all_keyword_dir = os.path.join(p_workin_dir, '_all_keywords_')
    if not os.path.exists(all_keyword_dir):
        os.mkdir(all_keyword_dir)

    report_file_al = os.path.join(all_keyword_dir, 'all_report.txt')
    file_h_all = open(report_file_al, 'w')
    for norm in ['gmm', 'plain']:
        norm_dir = os.path.join(all_keyword_dir, norm)
        if not os.path.exists(norm_dir):
            os.mkdir(norm_dir)

        plot_list = []
        leg_list = []

        for state in range(states[0], states[1] +1):
            for mixture in range(mixtures[0], mixtures[1] + 1):

                model_name = 'hmmset_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model'.\
                format(state, jump, loop,vec_size, mixture)

                result_fn = model_name + '.' + norm + '.result'

                #copy files to the temp dir
                file_rel = os.path.join(score_dir, result_fn+ '.rel')
                file_top = os.path.join(score_dir, result_fn + '.top')

                extract_score_rel_file(file_rel,   norm_dir, result_fn + '.rel')
                extract_score_top_file(file_top,   norm_dir, result_fn + '.top')

                param_fn = os.path.join(norm_dir, result_fn)


                title = 's{0}_m{1}_{2}'.format(state, mixture, norm)
                performance_val = compute_performance(param_fn, title)

                file_h_all.write('s:{0},m{1},n:{2}\t '.format(state, mixture, norm))
                file_h_all.write(str(performance_val[0:2])+ '\n')


                plot_file_data = performance_val[2].get('plot', '')
                leg_str = 's:{0},m:{1},{2}'.format(state, mixture, norm)

                plot_list.append(plot_file_data)
                leg_list.append(leg_str)
        #end state
        gplot_all_fn = os.path.join(all_keyword_dir, 'key{0}_{1}.gnuplot'.format('all',norm))
        png_all_fn = os.path.join(all_keyword_dir, 'key{0}_{1}.png'.format('all', norm))
        get_plot_gnup_list(plot_list, gplot_all_fn, png_all_fn, 'state{0}'.format(state), leg_list)

        cmd = "gnuplot {0}".format(gplot_all_fn)
        print 'running ', cmd
        os.system(cmd)


    file_h_all.close()


    return


def process_config_file(p_fn):
    if not os.path.isfile(p_fn):
        return  [];
    file_h = open(p_fn , 'r')
    lines = file_h.readlines()
    states  = []
    mixture = []
    jump = 0
    loop = False
    vect_size = 0
    for line in lines:

        if 'states' in line:
            from_to_ =   line[ line.find('=') + 1:].rstrip('\n').lstrip('\n').split(':')
            states = [ int(s_item) for s_item in from_to_]
            #print states

        if 'gaussian_mixtures' in line:
            from_to_ =   line[ line.find('=') + 1:].rstrip('\n').lstrip('\n').split(':')
            mixture = [ int(s_item) for s_item in from_to_]
            #print mixture


        if 'jump' in line:
            #print line
            from_to_ =   line[ line.find('=') + 1:].rstrip('\n').lstrip('\n').split(':')
            jump   = [ int(s_item) for s_item in from_to_]
            #print jump

        if 'loop' in line:
            #print line
            is_loop =   line[ line.find('=') + 1:].rstrip('\n').lstrip('\n')
            if 'true' in is_loop:
                loop = True
            else:
                loop = False

            #print loop

        if 'vect_size' in line:
            #print line
            from_to_ =   line[ line.find('=') + 1:].rstrip('\n').lstrip('\n').split(':')
            vect_size   = [ int(s_item) for s_item in from_to_]
            #print vect_size

        if 'score_dir' in line:
            score_dir = line[ line.find('=') + 1:].rstrip('\r\n').lstrip(' ')
        if 'keyword_file' in line:
            keyword_file = line[ line.find('=') + 1:].rstrip('\r\n').lstrip(' ')

    score_dir = score_dir.replace('/', os.sep)
    score_dir = score_dir.replace('\\', os.sep)

    keyword_file = keyword_file.replace('/', os.sep)
    keyword_file = keyword_file.replace('\\', os.sep)

    #print score_dir


    dict_config = {'states':states, 'mixtures':mixture, 'jump': jump, 'loop':loop, 'vec_size' : vect_size\
        , 'score_dir': score_dir, 'keyword_file': keyword_file}

    return  dict_config


if __name__ == '__main__':

    argv = sys.argv[1:]

    print os.path.abspath(os.curdir)

    if len(argv) > 0 :
        rec_config_name = argv[0]
        user_out_dir = argv[1]
    else:
        print 'argv is empty'
        exit()

    fields = process_config_file(rec_config_name)


    keyword_file = fields.get('keyword_file', '')

    keyword_list = read_keyword_list(keyword_file)


    #process_params(fields)
    home = expanduser("~")
    temp_dir = os.path.join(home, 'Desktop', '_temp_'+ user_out_dir)
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    process_params_general(fields, temp_dir)

    process_params_per_key(fields, keyword_list, temp_dir)