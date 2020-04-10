#!/usr/bin/env python
"""
Anomaly detection, where anomalies are "too far" from one of k cluster centers.

Calculate cluster centers for k clusters (where k is an input).
Then: for each observation in the input file, assign it to the closest cluster 
and calculate the Mahalanobis distance from that point to the cluster center.
Output the original observation, plus the additional calculated columns:  
    assigned_cluster, cluster center, distance 
    
The input (CSV) is expected to be a database extract. Each input row consists of
several columns of identifying information for this obs (cols 0 : first), 
followed by several columns of actual observation (cols first : last). 
This approach allows anomalies to be traced back to the source data if necessary.
Tested with 3 columns of observational variables.

Uses Spark / Mllib.

Inputs: 
    infile      csv format file, 1 row per observation
    k           number of clusters to use
    outfile     directory to place output files in 
Output: 
    CSV file    input file + calculated columns

Requires:
    pyspark, pyspark.mllib
    scipy.spatial
    numpy

"""
import sys
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import KMeans  
import scipy.spatial.distance as sci  # for Mahalanobis distance calc

# if running pyspark / spark-submit, 'sc' is automatically defined
#    sc = SparkContext(appName="KMeans E.G.")
conf = SparkConf().setAppName("KMeans E.G.")
sc = SparkContext(conf=conf)
"""
Dictionary 'incols' relates infile's columns to the data extracted.
Columns [count starts from 0]: 
select:  highway, sensorstation, sensorid, 
yearday, dow, timeofday, volume, speed, occupancy
"""
incols = {'highway' : 0, 'sensorstation': 1, 'sensorid': 2, 'dayofyear': 3, 'dow': 4, 'time': 5, 'vol': 6, 'spd': 7, 'occ': 8 }
sensorset = incols['sensorid']
dow = incols['dow'] 
# Columns we want to cluster on are: fst:lst
fst = incols['vol'] 
lst = incols['occ'] + 1   
clstrcol = lst    # the column for the cluster center TO FIX
idstr = ''

def parse_vector(line):
    return np.array([float(x) for x in line.split(',')])

def pt_pred_arr(point):
    # Returns the original point and the cluster index that a given point belongs to.
    # e.g.: clusters.predict([1,0,1])
    cntr = -1
    pt = point[fst:lst]
    cntrpt = np.zeros_like(pt)   # Create "null" array: if there's no center
    if np.count_nonzero(pt) > 0:
        cntr = clusters.predict(point[fst:lst])
        cntrpt = clusters.centers[cntr]
    return np.r_[point, [cntr], cntrpt]

if __name__ == "__main__":    
    if len(sys.argv) != 4: 
        print >> sys.stderr, "Usage: kmeansande.py <infile> <k> <outfile>"
        exit(-1)
        
    infilenm = sys.argv[1]         # input file name (in s3)
    k = int(sys.argv[2])           # number of clusters to use
    outfilenm = sys.argv[3]     
    
    # Read the main data file
    lines = sc.textFile(infilenm)

    alldata = lines.map(parse_vector)  
    # Only want kmeans run on columns fst:lst
    # For weekend only: .filter(lambda arr: np.array(arr[incols['dow']]) == 0 
    #       or np.array(arr[incols['dow']] == 6))     
    datasub = alldata.map(lambda arr: np.array(arr[fst:lst])) \
        .filter(lambda x: np.count_nonzero(x) > 0)
    clusters = KMeans.train(datasub, k)
    # For each point: figure out the closest cluster center
    # Add each cluster center as additional columns to the original input
    closestcenter = alldata.map(lambda cc: pt_pred_arr(cc))

    # For M.distance calc: need inverted covariance matrix as part of inputs.
    # So: For each cluster 'c', calculate the covariance matrix. 
    inv_covmat = []
    for c in range(0, k):
        # Get the actual data columns (subset of the whole line) 
        data = closestcenter.filter(lambda arr: np.array(arr[clstrcol]) == c) \
            .map(lambda arr: np.array(arr[fst:lst]))
        # Calc the covariance matrix, and invert
        # Convert from RDD to list, so numpy stats will run against it
        # OR - could write a function to calc the covariance matrix against this RDD ...
        datacol = data.collect()
        dtcnt = len(datacol)
        if dtcnt == 0:
            print "Error? - No data for cluster #" + str(c) + ".\n"
            iterate 
        covmat = np.cov(datacol,None,0)        # Get covariance matrix
        inv_covmat.append( np.linalg.inv(covmat))  # Invert

    # Calc the Malhanobis distance for each point and append to row
    dists = closestcenter.map(lambda dst: 
        ','.join(['%.2f' % num for num in 
		(np.r_[dst, sci.mahalanobis(dst[fst:lst], 
        	clusters.centers[int(dst[clstrcol])], 
        	inv_covmat[int(dst[clstrcol])])])]))  
    dists.saveAsTextFile(outfilenm)     # output resulting file

    sc.stop()
