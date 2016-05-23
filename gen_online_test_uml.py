# @ generate online test user merchant location candidates

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
    test_umls_file = sys.argv[3]
    loc_merchants = load_loc_merchants(loc_merchants_file)
    user_loc_merchants = {}
    with open(koubei_data) as f:
        for line in f:
            user, location = line.rstrip().split(',')
            user_loc_merchants[user] = {}
            user_loc_merchants[user][location] = {'pos': set(), 'neg': set()}
            user_loc_merchants[user][location]['neg'] = set(loc_merchants[location])
    pk.dump(user_loc_merchants, open(test_umls_file, 'w'))

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
