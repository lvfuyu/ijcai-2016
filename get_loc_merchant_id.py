import sys
import cPickle as pk
def main():
    koubei_file = sys.argv[1]
    lmid_file = sys.argv[2]
    lmid_dic = {}
    index = 1
    with open(koubei_file) as f:
        for line in f:
            ulm, _ = line.rstrip().split('\t', 1)
            user, loc_mid = ulm.split(',', 1)
            if loc_mid not in lmid_dic:
                lmid_dic[loc_mid] = index
                index += 1
    pk.dump(lmid_dic, open(lmid_file, 'w'))

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
