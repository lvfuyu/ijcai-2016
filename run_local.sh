
. ./global.conf
#:<<eof
python get_location_merchant.py $merchant_info $location_merchants

# generate postive and negative merchants for each user in each location
python gen_postive_uml.py $local_koubei_train_p1 $location_merchants $p1_pos_neg_file
python gen_postive_uml.py $local_koubei_train_p2 $location_merchants $p2_pos_neg_file
echo 'run preprocessing ...'
python preprocess_data.py $local_koubei_train_p1 local_train $local_train_uml_actions 
python preprocess_data.py $local_koubei_train_p2 local_test $local_test_uml_actions 
eof
#python gen_taobao_user_feature.py $taobao_data ${local_taobao_user_feature} $taobao_seller_id $taobao_cate_id $koubei_all_users local

#:<<eof
echo 'run uml feature ...'
python gen_user_loc_merchant_feature.py $local_train_uml_actions $local_train_koubei_feature $p1_pos_neg_file local_train $location_merchants
python gen_user_loc_merchant_feature.py $local_test_uml_actions $local_test_koubei_feature $p2_pos_neg_file local_test $location_merchants
#:<<eof
python get_loc_merchant_id.py $local_train_koubei_feature $local_train_loc_mid_feature
#eof
echo 'run merge feature'
# merge all features
sh run_merchant.sh
python merge_koubei_taobao_all_feature.py $local_train_koubei_feature $local_train_merge_feature $local_taobao_user_feature $local_train_merchant_feature $local_train_location_feature $local_train_merchant_feature_zx $local_train_location_merchant_feature_zx $merchant_interests_file $local_train_loc_mid_feature $local_koubei_p1_user_lmid_index $local_koubei_p1_user_lmid_embedding
python merge_koubei_taobao_all_feature.py $local_test_koubei_feature $local_test_merge_feature $local_taobao_user_feature $local_test_merchant_feature $local_test_location_feature $local_test_merchant_feature_zx $local_test_location_merchant_feature_zx $merchant_interests_file $local_train_loc_mid_feature $local_koubei_p2_user_lmid_index $local_koubei_p2_user_lmid_embedding

cd train
sh run_local_train.sh fm
