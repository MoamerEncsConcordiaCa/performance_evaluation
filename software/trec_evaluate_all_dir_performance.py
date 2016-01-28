__author__ = 'mameri'

import sys, os

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
    train_type = ''
    
    
    for line in lines:
        print line
        
        #type = init_bp
        
        if 'type' in line:
            type_value = line[ line.find('=') + 1:].rstrip('\r\n ').lstrip('\r\n ')
            train_type = type_value
            
            
        if 'states' in line:
            from_to_ =   line[ line.find('=') + 1:].rstrip('\r\n ').lstrip('\r\n ').split(':')
            print from_to_
            for s_item in from_to_:
                if s_item.isdigit():
                    states.append( int(s_item))
                    
            #states = [ int(s_item) for s_item in from_to_]
            #print states

        if 'gaussian_mixtures' in line:
            from_to_ =   line[ line.find('=') + 1:].rstrip('\n\r ').lstrip('\n\r ').split(':')
          
            for s_item in from_to_:
                if( s_item.isdigit()):
                    mixture.append( int(s_item))


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
        , 'score_dir': score_dir, 'keyword_file': keyword_file, 'type': type_value}

    return  dict_config


def get_config_data_list(p_dir_in_path):

    config_list = []
    dir_list = os.listdir(dir_in_path)
    for dir_item in dir_list:
        expr_dir  = os.path.join(p_dir_in_path, dir_item)
        print( expr_dir)
        rc_file = os.path.join(expr_dir, 'rc.txt')
        if os.path.exists(rc_file):
            print(rc_file)
            fields = process_config_file(rc_file)
            print fields
            config_list.append(fields)


    return config_list

def read_keyword_list(keyword_file):
    ret_list= []
    file_h = open(keyword_file, 'r')
    lines = file_h.readlines()

    for line in lines:
        if '_begin_' in line or '_end_' in line:
            continue
        if ':' in line:
            continue
        
        line_split = line.split()
        
        ret_list.append(line_split[0].rstrip('\t\r\n '))

    file_h.close()

    return  ret_list



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
    file_h.write('plot [0:1][0:1] "{0}" w lp t ""\n'.format(file_plot) )

    file_h.close()


def append_keyword_score_to_all(param_in_fn, file_rel_all, file_top_all):

    file_rel = os.path.join(param_in_fn+ '.rel')

    file_top = os.path.join(param_in_fn + '.top')

    with open(file_rel_all, 'a') as outfile, open(file_rel, 'r') as infile:
        for line in infile:
            outfile.write(line)

    with open(file_top_all, 'a') as outfile, open(file_top, 'r') as infile:
        for line in infile:
            outfile.write(line)



    return

def compute_performance(p_result_fn, p_title):

    # print '###################compute_performance()########################'

    file_rel = os.path.join(p_result_fn+ '.rel')

    file_top = os.path.join(p_result_fn + '.top')

    file_result = os.path.join(p_result_fn + '._res')

    file_plot = os.path.join(p_result_fn + '.plot')

    file_gnup = os.path.join(p_result_fn + '.gnup')

    file_png = os.path.join(p_result_fn + '.plot.png')

    cur_path = os.path.abspath( os.curdir)
    # print(os.listdir(cur_path))


    cmd = 'trec_eval -q "{0}" "{1}" > "{2}" '.format(file_rel, file_top, file_result)
    # print 'running ', cmd, '\\n\\n'
    os.system(cmd)


    [map_val, r_pr] = get_map_rpc(file_result)
    # print map_val, r_pr
    # get_plot_data(file_result, file_plot)

    # get_plot_gnup(file_plot, file_gnup, file_png,p_title )

    # cmd = 'gnuplot "{0}" '.format(file_gnup)
    # print 'running ', cmd
    # os.system(cmd)


    return [{'pr_re': r_pr},  {'map' : map_val}, {'plot':file_plot}]

def compute_performance_with_plot(p_result_fn, p_title):

    # print '###################compute_performance()########################'

    file_rel = os.path.join(p_result_fn+ '.rel')

    file_top = os.path.join(p_result_fn + '.top')

    file_result = os.path.join(p_result_fn + '._res')

    file_plot = os.path.join(p_result_fn + '.plot')

    file_gnup = os.path.join(p_result_fn + '.gnup')

    file_png = os.path.join(p_result_fn + '.plot.png')

    cur_path = os.path.abspath( os.curdir)
    # print(os.listdir(cur_path))


    cmd = 'trec_eval -q "{0}" "{1}" > "{2}" '.format(file_rel, file_top, file_result)
    # print 'running ', cmd, '\\n\\n'
    os.system(cmd)


    [map_val, r_pr] = get_map_rpc(file_result)
    # print map_val, r_pr
    get_plot_data(file_result, file_plot)

    get_plot_gnup(file_plot, file_gnup, file_png,p_title )

    cmd = 'gnuplot "{0}" '.format(file_gnup)
    # print 'running ', cmd
    os.system(cmd)


    return [{'pr_re': r_pr},  {'map' : map_val}, {'plot':file_plot}]

def get_state_mixtuer_for_bp(param_keyword_file, param_keyword):
 
    states = []
    mixtures = []
    file_h = open(param_keyword_file, 'r')
    lines = file_h.readlines()
    #adherant	s = 26	m = 7	RPr = 0.6809	MAP = 0.7543
    for line in lines:
        if '_begin_' in line or '_end_' in line:
            continue
        
        line_split = line.split()
        
        keyword_item = line_split[0].rstrip('\t\r\n ')
        if param_keyword == keyword_item:
            states.append(int (line_split[3]))
            states.append(int (line_split[3]))
            
            mixtures.append(int (line_split[6]))
            mixtures.append(int (line_split[6]))
            
            

    file_h.close()

    
    return [states, mixtures]
    
    
def process_params_general(p_config_data, p_dir_in_path):
    print '####################### process_params_general() ################################'

    keyword_list = []
    if len (p_config_data) > 0:
        key_word_file = p_config_data[0].get('keyword_file', '')
        keyword_list = read_keyword_list(os.path.abspath( key_word_file) )
        print keyword_list

    dir_out_path = os.path.join(p_dir_in_path, '_evaluation_')
    if not os.path.exists(dir_out_path):
        os.mkdir(dir_out_path)

    # print dir_out_path
#    print keyword_list
    best_params_keyword = {}
    for keyword_item in keyword_list:

        keyword_dir= os.path.join(dir_out_path, keyword_item)
        if not os.path.exists(keyword_dir):
            os.mkdir(keyword_dir)

        keyword_temp_dir = os.path.join(keyword_dir, '_temp_')
        if not os.path.exists(keyword_temp_dir):
            os.mkdir(keyword_temp_dir)

        report_file_al = os.path.join(keyword_dir, 'all_report.txt')

        if os.path.exists(report_file_al):
            print 'report file exists ', report_file_al
            continue

#        print 'keyword' , keyword_item
#        print 'config data ', p_config_data
        norm = 'gmm'
        performance_list = []
        for config_item in p_config_data:
            fields = config_item
            loop = 0
            score_dir = fields.get('score_dir', [])
            states = fields.get('states')
            mixtures = fields.get('mixtures')
            jump = fields.get('jump')[0]
            loop_item = fields.get('loop')
            vec_size = fields.get('vec_size')[0]
            if loop_item:
                loop = 1
            train_type = fields.get('type')
            

            print(keyword_item,  states, mixtures)
            if not os.path.exists(score_dir):
                print 'score dir does not exists', score_dir
                continue            
            
            print train_type
            if train_type == 'init_bp' or train_type == 'retrain_bp':
                states, mixtures = get_state_mixtuer_for_bp(os.path.abspath( key_word_file), keyword_item)
                
                #hmm-model_sante_states-16_jump-0_loop-1_vecsize-24_mix-13.model.plain.result
                model_name = 'hmm-model_{5}_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model'.\
                format(states[0], jump, loop,vec_size, mixtures[0], keyword_item)

                result_fn = model_name + '.' + norm + '.result'


                    #copy files to the temp dir
                file_rel = os.path.join(score_dir, result_fn + '.rel')
                file_top = os.path.join(score_dir, result_fn + '.top')

                if not os.path.exists( file_rel ):
                    print 'result file does not exists', file_rel
                else:

                    extract_keyword_score_rel_file(file_rel, keyword_item,  keyword_temp_dir, result_fn + '.rel')
                    extract_keyword_score_top_file(file_top, keyword_item,  keyword_temp_dir, result_fn + '.top')

                    param_fn = os.path.join(keyword_temp_dir, result_fn)


                    title = '{3}_'.format(states[0], mixtures[0], norm, keyword_item)
                    performance_val = compute_performance(param_fn, title)

                    [pr_re,  map_val, file_plot] = performance_val                    

                    performance_list.append([pr_re['pr_re'], map_val['map'], states[0], mixtures[0]])

                
            else:
                for state in range(states[0], states[1] +1):
    
                    for mixture in range(mixtures[0], mixtures[1] + 1):
    
                        model_name = 'hmmset_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model'.\
                        format(state, jump, loop,vec_size, mixture)
    
                        result_fn = model_name + '.' + norm + '.result'
    
    
                        #copy files to the temp dir
                        file_rel = os.path.join(score_dir, result_fn + '.rel')
                        file_top = os.path.join(score_dir, result_fn + '.top')
    
                        if not os.path.exists( file_rel ):
                            print 'result file does not exists', file_rel
                            continue
    
                        extract_keyword_score_rel_file(file_rel, keyword_item,  keyword_temp_dir, result_fn + '.rel')
                        extract_keyword_score_top_file(file_top, keyword_item,  keyword_temp_dir, result_fn + '.top')
    
                        param_fn = os.path.join(keyword_temp_dir, result_fn)
    
    
                        title = 's{0}_m{1}_{2}'.format(state, mixture, norm)
                        performance_val = compute_performance(param_fn, title)
    
                        [pr_re,  map_val, file_plot] = performance_val
    
                        # file_h_all.write('s:{0},m{1},n:{2}\t '.format(state, mixture, norm))
                        # file_h_all.write(str(performance_val[0:2])+ '\n')
    
                        performance_list.append([pr_re['pr_re'], map_val['map'], state, mixture])
    
                        #plot_file_data = performance_val[2].get('plot', '')
                        #leg_str = 's:{0},m:{1},{2}'.format(state, mixture, norm)
    
    
    
                #end state


        #end config
        performance_list.sort(key=lambda x: x[1] ,reverse=True)
        if len(performance_list) > 0 :
            best_params_keyword[keyword_item] = [performance_list[0], config_item]

        file_h_all = open(report_file_al, 'w')
        for performance_item in performance_list:
            file_h_all.write(str(performance_item) + ' \n')
        file_h_all.close()



    return best_params_keyword

def get_params_in_performance_line(all_report_fn, col_num):

    sm = []
    with open(all_report_fn, 'r') as best_param_file_h:
            lines = best_param_file_h.readlines()
    if len(lines) == 0:
        return  sm

    lines.sort(key = lambda x:float(x.replace('[', '').replace(']', '').split(',')[col_num]), reverse = True)

    line = lines[0]
    linesplit = line.replace('[', '').replace(']', '').split(',')
    if len(linesplit) == 4:
        state = int (linesplit[2])
        mixture= int (linesplit[3])
        sm  = [state, mixture]
    # print sm
    return  sm

def process_best_params(p_config_data, p_dir_in_path):

    print 'processing best parameters'

    if len(p_config_data) == 0:
        return

    key_word_file = p_config_data[0].get('keyword_file', '')
    keyword_list = read_keyword_list(os.path.abspath( key_word_file) )

    dir_out_path = os.path.join(p_dir_in_path, '_evaluation_')

    all_dir= os.path.join(dir_out_path, '_all_')
    if not os.path.exists(all_dir):
        os.mkdir(all_dir)

    result_fn_all = 'result'

    file_rel_all = os.path.join(all_dir, result_fn_all + '.rel')
    file_top_all = os.path.join(all_dir, result_fn_all + '.top')

    report_all_fnfp = os.path.join(all_dir, '_all_reports.txt')

    if os.path.exists( file_rel_all):
        os.remove(file_rel_all)
    if os.path.exists(file_top_all):
        os.remove(file_top_all)

    file_h_report_all = open(report_all_fnfp, 'w')
    file_h_report_all.write('_begin_\n')

    best_params_keyword = {}
    norm = 'gmm'
    for keyword_item in keyword_list:
        keyword_dir= os.path.join(dir_out_path, keyword_item)
        all_report_fn = os.path.join(keyword_dir, 'all_report.txt')
        sm = get_params_in_performance_line(all_report_fn, 0)
        if sm == []:
            continue


        for config_item in p_config_data:
            fields = config_item
            loop = 0
            score_dir = fields.get('score_dir', [])
            states = fields.get('states')
            mixtures = fields.get('mixtures')
            jump = fields.get('jump')[0]
            loop_item = fields.get('loop')
            vec_size = fields.get('vec_size')[0]
            if loop_item:
                loop = 1
                
            train_type = fields.get('type')

            
            print train_type
            if train_type == 'init_bp' or train_type == 'retrain_bp':
                states, mixtures = get_state_mixtuer_for_bp(os.path.abspath( key_word_file), keyword_item)
                
                 #hmm-model_sante_states-16_jump-0_loop-1_vecsize-24_mix-13.model.plain.result
                result_fn = 'hmm-model_{6}_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model.{5}.result'.\
                format(states[0], jump, loop,vec_size, mixtures[0], norm,  keyword_item)
                
                file_rel = os.path.join(score_dir, result_fn + '.rel')
                file_top = os.path.join(score_dir, result_fn + '.top')

                if not os.path.exists( file_rel ):
                    print 'file rel does not exists', file_rel
                    continue

                extract_keyword_score_rel_file(file_rel, keyword_item,  keyword_dir, result_fn + '.rel')
                extract_keyword_score_top_file(file_top, keyword_item,  keyword_dir, result_fn + '.top')



                param_fn = os.path.join(keyword_dir, result_fn)

                append_keyword_score_to_all(param_fn, file_rel_all, file_top_all)

                title = 's{0}_m{1}_{2}'.format(sm[0], sm[1], keyword_item)
                performance_val = compute_performance_with_plot(param_fn, title)

                [pr_re,  map_val, file_plot] = performance_val

                # print 'keyword:', keyword_item, pr_re, map_val
                # file_h_report_all.write('P:{1},\tR:{2}, \ts:{3}, \tm:{4},\t keyword: {0},\n'.
                #                         format(keyword_item, pr_re['pr_re'], map_val['map'], sm[0],sm[1]))

                file_h_report_all.write('{0}\ts = {3}\tm = {4}\tRPr = {1}\tMAP = {2}\n'.
                                        format(keyword_item, pr_re['pr_re'], map_val['map'], sm[0],sm[1]))
                                        
            
            else:
            # print states, mixtures, type(states)
                if states[0] <= sm[0] <=states[1] \
                        and  mixtures[0] <= sm[1] <= mixtures[1]:
    
                    keyword_dir= os.path.join(dir_out_path, keyword_item)
    
                    result_fn = 'hmmset_states-{0}_jump-{1}_loop-{2}_vecsize-{3}_mix-{4}.model.{5}.result'.\
                    format(sm[0], jump, loop,vec_size, sm[1], norm)
    
                    file_rel = os.path.join(score_dir, result_fn + '.rel')
                    file_top = os.path.join(score_dir, result_fn + '.top')
    
                    if not os.path.exists( file_rel ):
                        print 'file rel does not exists', file_rel
                        continue
    
                    extract_keyword_score_rel_file(file_rel, keyword_item,  keyword_dir, result_fn + '.rel')
                    extract_keyword_score_top_file(file_top, keyword_item,  keyword_dir, result_fn + '.top')
    
    
    
                    param_fn = os.path.join(keyword_dir, result_fn)
    
                    append_keyword_score_to_all(param_fn, file_rel_all, file_top_all)
    
                    title = 's{0}_m{1}_{2}'.format(sm[0], sm[1], keyword_item)
                    performance_val = compute_performance_with_plot(param_fn, title)
    
                    [pr_re,  map_val, file_plot] = performance_val
    
                    # print 'keyword:', keyword_item, pr_re, map_val
                    # file_h_report_all.write('P:{1},\tR:{2}, \ts:{3}, \tm:{4},\t keyword: {0},\n'.
                    #                         format(keyword_item, pr_re['pr_re'], map_val['map'], sm[0],sm[1]))
    
                    file_h_report_all.write('{0}\ts = {3}\tm = {4}\tRPr = {1}\tMAP = {2}\n'.
                                            format(keyword_item, pr_re['pr_re'], map_val['map'], sm[0],sm[1]))
    #end keywords

    file_h_report_all.write('_end_\n')

    result_all_fnfp =  os.path.join(all_dir, result_fn_all)

    performance_val = compute_performance_with_plot(result_all_fnfp, 'all_keywords')

    [pr_re,  map_val, file_plot] = performance_val

    file_h_report_all.write('all:\tRPr:{0},\tMAP:{1}\n'.format( pr_re['pr_re'], map_val['map']))


    return

if __name__ == '__main__':


    print 'in dir:', os.path.abspath(os.curdir)
    print sys.argv

    if len(sys.argv) >  1 :
        argv = sys.argv[1:]
        dir_in_path = argv[0]
        dir_in_path =  os.path.abspath( dir_in_path)

    else:
        print 'argv is empty'
        exit()


    config_data = get_config_data_list(dir_in_path)

    print 'config data items'
    for config_item in config_data:
        print config_item
    
    
    best_params = process_params_general(config_data, dir_in_path)

    
    print( best_params)


    process_best_params(config_data, dir_in_path)


    # fields = process_config_file(rec_config_name)
    #
    #
    # keyword_file = fields.get('keyword_file', '')
    #
    # keyword_list = read_keyword_list(keyword_file)
    #
    #
    # #process_params(fields)
    # home = expanduser("~")
    # temp_dir = os.path.join(home, 'Desktop', '_temp_'+ user_out_dir)
    # if not os.path.exists(temp_dir):
    #     os.mkdir(temp_dir)
    #
    # process_params_general(fields, temp_dir)
    #
    # process_params_per_key(fields, keyword_list, temp_dir)
