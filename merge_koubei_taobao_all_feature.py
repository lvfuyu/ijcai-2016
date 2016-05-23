import sys
import cPickle as pk

def load_id_feature(filename):
    id_index_fea = {}
    with open(filename) as f:
        for line in f:
            name, nid_fea = line.rstrip().split('\t')
            nid, fea = nid_fea.split(' ', 1)
            id_index_fea[name] = {'index':0, 'fea':''}
            id_index_fea[name]['index'] = int(nid)
            id_index_fea[name]['fea'] = fea
    return id_index_fea

def load_name_feature(name_feature_file):
    name_feature = {}
    with open(name_feature_file) as f:
        for line in f:
            name, feature = line.rstrip().split('\t')
            name_feature[name] = feature
    fea_cnt = 0
    for name, fea in name_feature.items():
        fea_cnt = len(fea.split())
        break
    return name_feature, fea_cnt
def load_merchant_cate_feature(merchant_cate_fea_file):
    merchant_cat_fea = pk.load(open(merchant_cate_fea_file))
    m_fea = {}
    for merchant, feature in merchant_cat_fea.items():
        fea = ' '.join([str(val) for val in feature['cat_list']])
        m_fea[merchant] = fea.split()
    return m_fea

def check_merchant_cate_fea(merchant, merchant_cate_fea):
    zero_list = ['0']*72
    if merchant not in merchant_cate_fea:
        return zero_list
    else:
        return merchant_cate_fea[merchant]

def gen_cate_fea(cate_dic, beg_index):
    sorted_cate = sorted(cate_dic.iteritems(), key=lambda d:d[0])
    return ' '.join([str(int(key)+beg_index)+':'+ str(float(val)) for key, val in sorted_cate])

def get_tao_user_fea(user, user_taobao_fea, beg):
    if user not in user_taobao_fea:
        return ''
    else:
        buy_cate_fea = gen_cate_fea(user_taobao_fea[user]['buy']['cate'], beg)
        return buy_cate_fea

def get_merchant_fea(merchant, merchant_interest, beg):
    if merchant not in merchant_interest:
        return ''
    else:
        fea = gen_cate_fea(merchant_interest[merchant]['buy_cate'], beg)
        return fea
def load_embedding(filename):
    index_embed = {}
    f = open(filename)
    line = f.readline()
    cnt, size = line.rstrip().split()
    while 1:
        line = f.readline()
        if not line:
            break
        index, fea = line.rstrip().split(' ', 1)
        index_embed[index] = fea
    return index_embed

def load_name_index(filename):
    name2index = {}
    with open(filename) as f:
        for line in f:
            name, index = line.rstrip().split('\t')
            name2index[name] = index
    return name2index

def main():
    ulm_file = sys.argv[1]
    merge_feature = sys.argv[2]
    taobao_fea_file = sys.argv[3]
    merchant_fea_file = sys.argv[4]
    location_fea_file = sys.argv[5]
    merchant_ratio_fea_file = sys.argv[6]
    loc_merchant_ratio_fea_file = sys.argv[7]

    #user_taobao_fea = pk.load(open(taobao_fea_file))
    merchant_interest = pk.load(open(sys.argv[8]))
    loc_merchant_id = pk.load(open(sys.argv[9]))
    #name2index = load_name_index(sys.argv[10])
    #index_embed = load_embedding(sys.argv[11])

    f_merge = open(merge_feature, 'w')
    location_feature = load_id_feature(location_fea_file)
    merchant_feature = load_id_feature(merchant_fea_file)

    merchant_ratio_feature, mr_cnt = load_name_feature(merchant_ratio_fea_file)
    loc_merchant_ratio_feature, lmr_cnt = load_name_feature(loc_merchant_ratio_fea_file)

    loc_len = len(location_feature)
    merchant_len = len(merchant_feature)
    loc_mid_len = len(loc_merchant_id)

    print 'merchant_len',merchant_len
    print 'loc_len',loc_len
    print 'loc, mid', loc_mid_len

    #print 'taobao user cnt ', len(user_taobao_fea)
    taobao_seller_len = 10000
    taobao_cate_len = 72
    with open(ulm_file) as f:
        for line in f:
            ulm, label, his_fea = line.rstrip().split('\t')
            user, location, merchant = ulm.split(',')
            _ , loc_merchant = ulm.split(',', 1)
            fea_list = []
            fea_list += his_fea.split()
            if merchant in merchant_ratio_feature:
                fea_list += merchant_ratio_feature[merchant].split()
            else:
                fea_list += ['0']*mr_cnt
            if loc_merchant in loc_merchant_ratio_feature:
                fea_list += loc_merchant_ratio_feature[loc_merchant].split()
            else:
                fea_list += ['0']*lmr_cnt

            '''
            if loc_merchant in name2index:
                fea_list += index_embed[name2index[loc_merchant]].split()
            else:
                fea_list += ['0']*20
            if user in name2index:
                fea_list += index_embed[name2index[user]].split()
            else:
                fea_list += ['0']*20
            '''

            # add merchant feature
            #fea_list += merchant_feature[merchant]['fea'].split()
            # add online merchant interests
            # gen taobao user feature
            #if user in user_taobao_fea:
            #    fea_list += user_taobao_fea[user]['click']['cate']
                #fea_list += user_taobao_fea[user]['buy']['cate']
            #else:
            #    fea_list += ['0']*72
                #fea_list += ['0']*72

            #fea_list += merchant_interest[merchant]['click_cate']
            # add id feature
            mid_findex = merchant_feature[merchant]['index']
            lid_findex = location_feature[location]['index']+merchant_len

            lm_id_fea = str(mid_findex) + ':1' + ' ' + str(lid_findex) + ':1'
            if loc_merchant in loc_merchant_id:
                loc_mid = loc_merchant_id[loc_merchant] + merchant_len + loc_len
                lm_id_fea += ' ' + str(loc_mid) + ':1'
                #lm_id_fea = str(loc_mid) + ':1 ' + lm_id_fea
            id_fea_len = merchant_len + loc_len + loc_mid_len
            # index start from 1
            basic_feature_len = len(fea_list)
            basic_feature_list = []
            for i in range(basic_feature_len):
                if float(fea_list[i]) != 0.0:
                    basic_feature_list.append(str(i+1+id_fea_len)+':'+str(fea_list[i]))
            basic_feature = ' '.join(basic_feature_list)

            #'''
            #user_intr_fea = get_tao_user_fea(user, user_taobao_fea, basic_feature_len)
            #user_intr_len = 72
            #merchant_intr_fea = get_merchant_fea(merchant, merchant_interest, basic_feature_len+user_intr_len)
            #intr_fea = user_intr_fea + ' ' + merchant_intr_fea
            #intr_fea = intr_fea.strip()
            #'''
            merge_fea = lm_id_fea + ' ' + basic_feature #+ ' ' + intr_fea
            merge_fea = merge_fea.strip()
            # other feature
            # taobao feature
            #start_index = basic_feature_len + merchant_len + loc_len
            #id_list = []
            '''
            if user in user_taobao_fea:
                for seller in user_taobao_fea[user]['buy']['seller']:
                    id_list.append(start_index+int(seller))
                taobao_seller_len = 0
                for cate in user_taobao_fea[user]['buy']['cate']:
                    id_list.append(start_index+taobao_seller_len+int(cate))
            id_list.sort()
            taobao_id_fea = ' '.join([str(val)+':1' for val in id_list])
            '''
            #f_merge.write(label + ' ' + ' '.join(['%d:%s'%(i+1, fea_list[i]) for i in range(len(fea_list))]) + ' ' + lm_id_fea  + '\n')
            #f_merge.write(label + ' ' + basic_feature + ' ' + lm_id_fea + '\n')
            f_merge.write(label + ' ' + merge_fea + '\n')
    f_merge.close()



if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
