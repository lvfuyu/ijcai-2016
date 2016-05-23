import sys
import cPickle as pk

def write_id_feature(index_dic, filename):
    with open(filename, 'w') as f:
        for id, index in index_dic.items():
            f.write(id + '\t' + str(index)+'\n')

def load_all_user(filename):
    all_user = set()
    with open(filename) as f:
        for line in f:
            all_user.add(line.rstrip())
    return all_user

def main():
    taobao_train = sys.argv[1]
    taobao_feature_file = sys.argv[2]
    seller_file = sys.argv[3]
    cate_file = sys.argv[4]
    all_user = load_all_user(sys.argv[5])
    mode = sys.argv[6]
    t_user_feature = {}
    seller_index = {}
    s_index, c_index = 1, 1
    cate_index = {}
    with open(taobao_train) as f:
        for line in f:
            user, seller, item, cate, action, ts = line.rstrip().split(',')
            if seller not in seller_index:
                seller_index[seller] = s_index
                s_index += 1
            if cate not in cate_index:
                cate_index[cate] = c_index
                c_index += 1
    print 'cate_cnt', len(cate_index)
    print 'seller_cnt', len(seller_index)
    if mode == 'local':
        write_id_feature(seller_index, seller_file)
        write_id_feature(cate_index, cate_file)

    with open(taobao_train) as f:
        for line in f:
            user, seller, item, cate, action, ts = line.rstrip().split(',')
            if user not in all_user:
                continue
            if mode == 'local':
                if ts[4:6] == '11':
                    continue
            t_user_feature.setdefault(user, {'click':{'seller':set(), 'cate':set()},
                'buy':{'seller':set(), 'cate':set()}})
            if action == '0':
                t_user_feature[user]['click']['seller'].add(seller_index[seller])
                t_user_feature[user]['click']['cate'].add(cate_index[cate])
            elif action == '1':
                t_user_feature[user]['buy']['seller'].add(seller_index[seller])
                t_user_feature[user]['buy']['cate'].add(cate_index[cate])

    pk.dump(t_user_feature, open(taobao_feature_file, 'w'))

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
