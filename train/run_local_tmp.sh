
. ../global.conf

model=$1
c_val=0.7
output_file='local_pred.txt'
local_submit_file='local_submit_file'
#:<<eof
if [ ${model} == 'fm' ]
then
    #output_file=local_fm_pred.txt
    ${libfm}/libFM -train $local_train_merge_feature -test $local_test_merge_feature -out $output_file -task c -save_model 'fm_110_local.model' -dim 1,1,8 -iter 100 -init_stdev 0.001
elif [ ${model} == 'gbdt' ]
then
    #output_file=local_gbdt_pred.txt
    tmp_file='tmp_watch.txt'
    head -10000 $local_test_merge_feature > $tmp_file
    python train_gbdt.py $local_train_merge_feature $local_test_merge_feature $output_file 2 2000 $tmp_file 3
elif [ ${model} == 'lr' ]
then
    lr_model='local_lr.model'
    lr_output='local_lr.output'
    $lr/train -s 6 -c 0.001 -w1 5 $local_train_merge_feature $lr_model
    $lr/predict -b 1 $local_test_merge_feature $lr_model $lr_output
    python change_lr_output.py $lr_output $output_file
fi
#eof
python gen_online_submit_file.py $local_test_koubei_feature $output_file $local_submit_file $c_val
#python evaluation.py $local_submit_file $local_test_koubei_feature $merchant_info
/home/ijcai/houjp/bin/score.sh $local_submit_file

lr_model='local_lr.model'
lr_output='local_lr.output'
#$lr/train -s 6 -c 1 $local_train_merge_feature $lr_model 

#$lr/predict -b 1 $local_test_merge_feature $lr_model $lr_output
