import random
import numpy as np
import colorsys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots
import colorlover as cl
import dbmodules as dm

# Construct a list of unique colors to be used for plotting
def getUniqueColors(num_colors):
    if num_colors<=8:
    	colorset = cl.scales['8']['qual']['Set2']
    	#random.shuffle(colorset)
    	unqcolors = colorset[:num_colors]
    	return list(unqcolors)
    # More then 8 colors needed
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return list(colors)

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
	
# Scatter plot of sub-topic details for a completed topic
def scatterCompletedTopics(connection, username, topic):
	df = dm.completedTopicDetails(connection, username, topic)
	subtopics = list(df['sub_sub_topic'].unique())
	# Create hovertext and colors
	hovertext = []; colors = []
	for index, row in df.iterrows():
		hovertext.append('<b>'+row['sub_sub_topic']+'</b><br>Objective: '+row['BLTO']
			+'<br>Difficulty Level: '+row['difficulty_level']
			+'<br>Time Spent: '+str(round(row['timespent']/60,2))+' mins<br>Attempts: '
			+str(row['attempts'])+'<br>Errors: '+str(row['errors']))
		if row['score']>5 and row['timespent']>400:
			colors.append('lightsalmon')
		else:
			colors.append('lightgreen') 
	# Plotly Scatter
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df.index, y=df['timespent'], 
		hovertext=hovertext, hoverinfo='text', 
		mode='lines+markers', name=topic,
		marker=dict(size=df['score']*10, color=colors)
		))
	fig.update_layout(title=topic)
	fig.update_xaxes(showticklabels=False, title=str(df.shape[0])+' sub-topics')
	fig.update_yaxes(showticklabels=False)
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

# Stacked bar distribution of topics pending completion
def stackedBarPendingTopics(connection, studentid, subject):
	df = dm.studentPendingTopics(connection, studentid, subject)
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
def barTopicProgress(connection, studentid, subject):
	df = dm.studentTopicProgress(connection, studentid, subject)
	fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]])
	# Break topics into categories
	topicstatus = ['Not Started', 'In-Progress', 'Completed']
	ns = df.loc[df['topic_progress']==0]['topic_name'].tolist()
	pend = df.loc[(df['topic_progress']>0)&(df['topic_progress']<100)]['topic_name'].tolist()
	comp = df.loc[df['topic_progress']==100]['topic_name'].tolist()
	
	# Create hover text
	hover_text = [shortenText(ns), shortenText(pend), shortenText(comp)]

	# Bar graph of topic counts in the categories
	fig.add_trace(go.Bar(x=topicstatus, y=[len(ns), len(pend), len(comp)],
		hovertext=hover_text, hoverinfo='text',
		marker_color=['lightsalmon', 'lightblue', 'lightgreen']), row=1, col=1)
	fig.add_trace(go.Pie(labels=topicstatus, values=[len(ns), len(pend), len(comp)],
		hovertext=hover_text, hoverinfo='text',
		marker_colors=['lightsalmon', 'lightblue', 'lightgreen'],hole=.3), row=1, col=2)
	
	fig.update_layout(go.Layout(title='Topics',showlegend=False,
		xaxis=dict(fixedrange=True),yaxis=dict(fixedrange=True)))
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False, config={'displayModeBar':False})
	return plot
	
# Scatter plot with topic progress for a student
def scatterTopicProgress(connection, studentid, subject):
	df = dm.studentTopicProgressMonth(connection, studentid, subject)
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

# Distribution of topic and sub topics across months for a subject
def scatterTopicSubTopics(connection, grade, subject):
	df = dm.topicWithSubTopics(connection, grade, subject)
	
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
	fig.update_layout(title=subject+' grade ' + str(grade))
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot