import pandas as pd

# Get a list of sub topics for each topic of a specific grade
def topicWithSubTopics(connection):
	# Build query
	qry_topics = ('SELECT topic_id, topic_name, hours, month' 
	' from eblitydb.eblity_topic_table' 
	' where grade=8 and subject=\'Mathematics\'')
	
	# Execute query
	df = pd.read_sql(qry_topics, connection)
	sub_topics = []
	no_sub_topics = []
	
	# Create dataframe of topic and sub-topics
	for index, row in df.iterrows():
		qry_sub = 'SELECT subtopic_name FROM eblitydb.eblity_subtopic_table where topic_id_id=' + str(row['topic_id'])
		df_sub = pd.read_sql(qry_sub, connection)
		subs = df_sub['subtopic_name'].unique().tolist()
		sub_topics.append(subs)
		no_sub_topics.append(len(subs))	
	df['sub_topics'] = sub_topics
	df['no_sub_topics'] = no_sub_topics
	
	return df