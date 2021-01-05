from flask import Flask, request
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

engine = create_engine("")

@app.route('/', methods=['GET','POST'])
def main():

	if request.method == "POST":
		if 'file' not in request.files:
			return {"Message":"file not uploaded"}
		# con = psycopg2.connect(host = 'localhost' dbname = 'testdb' user = 'adialachar' password = 'squirtle123')
		# cur = con.cursor()
		file_ = request.files['file']
		print("1")
		# upload csv to database
		df = pd.read_csv(file_)
		print(df.head())
		print("2")
		df.to_sql('temp_table',con=engine)
		print("3")
		print(engine.execute('select * from temp_table').fetchall())
		print("4")
		return {"Message":"success"}

	return {"Message":"need post"}

@app.route('/a/<dataset>', methods=['GET','POST'])
def a(dataset):
	tablename = ""
	if dataset == "turk":
		tablename = "/Users/aditya/Downloads/data_dumm - data_akbilgic.csv"
	elif dataset == "wine":
		tablename = "/Users/aditya/Downloads/winequality-red - winequality-red.csv"
	

	results = (engine.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tablename}' AND DATA_TYPE='double precision' ORDER BY ORDINAL_POSITION").fetchall())


	L = {}

	for row in results:
		row_name = row[0]
		zscore = f'''
		WITH attr_table as 

		(SELECT AVG("{row_name}") AS MEAN,
				STDDEV("{row_name}") AS STDEV FROM "{tablename}")

		SELECT ABS("{row_name}" - attr_table.MEAN) / attr_table.STDEV as ZSCORE

		FROM attr_table, "{tablename}"
		'''
		
		
		
		
		
		
		z = (engine.execute(zscore).fetchall())
		# print(z)
	#     z = list(map(lambda x:x[0], z))
		L[row_name] = z
		d_list = []
		for p in L.keys():
			
			d_list.append(pd.DataFrame( L[p], columns=[p]))
			
		# print("hi", d_list)
		


	from functools import reduce
	df = reduce(lambda df1,df2: pd.merge(df1,df2,left_index=True,right_index=True), d_list)


	#find ever major anomaly and say (colX has y major annomalie(s) )
	# for each column, isolate the anamolies.
	D = {}
	for i in range(0, len(results)):
		D[f'{results[i][0]}'] = (df.loc[df[f'{results[i][0]}'] >= 3.5]).sort_values(by=[f'{results[i][0]}'],ascending=False)
		# print(D[f'{results[i][0]}'][f'{results[i][0]}'])


	existing_keys = list(filter(lambda x: len(D[x]) > 0, D.keys()))
	# print(existing_keys)
	import random
	cols = random.sample(existing_keys, 2)
	anomaly1_sentence = (f"There are {len(D[cols[0]].index)} major anomalies in column {cols[0].upper()}")
	anomaly2_sentence = (f"There are {len(D[cols[1]].index)} major anomalies in column {cols[1].upper()}")

	# from collections import defaultdict
	# date_type_exists = (engine.execute(f'''SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "{tablename}"''').fetchall())
	ccc = list(map( lambda x:x[0], engine.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tablename}' ORDER BY ORDINAL_POSITION").fetchall()))
	dft = pd.DataFrame(data=engine.execute(f'''SELECT * FROM "{tablename}" ''').fetchall(),columns=ccc)
	print(dft)
	# print(engine.execute(f'''SELECT * FROM "{tablename}" ''').fetchall())
	# print(dft.dtypes)
	# print(dft)
	# from pandas.api.types import is_datetime64_any_dtype as is_datetime

	# print(dft[[column for column in dft.columns if is_datetime(dft[column])]])



	# dft = pd.read_csv(open(tablename, "r"))
	# print(dft[[column for column in dft.columns if is_datetime(dft[column])]])

	# print(dft)
	contains_date = False
	date_col_name = ""
	from pandas import Timestamp
	for i in range(0,len(dft.columns)):
		data = (pd.to_datetime(dft[dft.columns[i]].to_list()))
		# print(type(pd.to_datetime(dft[dft.columns[i]].to_list())))




		# print(data.to_list())
		if data.to_list()[0].year != Timestamp('1970-01-01 00:00:00').year:
			contains_date = True
			date_col_name = dft.columns[i]
	# print(contains_date, date_col_name)
			
		


	# if len(date_type_exists) > 0:
	# 	# commence with the z scoring
	# print(date_type_exists)
	# print(df.dtypes)
	anomaly_sentences = []
	if contains_date == True and date_col_name != "":
		from collections import defaultdict

		TR = defaultdict(list)
		for i in range(0,len(cols)):
			for index, row in D[cols[i]].iterrows():
				a = []
				rownumber = index
				a.append(dft.iloc[rownumber - 2][[date_col_name, cols[i]]].to_list() )
				a.append(dft.iloc[rownumber - 1][[date_col_name, cols[i]]].to_list())
				a.append(dft.iloc[rownumber][[date_col_name, cols[i]]].to_list())
				a.append(dft.iloc[rownumber + 1][[date_col_name, cols[i]]].to_list())
				a.append(dft.iloc[rownumber + 2][[date_col_name, cols[i]]].to_list())
				TR[cols[i]].append(a)
				anomaly_sentences.append(f"There was a major anomaly on date {dft.iloc[rownumber][[date_col_name]].to_list()[0]} for column {cols[i]}")
				break
		zscore = {"zscorecol1":cols[0], "zscorecol2":cols[1], "sentence1":anomaly_sentences[0], "sentence2":anomaly_sentences[1] , "zscoredata1":TR[cols[0]], "zscoredata2":TR[cols[1]]}


		print(TR)
				
	#information needed: column name, sentence, data
	#szscorecol1, zscorecol2, 

	# now gather surrounding data of the two 
	# a = []
	# for i in range(len(D[cols[0]])):
		





	import numpy as np
	from sklearn.linear_model import LinearRegression
	dfp = (df.corr()).unstack()
	so = dfp.sort_values(kind="quicksort").drop_duplicates()
	# print((so)[-5:])
	z = (list(zip(so,so.index)))
	z = list(filter (lambda x:x[0] < 1 , z))

	z.sort(reverse=True)
	# print(z)
	strong_pos_correlations = z
	# strong_pos_correlations = list(filter(lambda x:x[0] >= 0.7 and x[0] < 1, z))
	# print(strong_pos_correlations)

	# moderate_pos_correlations = list(filter(lambda x:x[0] >= 0.49 and x[0] < 0.7, z))
	# print(moderate_pos_correlations[-5:])

	# strong_neg_correlations = list(filter(lambda x:x[0] <= -0.7 and x[0] > -1, z))
	# print(strong_neg_correlations)

	# moderate_neg_correlations = list(filter(lambda x:x[0] <= -0.49 and x[0] > -0.7, z))
	# print(moderate_neg_correlations[-5:])


	# logic 
	# maximum 2 correlations can come from here 
	# if strong has 2, return both strongs
	# if strong is empty, return top two mediums
	# if medium
	




	strong = []
	for i in range(0,len(strong_pos_correlations)):
		col1 = strong_pos_correlations[i][1][0]
		col2 = strong_pos_correlations[i][1][1]
		correlation_coefficient = strong_pos_correlations[i][0]
		d = (engine.execute(f'''SELECT "{col1}", "{col2}" from "{tablename}" LIMIT 20''').fetchall()) 

		m = list(map( lambda x:{"x": x[0] , "y":x[1] } ,d ))
		x = list(map( lambda x:x[0] ,d ))
		# print(x)
		X = np.asarray(x).reshape(-1,1)
		# print(X)
		y = np.asarray(list(map( lambda x:x[1] ,d )))

		model = LinearRegression().fit(X,y)
		
		# line_of_best_fit = ""
		line_of_best_fit = list(map(lambda x:{"x":x, "y": model.predict(np.asarray(x).reshape(-1,1)).tolist()[0]}, x ))
		# print(line_of_best_fit)
		sentence = ""
		if correlation_coefficient >= 0.7:
			sentence = f"{col1} has a strong positive correlation with {col2} (correlation = {round(correlation_coefficient,5)})"
		elif correlation_coefficient < 0.7 and correlation_coefficient >= 0.5:
			sentence = f"{col1} has a moderate positive correlation with {col2} (correlation = {round(correlation_coefficient,5)})"
		elif correlation_coefficient < 0.5 and correlation_coefficient >= 0.3:
			sentence = f"{col1} has a weak positive correlation with {col2} (correlation = {round(correlation_coefficient,5)})"
		elif correlation_coefficient <= -0.7:
			sentence = f"{col1} has a strong negative correlation with {col2} (correlation = {round(correlation_coefficient,5)})"
		elif correlation_coefficient > -0.7 and correlation_coefficient <= -0.5:
			sentence = f"{col1} has a moderate negative correlation with {col2} (correlation = {round(correlation_coefficient,5)})"
		elif correlation_coefficient > -0.5 and correlation_coefficient <= -0.3:
			sentence = f"{col1} has a weak negative correlation with {col2} (correlation = {round(correlation_coefficient,5)})"


			

		strong.append({"col1":col1, "col2": col2, "coords": m, "line_of_best_fit":line_of_best_fit, "correlation_coefficient": strong_pos_correlations[i][0], "sentence":sentence})
	return {"data":strong, "zscore": zscore}
		# a = list( map( lambda x: ,
		# b = list( map( lambda x:x[0] ,engine.execute(f"SELECT {col2} from {tablename}").fetchall()))







			
# 	results = (engine.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'temp_table' AND DATA_TYPE='double precision' ORDER BY ORDINAL_POSITION").fetchall())
	
# 	t = '''

# WITH attr_table as 
		
# 		(SELECT AVG(EU) AS MEAN,
# 				STD(EU) AS STDEV F)

# 		SELECT ABS(EU - attr_table.MEAN) / attr_table.STDEV as ZSCORE

# 		FROM attr_table, temp_table 

# 		'''
# 	L = {}
	
# 	for row in results:
# 		row_name = row[0]
# 		zscore = f'''
# 		WITH attr_table as 
		
# 		(SELECT AVG("{row_name}") AS MEAN,
# 				STDDEV("{row_name}") AS STDEV FROM temp_table)

# 		SELECT date, ABS("{row_name}" - attr_table.MEAN) / attr_table.STDEV as ZSCORE

# 		FROM attr_table, temp_table 
# 		'''
# 		z = (engine.execute(zscore).fetchall())
# 		z = list(map(lambda x:x[0], z))
# 		L[row_name] = z
		
	
# 	return {"L":L}

@app.route('/turk', methods=['GET','POST'])
def turk():
	return {"data":[2.2,4.5, 7.8, 5.6, 4.3, 2.1, 4.7]}


if __name__ == "__main__":
	app.run(debug=True)



