import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline

offline.init_notebook_mode(connected=True)

# Read in data.
df = pd.read_csv("db_backup/top_100_hip_hop_.csv")


def grouped_artists():

    '''Returns a dictionary of the top artists grouped by year. Used to graph.'''

    # Return top 10 artists and how many times they were mentioned. 
    top_10 = pd.DataFrame(df['artist'].value_counts()[:10])

    # Save the top 10 artists to a list.
    top_artists = list(top_10.index)

    # Get top 10 artists' songs by checking against list of top_artists.
    all_by_top = df.loc[df['artist'].isin(top_artists)]

    # Group by artist,year and round their counts.
    grouped = pd.DataFrame(all_by_top.groupby(['artist','year'])['rank'].count())
    grouped['rank'] = round(grouped['rank'],2)

    # Unstack grouped dataframe and convert to dictionary while filling in NaNs with 0.
    new_df = grouped.unstack()
    dic = new_df.fillna(0).to_dict()

    return dic,top_artists

############### Plotting Parameter Functions ###############

def make_hover_over_text(artist,year):

    ''' Returns hover-over text for plotly time series.'''

    x = list(df[(df['artist']==artist)&(df['year']==year)]['song'])
    y = list(df[(df['artist']==artist)&(df['year']==year)]['rank'])
    
    if x:
        string = 'Songs: ' 
        for song,rank in zip(x,y):
            string+= f'''<br>{song} #{rank}'''
    else:
        return ''

    return string

def make_conditions(col_list):

    ''' Returns an array with lists of conditions for dropdown menus.'''
    
    # Make array full of False values with dimensions of input list.
    array = np.full(shape=(len(col_list),len(col_list)), fill_value=False, dtype=bool)
    
    for i in range(len(array)):
        array[i][i] = True

    return array

def make_buttons(top_artists,conditions):

    '''Returns button options for dropdown menus.'''

    buttons = []

    for artist,condition in zip(top_artists,conditions):
        dic = {'label':artist,
            'method':'restyle',
            'args':[{'visible': condition}]}
        buttons.append(dic)

    return buttons

############### Plotting Functions ###############
def plot_gen():
    ''' Generates 3D scatterplot based on Spotify song features '''
    data = []
    trace = go.Scatter3d(
    x=df['danceability'],
    y=df['energy'],
    z=df['loudness'],
    mode='markers',
    marker=dict(
        size=4,
        color="teal",
        line=dict(
            width=0.1),
        opacity=.8
    ),
    text=[f'Title: {song}<br>Artist: {artist}' for song,artist in zip(df['song'],df['artist'])])

    data.append(trace)

    layout = go.Layout(
        scene = dict(
            annotations=[
                dict(
                    x = 0.932,
                    y = 0.819,
                    z = -3.484,
                    ax = 0,
                    ay =-150,
                    text = "WTF by Missy Elliot/Pharrell<br>comes in as what<br>we consider a <br>club banger.",
                    arrowhead = 1,
                    xanchor = "auto",
                    yanchor = "top"),
                dict(
                    x=0.492,
                    y=0.26,
                    z=-17.341,
                    ax = 50,
                    ay = 0,
                    text = "Marvin's Room by Drake<br>comes in as the quietest,<br>least danceable.",
                    arrowhead = 1,
                    xanchor = "left",
                    yanchor = "bottom")
            ],
        aspectratio = dict(
        x = 1,
        y = 1,
        z = 1
        ),
        camera = dict(
        center = dict(
            x = 0,
            y = 0,
            z = 0
        ),
        eye = dict(
            x = 1.96903462608,
            y = -1.09022831971,
            z = 0.405345349304
        ),
        up = dict(
            x = 0,
            y = 0,
            z = 1
        )
        ),
        dragmode = "turntable",
        xaxis = dict(
        title = "Danceability"
        ),
        yaxis = dict(
        title = "Energy"
        ),
        zaxis = dict(
        title = "Loudness"
        ),
        ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )

    fig = go.Figure(data=data, layout=layout)

    return offline.plot(fig, include_plotlyjs=False, output_type='div')


def top_10_rappers_bar():

    '''Returns bar chart of the top 10 artists by count.'''

    top_10 = pd.DataFrame(df['artist'].value_counts()[:10])

    trace = go.Bar(
    x=top_10['artist'][::-1],
    y=top_10.index[::-1],
    orientation='h',
    marker=dict(
        color=top_10['artist'][::-1],
        colorscale='Greens',
        reversescale=True,
        line=dict(
            width=1.5
        )
    ),
    )

    layout = go.Layout(
        title="# of Times on Billboard Hot 100",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        # yaxis=dict(
        # tickfont=dict(
        #     size=12,
        #     color='black'
        # ))
    )

    fig = go.Figure(data=[trace],layout=layout)
    
    return offline.plot(fig, include_plotlyjs=False, output_type='div')


def top_10_rappers_line():

    data = []

    # Invoke grouped_artists() function to get data, and the list of the top artists.
    dic,top_artists = grouped_artists()

    conditions = make_conditions(top_artists)
    buttons = make_buttons(top_artists,conditions)

    # 2010-2018
    years = [k[1] for k in dic.keys()]

    # Loop through top_artists to make traces for plot.
    for artist in top_artists:
        # Number of songs on billboard hot 100.
        num_hits = [v[artist] for v in dic.values()]

        # Only display the first trace.
        if artist == top_artists[0]:
            visible = True
        else:
            visible = 'legendonly'

        trace = go.Scattergl(
            x=years,
            y=num_hits,
            mode='lines',
            name=artist,
            text = [make_hover_over_text(artist,year) for year in years],
            visible=visible
            )
        data.append(trace)


    updatemenus = list([
        dict(
            buttons=buttons,
            x = 1.2,
            xanchor = 'right',
            y = 1.2,
            yanchor = 'top',
            pad = {'l': 0, 't': 0.0},
            bgcolor = '#AAAAAA',
            showactive = False,
            bordercolor = '#FFFFFF',
            font = dict(size=11, color='#000000')
        )])    

    layout = go.Layout(
        updatemenus=updatemenus,
        showlegend=False,
        title="# of Unique Songs on the Hot 100 Rap Charts",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )


    fig = go.Figure(data=data, layout=layout)

    return offline.plot(fig, include_plotlyjs=False, output_type='div')

