############################################################################
#
# Copyright (c) 2016 ICT MCG Group, Inc. All Rights Reserved
#
###########################################################################
"""
Brief:
    get merchant list of every location, sorted by merchant count
Authors: zhouxing(@ict.ac.cn)
Date:    2016/04/23 22:31:49
File:    get_location_merchant.py
"""
import sys
def main():
    m_loc_file = sys.argv[1] #input merchant_info file
    loc_m_file = sys.argv[2] #output location merchant file
    loc_m_dic = {}
    with open(m_loc_file) as f:
        for line in f:
            merchat, budget, locs = line.rstrip().split(',')
            loc_list = locs.split(':')
            for loc in loc_list:
                loc_m_dic.setdefault(loc, [])
                loc_m_dic[loc].append(merchat)
    # sort by size
    s_list = sorted(loc_m_dic.items(), key=lambda d:len(d[1]), reverse=True)
    with open(loc_m_file, 'w') as f:
        for loc, mers in s_list:
            f.write(loc + '\t' + str(len(mers)) + '\t' + ','.join(mers) + '\n')

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
