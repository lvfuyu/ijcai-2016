# @brief: generate positive samples

import sys
import cPickle as pk

def load_loc_merchants(filename):
    loc_merchants = {}
    with open(filename) as f:
        for line in f:
            loc, cnt, merchants = line.rstrip().split('\t', 2)
            m_list = merchants.split(',')
            loc_merchants[loc] = m_list
    return loc_merchants

def main():
    koubei_data = sys.argv[1]
    loc_merchants_file = sys.argv[2]
    pos_neg_files = sys.argv[3]
    loc_merchants = load_loc_merchants(loc_merchants_file)

    user_loc_merchants = {}
    with open(koubei_data) as f:
        for line in f:
            user, merchant, loc, ts = line.rstrip().split(',')
            user_loc_merchants.setdefault(user, {})
            if ts[4:6] == '11':
                user_loc_merchants[user].setdefault(loc, {'pos': set(), 'neg': set()})
                user_loc_merchants[user][loc]['pos'].add(merchant)
    # gen negative pairs
    for user, loc_merchants_real in user_loc_merchants.items():
        for loc, merchants_real in loc_merchants_real.items():
            for mer in loc_merchants[loc]:
                # add negative samples
                if mer not in merchants_real['pos']:
                    user_loc_merchants[user][loc]['neg'].add(mer)

    pk.dump(user_loc_merchants, open(pos_neg_files, 'w'))

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
