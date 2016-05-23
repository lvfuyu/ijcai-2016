import sys

def main():
    uml_feature_file = sys.argv[1]
    fm_pred_file = sys.argv[2]
    submit_file = sys.argv[3]
    f_pred = open(fm_pred_file)
    f_submit = open(submit_file, 'w')
    user_loc_merchants = {}
    with open(uml_feature_file) as f:
        for line in f:
            uml, label,fea = line.rstrip().split('\t')
            user, merchant, location = uml.split(',')
            pred = float(f_pred.readline().rstrip())
            if pred > 0.5:
                user_loc_merchants.setdefault(user, {})
                user_loc_merchants[user].setdefault(location, [])
                user_loc_merchants[user][location].append(merchant)
    for user, loc_mers in user_loc_merchants.items():
        for loc, mers in loc_mers.items():
            f_submit.write(user + ',' + loc + ',' + ':'.join(mers) + '\n')
    f_submit.close()

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
