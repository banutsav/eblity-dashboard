import pandas as pd
import dbmodules as dm
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots

# Create a short text for the hover info
def shortenText(words):
	l = len(words)
	# Less than 5 strings, concatenate and return
	if l<=5:
		return('<br>'.join(words))
	text = ''
	# More than 5 strings
	for i in range(5):
		text = text + '<br>' + words[i]
	text = text + '<br>' + '...and ' + str(l-5) + ' more'
	return text

# Stacked bar distribution of topics pending completion
def stackedBarPendingTopics(connection):
	df = dm.studentPendingTopics(connection)
	topics = df['topic_name'].unique()
	# Counts of sub-topics under each category
	nscount = []; pendcount = []; compcount = []
	# Hover text
	nshover = []; pendhover = []; comphover = []
	# Construct list of sub topics by their completion status
	for topic in topics:
		# Get sub topics of status = completed, pending and not-started
		ns = df.loc[(df['topic_name']==topic)&(df['subtopic_progress']==0)]['subtopic_name'].unique().tolist()
		pend = df.loc[(df['topic_name']==topic)&(df['subtopic_progress']>0)&(df['subtopic_progress']<100)]['subtopic_name'].unique().tolist()
		comp = df.loc[(df['topic_name']==topic)&(df['subtopic_progress']==100)]['subtopic_name'].unique().tolist()
		nscount.append(len(ns)); pendcount.append(len(pend)); compcount.append(len(comp))
		nshover.append(shortenText(ns)); pendhover.append(shortenText(pend)); comphover.append(shortenText(comp))

	# Create stacked bar
	fig = go.Figure(data=[
    	go.Bar(name='Completed', x=topics, y=compcount, marker_color='lightgreen', hovertext=comphover, hoverinfo='text'),
    	go.Bar(name='In-Progress', x=topics, y=pendcount, marker_color='lightblue', hovertext=pendhover, hoverinfo='text'),
    	go.Bar(name='Not Started', x=topics, y=nscount, marker_color='lightsalmon', hovertext=nshover, hoverinfo='text')
	])

	# Change the bar mode
	fig.update_layout(title='In-Progress Topics with Sub-Topics', barmode='stack')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

# Bar and Donut distribution of topics completed and not completed
def barTopicProgress(connection):
	df = dm.studentTopicProgress(connection)
	fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]])
	# Break topics into categories
	topicstatus = ['Not Started', 'In-Progress', 'Completed']
	ns = df.loc[df['topic_progress']==0]['topic_name'].tolist()
	pend = df.loc[(df['topic_progress']>0)&(df['topic_progress']<100)]['topic_name'].tolist()
	comp = df.loc[df['topic_progress']==100]['topic_name'].tolist()
	
	# Create hover text
	hover_text = [shortenText(ns), shortenText(pend), shortenText(comp)]

	# Bar graph of topic counts in the categories
	fig.add_trace(go.Bar(x=topicstatus, 
		y=[len(ns), len(pend), len(comp)],
		marker_color=['lightsalmon', 'lightblue', 'lightgreen']
	#	, hovertext=hover_text, hoverinfo='text'
		), row=1, col=1)
	fig.add_trace(go.Pie(labels=topicstatus, values=[len(ns), len(pend), len(comp)], 
		marker_colors=['lightsalmon', 'lightblue', 'lightgreen'],hole=.3), row=1, col=2)
	
	# Set title and hover
	fig.update(layout_title_text='Topics', layout_showlegend=False)
	fig.update_traces(hovertext=hover_text, hoverinfo='text')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

# Scatter plot with topic progress for a student
def scatterTopicProgress(connection):
	df = dm.studentTopicProgressMonth(connection)
	# Create scatter marker colors and hovertext
	colors = []; hover_text = []
	for index, row in df.iterrows():
		info = row['topic_name']
		if row['topic_progress']==100:
			colors.append('lightgreen'); info += '<br>Completed' 
		elif row['topic_progress']==0:
			colors.append('lightsalmon'); info += '<br>Not Started<br>Requires ' + str(row['hours']) + ' hours'
		else:
			colors.append('lightblue'); info += '<br>' + str(row['topic_progress']) + '% completed'
		hover_text.append(info)

	# Plotly Scatter
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df['sequence'], y=df['month'], 
		hovertext=hover_text, hoverinfo='text',
		mode='lines+markers', name='Mathematics',
		marker=dict(size=df['hours']*10, color=colors),
		))
	fig.update_layout(title='Student Progress Calendar')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

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
	fig.add_trace(go.Scatter(x=df['sequence'], y=df['month'], 
		hovertext=hover_text, hoverinfo='text',
		mode='lines+markers', name='Mathematics',
		marker=dict(size=df['hours']*10, color=df['no_sub_topics']),
		))
	fig.update_layout(title='Mathematics Grade 8')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot