import sys

def main():
    lr_output = sys.argv[1]
    pred_file = sys.argv[2]
    f_pred = open(pred_file, 'w')
    f = open(lr_output)
    line = f.readline()
    _, label1, label2 = line.rstrip().split(' ')
    while 1:
        line = f.readline()
        if not line:
            break
        label, pred1, pred2 = line.rstrip().split()
        if label1 == '1':
            f_pred.write(pred1 + '\n')
        else:
            f_pred.write(pred2 + '\n')
    f_pred.close()

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
