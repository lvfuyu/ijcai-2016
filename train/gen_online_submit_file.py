import sys

def main():
    uml_file = sys.argv[1]
    pred_file = sys.argv[2]
    submit_file = sys.argv[3]
    theta = float(sys.argv[4])
    f_pred = open(pred_file)
    f_sub = open(submit_file, 'w')
    user_location_merchants = {}
    with open(uml_file) as f:
        for line in f:
            ulm, _ = line.rstrip().split('\t', 1)
            user, location, merchant = ulm.split(',')
            pred = float(f_pred.readline().rstrip())
            user_location_merchants.setdefault(user, {})
            user_location_merchants[user].setdefault(location, set())
            user_location_merchants[user][location].add((merchant, pred))
    for user, loc_merchants in user_location_merchants.items():
        for loc, merchants in loc_merchants.items():
            merchants = sorted(merchants, key=lambda merchants : merchants[1], reverse=True)
            top_1_merchant = merchants[0][0]
            added_merchants = []
            for rec_pair in merchants:
                if rec_pair[1] > theta:
                    added_merchants.append(rec_pair[0])
            if not added_merchants:
                added_merchants.append(top_1_merchant)
            f_sub.write(user + ',' + loc + ',' + ':'.join(list(added_merchants)[:10]) + '\n')
    f_sub.close()


if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
