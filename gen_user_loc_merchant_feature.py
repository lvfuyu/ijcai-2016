import sys
import cPickle as pk
from gen_postive_uml import load_loc_merchants
import random
import numpy as np
TIME_RANGE=[1,3, 7, 30, 60, 200]
#TIME_RANGE=[1,3,5,7,15,21,30,60,200]
TIME_LEN = len(TIME_RANGE)
def cal_day_feature(day_list, a):
    for cur_index in day_list:
        for i in range(TIME_LEN):
            if cur_index <= TIME_RANGE[i]:
                a[i] += 1
    return a

def check_history(user, loc, merchant, user_ulm_history, user_loc_actions, user_merchants_actions,
        user_fea_dic):
    fea_num = 12 + TIME_LEN
    fea_list = [0]*fea_num
    zero_fea = ' '.join([str(val) for val in fea_list])
    ulm_action = 0
    ulm_day = 0
    ulm_action_ratio = 0
    ulm_day_ratio = 0
    ulm_his = [0]*TIME_LEN

    cur_loc_actions = 0
    cur_loc_actions_ratio = 0
    cur_loc_days = 0
    cur_loc_days_ratio = 0

    cur_merchant_actions = 0
    cur_merchant_day = 0
    cur_merchant_actions_ratio = 0
    cur_merchant_day_ratio = 0

    if user not in user_ulm_history:
        return zero_fea
    if loc in user_ulm_history[user]:
        cur_loc_actions = user_loc_actions[loc]['cnt']
        cur_loc_actions_ratio = 1.0*cur_loc_actions/user_fea_dic['user_actions_cnt']
        cur_loc_days = len(set(user_loc_actions[loc]['day']))
        cur_loc_days_ratio = 1.0*cur_loc_days/user_fea_dic['user_actions_day']
        if merchant in user_ulm_history[user][loc]:
            ulm_action = user_ulm_history[user][loc][merchant]['cnt']
            ulm_action_ratio = 1.0*ulm_action/cur_loc_actions
            ulm_day_ratio = 1.0*ulm_day/cur_loc_days
            ulm_his = cal_day_feature(user_ulm_history[user][loc][merchant]['ts'], np.zeros(TIME_LEN))
            ulm_day = len(set(user_ulm_history[user][loc][merchant]['ts']))
            ulm_his /= user_loc_actions[loc]['his']

    if merchant in user_merchants_actions:
        cur_merchant_actions = user_merchants_actions[merchant]['cnt']
        cur_merchant_actions_ratio = 1.0*cur_merchant_actions/user_fea_dic['user_actions_cnt']
        cur_merchant_day = len(set(user_merchants_actions[merchant]['day']))
        cur_merchant_day_ratio = 1.0*cur_merchant_day/user_fea_dic['user_actions_day']
    fea_list = [ulm_action, ulm_day, ulm_action_ratio, ulm_day_ratio, cur_merchant_actions,
            cur_merchant_day, cur_merchant_actions_ratio, cur_merchant_day_ratio, cur_loc_actions,
            cur_loc_actions_ratio, cur_loc_days, cur_loc_days_ratio] + list(ulm_his)
    return ' '.join([str(val) for val in fea_list])

def check_user_feature(user, user_ulm_history):
    user_loc_actions = {}
    user_merchants_actions = {}

    fea_dic = {'user_actions_cnt':0, 'user_loc_num':0, 'user_merchant_num':0, 'user_actions_day':0}
    day_set = set()
    if user in user_ulm_history:
        fea_dic['user_loc_num'] = len(user_ulm_history[user])
        for loc, m_records in user_ulm_history[user].items():
            user_loc_actions.setdefault(loc, {'cnt':0, 'day':[], 'his':np.ones(TIME_LEN)})
            fea_dic['user_merchant_num'] += len(m_records)
            for merchant, record in m_records.items():
                fea_dic['user_actions_cnt'] += record['cnt']
                user_merchants_actions.setdefault(merchant, {'cnt':0, 'day':[]})
                user_merchants_actions[merchant]['cnt'] += record['cnt']
                user_merchants_actions[merchant]['day'] += record['ts']
                user_loc_actions[loc]['cnt'] += record['cnt']
                user_loc_actions[loc]['day'] += record['ts']
                day_set.update(record['ts'])
            #user_loc_actions[loc]['his'] = cal_day_feature(user_loc_actions[loc]['day'], np.ones(TIME_LEN))
    fea_dic['user_actions_day'] = len(day_set)
    fea_str = ' '.join([str(val) for key, val in fea_dic.items()])
    return fea_str, user_loc_actions, user_merchants_actions, fea_dic

def main():
    ulm_file = sys.argv[1]
    feature_file = sys.argv[2]
    labels_file = sys.argv[3]
    mode = sys.argv[4]
    loc_merchants_file = sys.argv[5]
    loc_merchants = load_loc_merchants(loc_merchants_file)
    user_loc_merchants_real = pk.load(open(labels_file))
    user_ulm_history = pk.load(open(ulm_file))
    fres = open(feature_file, 'w')
    for user, loc_merchants_samples in user_loc_merchants_real.items():
        user_fea, user_loc_actions, user_merchants_actions, user_fea_dic = check_user_feature(user, user_ulm_history)
        for loc, samples in loc_merchants_samples.items():
            if 'train' in mode:
                for merchant in samples['pos']:
                    label = '1'
                    history_fea = check_history(user, loc, merchant, user_ulm_history,
                            user_loc_actions, user_merchants_actions, user_fea_dic)
                    fres.write(user + ',' + loc + ',' + merchant + '\t' + label + '\t' + user_fea + ' ' + history_fea + '\n')
                for merchant in samples['neg']:
                    if random.randint(1, 5) == 1:
                        label = '0'
                        history_fea = check_history(user, loc, merchant, user_ulm_history, user_loc_actions, user_merchants_actions, user_fea_dic)
                        fres.write(user + ',' + loc + ',' + merchant + '\t' + label + '\t' + user_fea + ' ' + history_fea + '\n')
            elif 'test' in mode:
                for merchant in loc_merchants[loc]:
                    label = '0'
                    if merchant in samples['pos']:
                        label = '1'
                    history_fea = check_history(user, loc, merchant, user_ulm_history,
                            user_loc_actions, user_merchants_actions, user_fea_dic)
                    fres.write(user + ',' + loc + ',' + merchant + '\t' + label + '\t' + user_fea + ' ' + history_fea + '\n')

    fres.close()
if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
