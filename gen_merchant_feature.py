import sys
import datetime
import numpy as np
TIME_RANGE=[1,3,5,7,15,21,30,60,200]
TIME_LEN = len(TIME_RANGE)
def get_day_delta(date1,date2):
    y1,m1,d1 = int(date1[:4]),int(date1[4:6]), int(date1[6:])
    y2,m2,d2 = int(date2[:4]),int(date2[4:6]), int(date2[6:])
    d1 = datetime.datetime(y1,m1,d1)
    d2 = datetime.datetime(y2,m2,d2)
    day_diff = (d2-d1).days
    return day_diff
def get_action_range(ts, init_day):
    cur_index = get_day_delta(ts, init_day)
    a = np.zeros(TIME_LEN)
    for i in range(TIME_LEN):
        if cur_index <= TIME_RANGE[i]:
            a[i] = 1
    return a
def get_repeat_cnt(user_dic):
    cnt = 0
    for user, val in user_dic.items():
        if val > 1:
            cnt += 1
    if cnt == 0:
        return 1
    else:
        return cnt

def main():
    koubei_file = sys.argv[1]
    merchant_feature_file = sys.argv[2]
    loc_mer_feature_file = sys.argv[3]
    mode = sys.argv[4]
    loc_merchants_fea = {}
    merchants_fea = {}
    total_cnt = 0
    user_set = set()
    loc_actions = {}
    init_day = '20151101'
    if mode == 'online_test':
        print mode
        init_day = '20151201'
    with open(koubei_file) as f:
        for line in f:
            user, merchant, location, ts = line.rstrip().split(',')
            if mode != 'online_test':
                if ts[4:6] == '11':
                    continue
            total_cnt += 1
            action_list = get_action_range(ts, init_day)
            user_set.add(user)
            loc_merchants_fea.setdefault(location, {})
            loc_actions.setdefault(location, {'cnt':np.ones(TIME_LEN), 'user':{}})
            loc_merchants_fea[location].setdefault(merchant, {'cnt':np.zeros(TIME_LEN), 'user':{}})
            merchants_fea.setdefault(merchant, {'cnt':np.zeros(TIME_LEN), 'user':{}})

            # update actions
            loc_actions[location]['cnt'] += action_list
            loc_actions[location]['user'].setdefault(user, 0)
            loc_actions[location]['user'][user] += 1
            loc_merchants_fea[location][merchant]['cnt'] += action_list
            loc_merchants_fea[location][merchant]['user'].setdefault(user, 0)
            loc_merchants_fea[location][merchant]['user'][user] += 1
            merchants_fea[merchant]['cnt'] += action_list
            merchants_fea[merchant]['user'].setdefault(user, 0)
            merchants_fea[merchant]['user'][user] += 1
    # gen feature
    loc_merchants_feature = {}
    user_cnt = len(user_set)
    flm = open(loc_mer_feature_file, 'w')
    for location, merchant_fea in loc_merchants_fea.items():
        cur_loc_user_cnt = len(loc_actions[location]['user'])
        avg_buy_person_loc = 1.0*loc_actions[location]['cnt'][-1]/cur_loc_user_cnt
        for merchant, feature in merchant_fea.items():
            cur_loc_m_user_cnt = len(feature['user'])
            #last_month_cnt = feature['cnt'][4]
            repeat_cnt = get_repeat_cnt(feature['user'])
            repeat_cnt_ratio = 0
            repeat_cnt_ratio = 1.0*repeat_cnt/get_repeat_cnt(loc_actions[location]['user'])
            # avg buy cnt
            #avg_buy_person = 1.0*feature['cnt'][-1]/cur_loc_m_user_cnt
            #avg_buy_person_ratio = 1.0*avg_buy_person/avg_buy_person_loc

            #cnt_fea_list = [repeat_cnt_ratio,]# avg_buy_person_ratio]
            #cnt_fea = ' '.join([str(val) for val in cnt_fea_list])

            location_merchant_hotrank = feature['cnt']/loc_actions[location]['cnt']
            lm_user_ratio = 1.0*len(feature['user'])/cur_loc_user_cnt
            lm_hotrank_fea = ' '.join([str(val) for val in location_merchant_hotrank])
            flm.write(location+','+merchant + '\t' + lm_hotrank_fea + ' ' + str(lm_user_ratio) + '\n')
    flm.close()
    # write merchant feature
    with open(merchant_feature_file, 'w') as f:
        for merchant, feature in merchants_fea.items():
            cur_m_user_cnt = len(feature['user'])
            #last_month_cnt = feature['cnt'][4]
            #repeat_cnt = get_repeat_cnt(feature['user'])
            #avg_buy_person = 1.0*feature['cnt'][-1]/cur_m_user_cnt
            #cnt_fea_list = [last_month_cnt, repeat_cnt]
            #cnt_fea = ' '.join([str(val) for val in cnt_fea_list])
            merchant_hot = feature['cnt']/total_cnt
            user_ratio = 1.0*cur_m_user_cnt/user_cnt
            merchant_hot_fea = ' '.join([str(val) for val in merchant_hot])
            f.write(merchant + '\t' + merchant_hot_fea + ' ' + str(user_ratio) + '\n')



if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
