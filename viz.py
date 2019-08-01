import pandas as pd
import dbmodules as dm
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy

# Distribution of topic and sub topics across months
def scatterTopicSubTopics(connection):
	df = dm.topicWithSubTopics(connection)
	
	# Create Hover Text - Topic Name + No. of Sub-Topics
	hover_text = []
	for index, row in df.iterrows():
		topictext = ' Sub-Topics' if row['no_sub_topics']>1 else ' Sub-Topic' 
		hover_text.append(
			'<b>' + str(row['topic_name']) + '</b><br>' 
			+ str(row['no_sub_topics'])
			+ topictext 
			+ '<br>'
			+ str(row['hours']) + ' hours'
			)

	# Plotly Scatter
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df['topic_id'], y=df['month'], 
		hovertext=hover_text, hoverinfo='text',
		mode='lines+markers', name='Mathematics',
		marker=dict(size=df['hours']*10, color=df['no_sub_topics']),
		))
	fig.update_layout(title='Mathematics Grade 8')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot