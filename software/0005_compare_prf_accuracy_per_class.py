import os
import sys

__author__ = 'mameri'


def label_prf_by_score_files(p_file_orig, p_file_label, p_file_report ):

    with open(p_file_orig, 'r') as f_o:
        lines_original = f_o.readlines()

    with open(p_file_label, 'r') as f_l:
        lines_labeled = f_l.readlines()

    perclass_dict = {}

    for i, line in enumerate(lines_original):
        if 'PROF' in line:

            original_prof = lines_original[i].split()[1].split(':')[1]
            labeled_prof = lines_labeled[i].split()[1].split(':')[1]
            h = int(lines_original[i].split()[5])

            if original_prof != 'non-keyword':
                prof_stat = perclass_dict.get(original_prof, {'tp': 0, 'fn': 0, 'fclass': {}})

                if labeled_prof != 'non-keyword':
                    (label_prof, label_score) = labeled_prof.split('_')
                else:
                    label_prof = 'non-keyword'

                if label_prof[:4] == original_prof[:4]:
                    prof_stat['tp'] += 1
                else:
                    if label_prof != 'non-keyword':
                        print label_prof

                    prof_stat['fn'] +=1
                    fclass_missed = prof_stat['fclass'].get(label_prof, 0) + 1
                    prof_stat['fclass'][label_prof] = fclass_missed

                perclass_dict[original_prof] = prof_stat

    tp_all = 0
    fn_all = 0
    with open(p_file_report, 'w') as f_report:
        for key, value in perclass_dict.items():
            f_report.write('{0}-> '.format(key))
            f_report.write('\ttp:{0}, fn:{1}\n'.format(value['tp'], value['fn']))
            tp_all += value['tp']
            fn_all += value['fn']

            for fclass_key, fclass_num in value['fclass'].items():
                f_report.write('\t{0}:{1}\n'.format(fclass_key, fclass_num))
        f_report.write('tp_all:{0}, fn_all{1}, acc:{2}\n'.format(tp_all, fn_all, float(tp_all)/(fn_all + tp_all)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv = sys.argv[1:]

        file_orig = argv[0]
        file_label = argv[1]
        file_report = argv[2]


        label_prf_by_score_files(file_orig, file_label, file_report)

    else:
        print 'call original-_prf labeled_prf report_file '


