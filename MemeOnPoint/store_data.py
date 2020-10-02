import pandas as pd
df = pd.read_csv('db.csv')

def store_to_db(id,path,tags):
	df.loc[id] = [id,path,tags]
	with open('db.csv', 'a') as f:
		     (df).to_csv(f, header=False)

def crawler():
	#The id to assign the new meme
	if(df.empty):
		id = 0
	else:
		id = df.tail(1)["ID"]+1


print(df.empty)

