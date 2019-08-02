import pandas as pd

# Student topic progress by month
def studentTopicProgressMonth(connection):
	qry = ('select distinct(p.topic_name), p.topic_progress, t.sequence, t.month, t.hours'
		' from eblitydb.eblity_plan_table p'
		' join eblitydb.eblity_topic_table t on (p.topic_id_id = t.topic_id)'
		' where p.subject=\'mathematics\' and p.student_id_id=10'
		' order by t.sequence'
		)
	df = pd.read_sql(qry, connection)
	return df

# Sub Topic status of Pending Topics
def studentPendingTopics(connection):
	qry = ('select topic_name, topic_progress, subtopic_name, subtopic_progress'
		' from eblitydb.eblity_plan_table'
		' where student_id_id=10 and subject=\'mathematics\''
		' and topic_progress<100 and topic_progress>0'
		' order by topic_progress'
		)
	df = pd.read_sql(qry, connection)
	return df

# Get topic and sub-topic progress for a student
def studentTopicProgress(connection):
	qry = ('select distinct(topic_name), topic_progress'
		' from eblitydb.eblity_plan_table'
		' where student_id_id=10 and subject=\'mathematics\''
		' order by topic_progress'
		)
	df = pd.read_sql(qry, connection)
	return df

# Get a list of sub topics for each topic of a specific grade
def topicWithSubTopics(connection):
	# Build query
	qry_topics = ('SELECT topic_id, sequence, topic_name, hours, month' 
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