#! /usr/bin/env python

def wiggle2bed(wigfile,outfile,outfile1):
    f = open(wigfile,'r') # open an input .wig file
    f2 = open(outfile,'w') # open an output file
    f3 = open(outfile1,'w') # open the second output file
    sepstring = 'fixedStep' # "sepstring" is used to separate cluster from .wig file 
    ALL = f.read() # read an input file
    ALL = ALL.split(sepstring)[1:] # split the input file into clusters by "sepstring"
    for all in ALL: # for each cluster
        
        # get all score values from the cluster
        cluster_values = all.split(os.linesep,1)[1].split(os.linesep)
        cluster_values = cluster_values[0:len(cluster_values)-1]
        cluster_values = [float(x) for x in cluster_values]
        max_score = max(cluster_values) # find the maximum score of the cluster
        
        # create a dictionary from cluster score values
        cluster_dict = dict([(x, cluster_values[x-1]) for x in 
                              range(1,len(cluster_values)+1)])
        k = cluster_dict.keys()
        v = cluster_dict.values()
        for i in k:
            if v[i-1] != max_score:
                cluster_dict.pop(i) # narrow the dictionary leaving only nodes
                                    # corresponding to the max_score
        clust_middle = round(len(cluster_dict)/2) # middle of the narrowed cluster
        
        strand = wigfile.split('_')[2] # define the strand
        
        desline = all.split(os.linesep,1)[0]
        chr = desline.split()[0].split('=')[1] # define the chromosome
        clust_start = int(desline.split()[1].split('=')[1]) + cluster_dict.keys()[0] - 1
        
              start = int(clust_start + clust_middle - 1)
        end = int(clust_start + clust_middle + 1)
        print >>f2, '\t'.join([chr, str(start), str(end), ".", str(max_score), strand])
        for i in [start, start + 1, start + 2]:
            print >>f3, '\t'.join([chr, str(i), str(i + 1), ".", str(max_score), strand])

            
    f.close()
    f2.close()
    f3.close()
        
if __name__ == '__main__': 
    import sys
    import time
    import os
    
    if len(sys.argv) == 1:
        print "usage:python wig2bed.py wigfile bedfile1 bedfile2"
        print "the output filename is: [wigfile].bed"
    else:
        wigfile = sys.argv[1]
        outfile = sys.argv[2]
        outfile1 = sys.argv[3]
        starttime = time.time()
        wiggle2bed(wigfile,outfile,outfile1)
        endtime = time.time()
        print "DONE! Takes %f seconds" % (endtime-starttime)
        
