# input list of files for script to find
# and consolidate fpkm reads

import sys

IDCOLUMN = 'target_id'
# change this to consolidate data from different column
DATACOLUMN = 'fpkm'

def extract_column(fname,cname):
    infile = open(fname,'r')
    columns = infile.readline().split()
    
    # make sure column exists
    if not cname in columns:
        print 'COLUMN %s does not exist!!' % cname
        return
    
    cindex = columns.index(cname)
    data = [line.split()[cindex] for line in infile]
    infile.close()
    return data
    
def main(args):
    # input is file containing list of files to series
    if not len(args) == 2:
        print 'usage: python series.py files.txt'
        return -1
    
    # get list of files to consolidate
    flist = [line.strip() for line in open(args[1])]
    
    # for each file in list
    ids = [None for i in xrange(len(flist))]
    datas = [None for i in xrange(len(flist))]
    for i in xrange(len(flist)):
        ids[i] = extract_column(flist[i],IDCOLUMN)
        datas[i] = extract_column(flist[i],DATACOLUMN)
        
    # create list of all ids
    master_ids = set()
    for i in xrange(len(flist)):
        master_ids.update(ids[i])

    master_ids = list(master_ids)
    master_ids.sort()
    # now master_id list is sorted
    
    sorted_indices = [None for i in xrange(len(flist))]
    for i in xrange(len(flist)):
        sorted_indices[i] = sorted(range(len(ids[i])),key=lambda x:ids[i][x])
        
    cs = [0 for i in xrange(len(flist))]
    id_lengths = [len(ids[i]) for i in xrange(len(flist))]
    for m in xrange(len(master_ids)):
        s = master_ids[m] + ' '
        for i in xrange(len(flist)):
            # make sure counter hasn't gone over length of file
            if cs[i] >= id_lengths[i]:
                s += 'NA '
            elif ids[i][sorted_indices[i][cs[i]]] == master_ids[m]:
                s += datas[i][sorted_indices[i][cs[i]]] + ' '
                cs[i] += 1
            else:
                s += 'NA '
        print s

if __name__ == '__main__':
    main(sys.argv)
