import sys

def load_submit_file(filename):
    user_loc = {}
    with open(filename) as f:
        for line in f:
            user, loc, rec = line.rstrip().split(',')
            user_loc[user+','+loc] = line
    return user_loc

def main():
    old_submit = sys.argv[1]
    new_submit = sys.argv[2]
    fres = open(sys.argv[3], 'w')
    old_user_rec = load_submit_file(old_submit)
    with open(new_submit) as f:
        for line in f:
            user, loc, rec = line.rstrip().split(',')
            ul = user+','+loc
            if ul in old_user_rec:
                fres.write(old_user_rec[ul])
            else:
                fres.write(line)
    fres.close()

if __name__ == '__main__':
    main()
# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
