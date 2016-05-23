import sys
import cPickle as pk
import datetime
def get_day_delta(date1,date2):

    y1,m1,d1 = int(date1[:4]),int(date1[4:6]), int(date1[6:])
    y2,m2,d2 = int(date2[:4]),int(date2[4:6]), int(date2[6:])
    d1 = datetime.datetime(y1,m1,d1)
    d2 = datetime.datetime(y2,m2,d2)
    day_diff = (d2-d1).days
    return day_diff

def main():

    koubei_file = sys.argv[1]
    mode = sys.argv[2]
    uml_action_feature = sys.argv[3]
    user_loc_m_fea = {}
    with open(koubei_file) as f:
        for line in f:
            user, merchant, loc, ts = line.rstrip().split(',')
            cur_time = 0
            # filter monthe 11 data
            if mode == 'local_train' or mode == 'local_test' or mode == 'online_train':
                if ts[4:6] == '11':
                    continue
                cur_time = get_day_delta(ts ,'20151101')
            else:
                cur_time = get_day_delta(ts, '20151201')
            user_loc_m_fea.setdefault(user, {})
            user_loc_m_fea[user].setdefault(loc, {})
            user_loc_m_fea[user][loc].setdefault(merchant, {'cnt':0, 'ts':[]})
            # update feature
            user_loc_m_fea[user][loc][merchant]['cnt'] += 1
            user_loc_m_fea[user][loc][merchant]['ts'].append(cur_time)
    pk.dump(user_loc_m_fea, open(uml_action_feature, 'w'))


if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
