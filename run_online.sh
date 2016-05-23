
. ./global.conf
#:<<eof
# generate postive and negative merchants for each user in each location
python gen_postive_uml.py $online_koubei_train $location_merchants $online_train_pos_neg_file
python gen_online_test_uml.py $online_koubei_test $location_merchants $online_test_pos_neg_file
# gen feature

echo 'preprocesing...'
python preprocess_data.py $online_koubei_train online_train $online_train_uml_actions 
python preprocess_data.py $online_koubei_train online_test $online_test_uml_actions 
#eof
#python gen_taobao_user_feature.py $taobao_data ${online_taobao_user_feature} $taobao_seller_id $taobao_cate_id $koubei_all_users online
echo 'gen uml feature...'
python gen_user_loc_merchant_feature.py $online_train_uml_actions $online_train_koubei_feature $online_train_pos_neg_file online_train $location_merchants
python gen_user_loc_merchant_feature.py $online_test_uml_actions $online_test_koubei_feature $online_test_pos_neg_file online_test $location_merchants

python get_loc_merchant_id.py $online_train_koubei_feature $online_train_loc_mid_feature

#:<<eof
sh run_merchant.sh
echo 'merge feature...'
python merge_koubei_taobao_all_feature.py $online_train_koubei_feature $online_train_merge_feature $local_taobao_user_feature $online_train_merchant_feature $online_train_location_feature $online_train_merchant_feature_zx $online_train_location_merchant_feature_zx $merchant_interests_file $online_train_loc_mid_feature
python merge_koubei_taobao_all_feature.py $online_test_koubei_feature $online_test_merge_feature $local_taobao_user_feature $online_test_merchant_feature $online_test_location_feature $online_test_merchant_feature_zx $online_test_location_merchant_feature_zx $merchant_interests_file $online_train_loc_mid_feature


cd train
sh run_online_train.sh fm
#eof
