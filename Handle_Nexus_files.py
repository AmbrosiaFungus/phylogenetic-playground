#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:20:08 2018

@author: robert
"""
#Create this file to manipulate the names of nexus files. I want to switch the name and accession numbers to concatenate an alignment later on 

file2 = open("Beta_tubulin_BatchEntrez_Ophiostomatales_aligned_18Jan2018_exons.nxs", "r") #input file of a nexus file
file = open("test.nxs", 'w+') #output file

for line in file2:
    if line.startswith("["):
        line = line.replace('\n','')
        x = line.split(" ")[1]
        y = x.split("_")
        len_fungi = len(y)
        if len_fungi==3:
            z = "_".join([y[1],y[2],y[0]])
        elif len_fungi==4:
            z = "_".join([y[1],y[2],y[3], y[0]])
        else:
            z = "_".join([y[1],y[2],y[0]])
        k = z + "\n"
        line = line.replace(x, k)
        #print(line)
    file.write(line)
file.close()
file2.close()    
            
            
