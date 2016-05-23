
. ../global.conf

model=$1

output_file='online_pred_'${model}'.txt'
online_submit_file='online_submit_file_'${model}'.csv'
online_submit_file_post='online_submit_file_'${model}'_post.csv'
theata=0.5
#:<<eof
if [ ${model} == 'fm' ]
then
    #output_file=local_fm_pred.txt
    ${libfm}/libFM -train $online_train_merge_feature -test $online_test_merge_feature -out $output_file -task c -save_model 'online_fm_110.model' -dim 1,1,10 -iter 100 -init_stdev 0.01
    theata=0.2994
    #theata=0.31
elif [ ${model} == 'gbdt' ]
then
    #output_file=local_gbdt_pred.txt
    online_tmp='online_tmp_file.txt'
    head -100000 $online_test_merge_feature >$online_tmp
    python train_gbdt.py $online_train_merge_feature $online_test_merge_feature $output_file 2 5000 $online_tmp 2
elif [ ${model} == 'lr' ]
then
    lr_model='online_lr.model'
    lr_output='online_lr.output'
    $lr/train -s 6 -c 0.001 -w1 5 $online_train_merge_feature $lr_model
    $lr/predict -b 1 $online_test_merge_feature $lr_model $lr_output
    python change_lr_output.py $lr_output $output_file
fi
#eof
#python gen_online_submit_file.py $online_test_koubei_feature $output_file $online_submit_file 0.875

python gen_online_postprocess.py $online_test_koubei_feature $output_file $theata'_'$online_submit_file_post $theata $merchant_info

#val=$2
#python gen_online_postprocess.py $online_test_koubei_feature $output_file $val'_'$online_submit_file_post $val $merchant_info

#$lr/train -s 6 -c 1 $local_train_merge_feature $lr_model 

#$lr/predict -b 1 $local_test_merge_feature $lr_model $lr_output
