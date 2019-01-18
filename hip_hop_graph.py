
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline

offline.init_notebook_mode(connected=True)


# In[20]:
df = pd.read_csv("top_100_hip_hop_.csv")

def make_ranks():
    ''' Makes ranks for each artist according to year'''
    rank=[]

    # Create ranks for each artist.
    for year in sorted(list(set(df['year']))):
        rank+=[i+1 for i in range(len(df[df['year']==year]))]
    return rank


df['rank'] = make_ranks()

def grouped_artists():   
    top_10 = pd.DataFrame(df['artist'].value_counts()[:10])
    top_artists = list(top_10.index)

    # get all top 10 artist's songs:
    all_by_top = df.loc[df['artist'].isin(top_artists)]

    grouped = pd.DataFrame(all_by_top.groupby(['artist','year'])['rank'].count())
    grouped['rank'] = round(grouped['rank'],2)

    new_df = grouped.unstack()

    dic = new_df.fillna(0).to_dict()

    return dic,top_artists

def make_string(artist,year):
    x = list(df[(df['artist']==artist)&(df['year']==year)]['song'])
    y = list(df[(df['artist']==artist)&(df['year']==year)]['rank'])
    
    if x:
        s = 'Songs: ' 


        for song,rank in zip(x,y):
            s+= f'''<br>{song} #{rank}'''
    else:
        return ''
        
    return s

def make_conditions(col_list):
    
    ''' Returns an array with lists of conditions for dropdown menus.'''
    
    # Make array full of False values with dimensions of input list.
    array = np.full(shape=(len(col_list),len(col_list)), fill_value=False, dtype=bool)
    
    for i in range(len(array)):
        array[i][i] = True
    
    return array

def plot_gen():
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
        # title="Top Rap Songs of the Decade, by Audio Features",
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




def top_10_rappers():
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
    )

    fig = go.Figure(data=[trace],layout=layout)
    
    return offline.plot(fig, include_plotlyjs=False, output_type='div')





def make_top_rapper_chart():
    data = []
    buttons=[]


    dic,top_artists = grouped_artists()

    years = [k[1] for k in dic.keys()]
    conditions = make_conditions(top_artists)

    for artist in top_artists:
        num_hits = [v[artist] for v in dic.values()]

        trace = go.Scattergl(
            x=years,
            y=num_hits,
            mode='lines',
            name=artist,
            text = [make_string(artist,year) for year in years]
            )
        data.append(trace)

    for artist,condition in zip(top_artists,conditions):
        dic = {'label':artist,
            'method':'restyle',
            'args':[{'visible': condition}]}
        buttons.append(dic)

    updatemenus = list([
        dict(
            buttons=buttons,
            x = 1.2,
            xanchor = 'right',
            y = 1,
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
        title="# of Songs on the Hot 100 Rap Charts",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )


    fig = go.Figure(data=data, layout=layout)

#     offline.iplot(fig)
    return offline.plot(fig, include_plotlyjs=False, output_type='div')

