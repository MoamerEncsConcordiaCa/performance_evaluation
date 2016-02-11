import os
import sys

__author__ = 'mameri'


def label_prf_by_score_files(p_file_orig, p_file_label, p_file_report,
                             p_diff_prf):
    with open(p_file_orig, 'r') as f_o:
        lines_original = f_o.readlines()

    with open(p_file_label, 'r') as f_l:
        lines_labeled = f_l.readlines()

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    positive_count =0
    negative_count =0
    for i, line in enumerate(lines_original):
        if 'PROF' in line:
            is_diff = False
            original_prof = lines_original[i].split()[1].split(':')[1]
            labeled_prof = lines_labeled[i].split()[1].split(':')[1]
            h = int(lines_original[i].split()[5])

            if original_prof == 'non-keyword':
                negative_count += 1
            else:
                positive_count += 1

            if original_prof == 'non-keyword' or labeled_prof == 'non-keyword':
                if original_prof == labeled_prof:
                    tn += 1
                elif original_prof == 'non-keyword':
                    fp += 1
                    is_diff = True
                elif labeled_prof == 'non-keyword':
                    fn += 1
                    is_diff = True
            else:
                (label_prof, label_score) = labeled_prof.split('_')
                if label_prof[:4] == original_prof[:4]:
                    tp += 1
                else:
                    # print label_prof,' ', original_prof
                    is_diff = True
                    fn += 1

            if is_diff:
                with open(p_diff_prf, 'a') as f_diff:
                    print h
                    new_prof = '{}=>{}'.format(original_prof, labeled_prof)
                    header = line.replace(original_prof, new_prof)
                    f_diff.write(header)
                    f_diff.writelines(lines_original[i+1:i+1+h])

    with open(p_file_report, 'w') as f_report:

        acc = float((tp+tn)) / (tp + fp + tn + fn)
        f_report.write('tp:{0} fp:{1} tn:{2} fn:{3}\n'.format(tp, fp, tn, fn))
        f_report.write('acc:{0}\n'.format(acc))
        f_report.write('keywords:{0}\n'.format(tp+fn, positive_count))
        f_report.write('non-keywords:{0}\n'.format(tn+fp, negative_count))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv = sys.argv[1:]

        file_orig = argv[0]
        file_label = argv[1]
        file_report = argv[2]
        file_diff_prf = argv[3]

        label_prf_by_score_files(file_orig, file_label, file_report, file_diff_prf)

    else:
        print 'call original-_prf labeled_prf report_file diff_prf '


