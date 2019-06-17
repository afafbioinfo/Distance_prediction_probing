#!/usr/bin/env python

import numpy as np
import re,os
from os.path import isfile, join

def openfile(Path):
    fileIn = open(Path, "r")
    lines = fileIn.readlines()
    fileIn.close()
    return lines

def GetListFile(PathFile, FileExtension):
    return [os.path.splitext(f)[0] for f in os.listdir(PathFile) if isfile(join(PathFile, f)) and os.path.splitext(f)[1] == '.' + FileExtension]
def parse_ProbingFile(file):
    lines = openfile(file)
    #print lines
    return [float(re.sub( '\s+', ' ', elem ).strip().split(' ')[1]) for elem in lines]


def Transform_reactivities(array):
        reactivities = [max(0,x) for x in array]
        q1 = np.percentile(reactivities, 30)
        q2 = np.percentile(reactivities, 70)
	#print "q1", q1
 	
        R=[0.5 for i in range(len(reactivities))]
        Lowest=[]
        Highest=[]
	for i,elem in enumerate(reactivities):
                #print "SOS",i, elem
		if elem <= q1: # to consider only 30% of elements that are showing a value of 0 instead of more than this percentage.t
			Lowest.append(i)
		elif elem >= q2 :
			Highest.append(i)
        Lowest = Lowest[:int(0.3*len(reactivities))]
        Highest = Highest[-int(0.3*len(reactivities)):]
        for i in Lowest:
            R[i] = 0
        for i in Highest:
            R[i] = 1
	return R

def Transorm_structure(Struct):
	P=[]
	for i in range(len(Struct)):
		if Struct[i]==".":
			P.append(1)
		else:
			P.append(0)
	return P
def Deviation(R, P):
	N= len(P)
	A= 0.4*N/2
	B=0.6*N
	return (sum([np.abs(R[i]-P[i]) for i in range(N)])-A)/B
if __name__ == "__main__":
	FileExtension= "optimals"
	FileExtensionR = "Shape.txt"
 	path= "Multiprobing_march2"
	path_reactivities= "Reactivities"
	for filz in GetListFile(path, FileExtension):
                
		# get reactivities
		reactivityFile = os.path.join(path_reactivities, filz  + FileExtensionR)
		reactivity=parse_ProbingFile(reactivityFile)
		# Get structures
		strutureFile=os.path.join(path, filz  + "."+ FileExtension)
                #print strutureFile
		structure= list(openfile(strutureFile)[0][:-1]) 
		print filz[4:],"\t",round(Deviation(Transform_reactivities(reactivity),Transorm_structure(structure)),4)
		#react=np.array([0.0029,0.0044,0.0042,0.004,0.0066,0.0055,0.008,0.004,0.0067,0.01,0.0049,0.0036,0.0342,0.0566,0.0069,0.0025,0.0149,0.0153,0.004,0.0215,0.0175,0.0058,0.0197,0.0136,0.0144,0.0975,0.0559,0.0211,0.0681,0.315,0.0056,0.0044,0.0211,0.0195,0.0066,0.0249,0.0167,0.0171,0.022,0.0515,0.0326,0.0164,0.0235,0.008,0.0075,0.0209,0.0142,0.0135,0.0066,0.0227,0.0317,0.0326,0.0255,0.0308,0.0164,0.0109,0.0184,0.0251,0.0129,0.0158,0.0124,0.0107,0.0169,0.0133,0.0222,0.0226,0.0338,0.0227,0.0564,0.0584,0.0147,0.0093,0.0215,0.0104,0.0113,0.0122,0.0104,0.0086,0.1032,0.1314,0.012,0.0673,0.018,0.0382,0.0177,0.0282,0.0124,0.0115,0.014,0.0892,0.0646,0.0748,0.0293,0.0127,0.0124,0.0129,0.0275,0.0197,0,1,0,0.0497,0.0959,0.0136,0.0198,0.0479,0.0089,0.0659,0.0304,0.1654,0.0089,0.0371,0.03,0.0244,0.0162,0.1076,0.0621,0.0724,0.0109,0.0124,0.0109,0.0113,0.0096,0.0246,0.0142,0.0164,0.0087,0.0311,0.1086,0.0173,0.0115,0.0566,0.0157,0.006,0.0233,0.0106,0.018,0.0093,0.0193,0.0153,0.0078,0.0295,0.0337,0.0242,0.0146,0.0568,0.0524,0.0204,0.0692,0.0087,0.0193,0.0177,0.0178,0.0155,0.0164,0.0038,0.0069,0.0136,0.0308,0.0315,0.0504,0.0091,0.0069,0.0284,0.0402,0.0113,0.079,0.0613,0.024,0.0073,0.0131,0.0149,0.0098,0.0126,0.0959,0.0217,0.0104,0.0064,0.0055,0.0184,0.0258,0.0066,0.0449,0.0195,0.0198,0.0306,0.0076,0.0124])

	#print Transform_reactivities(react)

	#test="((..))"
	#print Transorm_structure(test)
