
. ./global.conf

python gen_merchant_feature.py $local_koubei_train_p1 $local_train_merchant_feature_zx $local_train_location_merchant_feature_zx local
python gen_merchant_feature.py $local_koubei_train_p2 $local_test_merchant_feature_zx $local_test_location_merchant_feature_zx local

# online merchant feature
python gen_merchant_feature.py $online_koubei_train $online_train_merchant_feature_zx $online_train_location_merchant_feature_zx online
python gen_merchant_feature.py $online_koubei_train $online_test_merchant_feature_zx $online_test_location_merchant_feature_zx online_test
