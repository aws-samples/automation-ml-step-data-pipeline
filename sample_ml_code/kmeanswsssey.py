#!/usr/bin/env python
#
# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
"""
A K-means clustering program (for some of the input columns only) 
Used to create the WSSSE graph that allows identification of the "best" K for
this data. Also provides the data for the "spider plots" of traffic regimes in
this paper: http://arxiv.org/abs/1602.03100 

The input (CSV) is expected to be a database extract. Each input row consists of
several columns of identifying information for this obs (cols 0 : first), 
followed by several columns of actual observation (cols first : last). 
This approach allows specific observations to be traced back to the source data if necessary.
Tested with 3 columns of observational variables.

For each k in the range (1: K) where K is a parameter to the program:
    Calculate and output cluster centers, std.dev. and Within Set Sum of Squared
    Error (WSSSE) for k clusters.

Uses Spark / MLlib.

Inputs: 
    infile      csv format file, 1 row per observation
    K           run clustering for each k in range (1 : K)  
Output: 
    CSV file    contains cluster centers and WSSSE for each k in range

Requires:
    pyspark, pyspark.mllib
    numpy

Original version based on code sample at: 
    http://spark.apache.org/docs/latest/mllib-clustering.html; 
Date: 2015
Author: V.Megler
"""

import sys
from math import sqrt
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import KMeans   
from pyspark.mllib.stat import Statistics

# if running pyspark, you get 'sc' automatically defined
#    sc = SparkContext(appName="KMeans E.G.")
conf = SparkConf().setAppName("KMeans E.G.")
sc = SparkContext(conf=conf)
"""
Dictionary incols relates the columns to the data extract. As I change the extract from time to time during the
project, this approach makes it easier to match input files and code versions used.
I'm only interested in clustering a subset of columns - but I need the rest for the anomaly analysis & tracability.
Columns [count starts from 0]: 
select:  highway, sensorstation, sensorid, 
yearday, dow, timeofday, volume, speed, occupancy
"""
incols = {'highway' : 0, 'sensorstation': 1, 'sensorid': 2, 'dayofyear': 3, 'dow': 4, 'time': 5, 'vol': 6, 'spd': 7, 'occ': 8 }
sensorset = incols['sensorid']
dow = incols['dow']    
#vol = 7
#spd = 8
#occ = 9
fst = incols['vol']        # "first" of the columns I'll be calculating on
lst = incols['occ'] + 1    # Splice ends at the index prior to lst ("last")
clstrcol = lst      # the column to place the cluster center 
        # (because there are sometimes more data columns that we're ignoring)
idstr = ''

def parse_vector(line):
    # Note that for this next line to work, all fields must be numeric.
    return np.array([float(x) for x in line.split(',')])
    
# Evaluate clustering by computing Within Set Sum of Squared Errors
# TO DO: What about using mlib.stat squared_distance, instead ?
def error(pt, dex):
    center = clusters.centers[int(dex)]
    return sqrt(sum([x**2 for x in (pt - center)]))

def pt_pred_arr(point):
    # Returns an np_array containing the original point and 
    # the cluster index that a given point belongs to.
    # e.g.: clusters.predict([1,0,1])
    pt = point[fst:lst]
    if np.count_nonzero(pt) > 0:
        cntr = clusters.predict(point[fst:lst])
    else:
        cntr = -1
    return np.r_[point, [cntr]]

if __name__ == "__main__":
    if len(sys.argv) != 5: 
        print >> sys.stderr, "Usage: kmeanswsssey.py <infile> <maxk> <runId> <outfile>"
        exit(-1)
        
    infilenm = sys.argv[1]      # input file name (in s3)
    maxk = int(sys.argv[2])     # max number of clusters: cluster from 1..maxk 
    runId = sys.argv[3]         # 
    outfilenm = '/mnt/var/sensor-' + runId + '.csv'  # tmp file, on local disk
    csvout = sys.argv[4]        # file to save to
         
    # Make the input file available to Spark (but it isn't read yet, really)
    lines = sc.textFile(infilenm)
    data = lines.map(parse_vector)   
    # Only want kmeans run on cols: volume, speed, occupancy
    # AND get rid of the known bad data: reporting all 0's
    # To limit the days of the week to, e.g., WEEKEND ONLY: 
    #    .filter(lambda arr: np.array(arr[2]) == 0 or np.array(arr[2] == 6)) 
    datasub = data.map(lambda arr: np.array(arr[fst:lst])) \
        .filter(lambda x: np.count_nonzero(x) > 0)
    
    # Output header string.
    nzcnt = datasub.count()         # used for run stats only
    outstr = []
    outstr.append( "----Input file: " + infilenm + "; " + str(lines.count()) + \
        " lines, " + str(nzcnt) + " selected. ")
    outstr.append("runid,WSSSE,k,cluster,count,mn:vol,mn:spd,mn:occ,stddv:vol,stddv:spd,stddv:occ ")
    with open(outfilenm, 'a') as f:
        f.write(outstr[0] + "\n" + outstr[1] + "\n")  
    
    # Now we're ready to calculate stats for each k in the range
    savedWsse = np.empty([maxk + 1])
    for k in range(1, maxk + 1):
        # e.g. clusters = KMeans.train(parsedData, k, maxIterations=10,
        #    runs=10, initializationMode="random")
        clusters = KMeans.train(datasub, k)
        
        # For each point: figure out the closest cluster center & add to row
        closestcenter = data.map(lambda cc: pt_pred_arr(cc))
        
        # Calculate the "error" from this combination of clusters
        # Scala version has computeCost; Python doesn't seem to, so compute "by hand".
        WSSSE = closestcenter.filter(lambda thisrow: thisrow[lst] >= 0) \
            .map(lambda thisrow: error(thisrow[fst:lst], thisrow[lst]))  \
            .reduce(lambda x, y: x + y)
        savedWsse[k] = WSSSE
        
        # For each cluster: get the standard deviation of the cluster's entries
        sigmasqd = np.empty([(lst - fst)])  # array to contain the variances
        for i in range(0, k):
            # Get the variance (already have the mean) for each column between fst and lst
            cstats = Statistics.colStats( closestcenter.filter(lambda row: row[clstrcol] == i) \
                .map(lambda row: row[fst:lst]))
            # The standard deviation is the square root of the variance.
            # sigmasqd[i] = cstats.variance()
            sigmasqd = cstats.variance()
            savestr = ','.join([runId, str(WSSSE),str(k), str(i), str(cstats.count())]) + "," + \
                ','.join(['%.1f' % num for num in clusters.centers[i]]) + "," + \
                ','.join(['%.1f' % sqrt(num) for num in sigmasqd]) 

            # I could put the write outside the loop. But I monitor results here sometimes.
            with open(outfilenm, 'a') as f:
                f.write(savestr)    
            outstr.append(savestr)

    outcsv = sc.parallelize(outstr)
    outcsv.coalesce(1).saveAsTextFile(csvout)
    # TO DO: create a plot of the WSSE's. But not now!
    sc.stop()
