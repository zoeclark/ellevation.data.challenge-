

import math 
import sys 
import numpy as np
import pandas as pd




def get (csv):
	"""
	takes in a csv and returns a dataframe with all the information needed from the csv. 

	"""

	harvest = pd.read_csv(csv)[['sasid', 'stugrade','eperf2','mperf2','sperf2','escaleds','mscaleds','sscaleds','ecpi','mcpi','scpi']]
	for column in harvest[['eperf2','mperf2','sperf2']]:
		harvest = harvest.replace({column:{'F':'1-F', 'W':'2-W', 'NI':'3-NI', 'P':'4-P','A':'5-A','P+':'6-P'}} ) 
	return harvest 


def store(harvest):
	"""
	takes in a data frame, uses this data frame to generate a new data frame matching specifications, writes the new data frame as a csv file.  
	"""
	df = pd.DataFrame(columns = ('NCESID', 'StudentTestID', 'StudentLocalID', 'StudentGradeLevel', 'TestDate', 'TestName', 'TestTypeName', 'TestSubjectName', 'TestGradeLevel', 'Score1Label', 'Score1Type', 'Score1Value', 'Score2Label', 'Score2Type', 'Score2Value', 'Score3Label', 'Score3Type', 'Score3Value', 'Score4Label', 'Score4Type', 'Score4Value') ) 

	for index, row in harvest.iterrows():
		template = {'NCESID': 373737, 'StudentTestID': row['sasid'], 'StudentLocalID': 'Missing', 'StudentGradeLevel':row['stugrade'], 'TestName': 'MCAS', 'TestGradeLevel': row['stugrade'], 'Score1Label': 'Preformance Level', 'Score1Type': 'Level', 'Score2Label': 'Scaled Score', 'Score2Type': 'Scale', 'Score3Label':'CPI', 'Score3Type': 'Scale'}
		ELA = template 
		ELA.update({'TestDate': '4/1', 'TestTypeName':'MCAS ELA', 'TestSubjectName': 'ELA', 'Score1Value': row['eperf2'], 'Score2Value': row['escaleds'], 'Score3Value': row['ecpi'] })
		df = df.append(ELA, ignore_index = True) #This construction is bad for run time. A better method would store each row generated in this four loop in some kind of list, then load the list once into a pd.dataframe. I couldn't debugg this method, at least not fast enough :/ 

		Math = template 
		Math.update({'TestDate':'5/1', 'TestTypeName':'MCAS MATH', 'TestSubjectName': 'Math', 'Score1Value': row['mperf2'], 'Score2Value': row['mscaleds'], 'Score3Value': row['mcpi'] })
		df = df.append(Math, ignore_index = True)
		
		Science = template 
		Science.update({'TestDate': '6/1', 'TestTypeName': 'MCAS Science', 'TestSubjectName': 'Science', 'Score1Value': row['sperf2'], 'Score2Value':row['sscaleds'], 'Score3Value': row['scpi']})
		df = df.append(Science, ignore_index = True)
	
	df.to_csv('processed_mcas.csv', index = False)


if __name__ == "__main__":
	csv = sys.argv[1]
	store(get(csv)) 
