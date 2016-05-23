import sys

def load_merchant_budget(filename):
    merchant_budget = {}
    with open(filename) as f:
        for line in f:
            mid, budget, locs = line.rstrip().split(',')
            merchant_budget[mid] = int(budget)
    return merchant_budget

def main():
    uml_file = sys.argv[1]
    pred_file = sys.argv[2]
    submit_file = sys.argv[3]
    theta = float(sys.argv[4])
    merchant_budget = load_merchant_budget(sys.argv[5])
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
    merchant_recs = {}
    for user, loc_merchants in user_location_merchants.items():
        for loc, merchants in loc_merchants.items():
            merchants = sorted(merchants, key=lambda merchants : merchants[1], reverse=True)
            top_1_merchant = merchants[0]
            added_merchants = []
            for rec_pair in merchants:
                if rec_pair[1] > theta:
                    added_merchants.append(rec_pair)
            if not added_merchants:
                added_merchants.append(top_1_merchant)
            for mid_info in added_merchants[:10]:
                merchant_recs.setdefault(mid_info[0], [])
                merchant_recs[mid_info[0]].append((user+','+loc+','+mid_info[0], mid_info[1]))
    print 'cal merchant list..end'
    # sort merchant by probability
    user_loc_mids = {}
    for mid, recs in merchant_recs.items():
        sorted_recs = sorted(recs, key=lambda recs : recs[1], reverse=True)
        top_cnt = int(2.05*merchant_budget[mid])
        top_recs = sorted_recs[:top_cnt]
        for ulm, prob in top_recs:
            user, loc, mid = ulm.split(',')
            user_loc_mids.setdefault(user, {})
            user_loc_mids[user].setdefault(loc, [])
            user_loc_mids[user][loc].append(mid)
    for user, locs in user_loc_mids.items():
        for loc, ms in locs.items():
            f_sub.write(user + ',' + loc + ',' + ':'.join(ms) + '\n')
    f_sub.close()


if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
