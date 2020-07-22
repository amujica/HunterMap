# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#Colors displayed

colors = ["#5DA5DA","#FAA43A","#60BD68","#F15854","#DECF3F", "#F17CB0", "#B276B2", "#B2912F"]
colors_pie = ["#60BD68","#F15854","#5DA5DA","#FAA43A","#DECF3F", "#F17CB0", "#B276B2", "#B2912F"]

#Loading data

def read_file(csv_path):
    return pd.read_csv(csv_path, sep=";", decimal=",")

hunted= read_file("https://raw.githubusercontent.com/amujica/HunterMap/master/hunted.csv")
missed= read_file("https://raw.githubusercontent.com/amujica/HunterMap/master/missed.csv")


#Graphs without selectors


mapbox_access_token = "pk.eyJ1Ijoic2FyYXNhdGFjbyIsImEiOiJja2NvemZnc3YwcTJoMnVxeWhld2h3M3EwIn0.JSHwpw20nEmiuvs_UzF9UA"
px.set_mapbox_access_token(mapbox_access_token)


#Merge both dataframes
trues = ["hunted"]*len(hunted)
sizes= hunted["Points"].tolist()
sizes = [2*x for x in sizes]
hunted["Type"] = trues
hunted["Size"] = sizes

falses = ["missed"]*len(missed)
sizes= [12]*len(missed)
missed["Type"] = falses
missed["Size"] = sizes

result = hunted.append(missed, sort=False,ignore_index=True ) 


#Map layout

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=40, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10)),
    #title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="outdoors",
        center=dict(lon=hunted["Longitude"].mean(), lat=hunted["Latitude"].mean()),
        zoom=12,
    ),
)



#Markdown

markdown_text = '''
Designed by [Alberto Mujica](https://amujica.github.io/)

'''

#Some calculations for the controls

def delete_nan(list_of_dicts):
    for index, items in enumerate(list_of_dicts):
        for key, value in items.items():
                if value == "nan":
                    del list_of_dicts[index]
                    break

hunter_options = [
    {"label": str(hunter), "value": str(hunter)}
    for hunter in hunted["Hunter"].unique() 
]


for hunter in missed["Hunter"].unique():
    if hunter not in hunted["Hunter"].unique():
        hunter_options.append({"label": str(hunter), "value": str(hunter)})



cb_hunter_options = list(hunted["Hunter"].unique())

for hunter in missed["Hunter"].unique():
    if hunter not in cb_hunter_options:
        cb_hunter_options.append(hunter)

delete_nan(hunter_options)


season_options = [
    {"label": str(season), "value": str(season)}
    for season in hunted["Season"].unique()
]

for season in missed["Season"].unique():
    if season not in hunted["Season"].unique():
        season_options.append({"label": str(season), "value": str(season)})

delete_nan(season_options)

cb_season_options = list(hunted["Season"].unique())

for season in missed["Season"].unique():
    if season not in cb_season_options:
        cb_season_options.append(season)

appr_options = [
    {"label": str(appr), "value": str(appr)}
    for appr in hunted["Approach"].unique()
]

cb_appr_options = list(hunted["Approach"].unique())

delete_nan(appr_options)


#Layout

app.title = 'HunterMap'

app.layout = dbc.Container(
     
    [
        html.Div([
            html.H1(
                "HunterMap",
                style={"text-align" :"center"},
                ),

                ],
        
        ),
        
        dcc.Markdown(children=markdown_text,
        style={"text-align" :"center"},
        ),

#CONTROLS AND MAP
        dbc.Row(
            [
            
            #Controls
                dbc.Col(
                    [
                        dbc.Container([
                        dbc.Row(
                            [
                                dbc.Col([  
                                   dcc.RadioItems(
                                        id="checklist_maptype",
                                        options=[
                                            {'label': 'Satellite', 'value': 'satellite'},
                                            {'label': 'Outdoors', 'value': 'outdoors'},
                                        ],
                                        value="outdoors",
                                        labelStyle={"border-bottom":"1px solid lightgray"},
                                        inputStyle={"margin": "10px"},
                                        className="dcc_control",
                                       
                                    ),
                                
                                   
                                    ],  
                                    
                                ),
                            ],
                            style={"text-align": "center"},
                            
                            ),

                        dbc.Row(
                            [
                                dbc.Col([ 
                                   dcc.Checklist(
                                        options=[
                                            {'label': 'Hunted', 'value': 'hunted'},
                                            {'label': 'Missed', 'value': 'missed'},
                                        ],
                                        value=['hunted', 'missed'],
                                        inputStyle={"margin": "10px"},
                                        labelStyle={"border-bottom":"1px solid lightgray"},
                                        className="dcc_control",
                                        id="checklist_hm"
                                    ),
                                    ],  
                                    
                                ),
                            ],
                            style={"text-align": "center"},
                            
                            ),

                        dbc.Row(
                            [
                                dbc.Col([
                                    html.P(html.Strong("Filter by points"), className="control-label"),
                                    dcc.RangeSlider(
                                        min=0,
                                        max=10,
                                        marks={i: '{}'.format(i) for i in range(11)},
                                        value=[0,10],
                                        id="slider_points"
                                        
                                                    )  

                                ]
                                    
                                ),
                            ],
                            className="row-controls",
                            ),
                        dbc.Row(
                            [
                                dbc.Col([
                                    html.Span(html.Strong("Filter by hunter"), className="control-label"),
                                    dcc.RadioItems(
                                        id="hunter_radio",
                                        options=[
                                            {"label": "All ", "value": "all"},
                                            {"label": "Customize ", "value": "custom"},
                                        ],
                                        value="all",
                                        labelStyle={"display": "inline-block"},
                                        className="dcc_control",
                                        inputStyle={"margin": "5px"},
                                    ),
                                    dcc.Dropdown(
                                       
                                        value=list(hunter_options[0].keys()),
                                        options=hunter_options,
                                        multi=True,
                                        className="dcc_control",
                                        style={"margin":"0"},
                                        id="dropdown_hunters",
                                    
                                    )  

                                ]
                                   
                                    
                                ),
                            ],
                            className="row-controls",
                            ),
                        dbc.Row(
                            [
                                dbc.Col([
                                    html.Span(html.Strong("Filter by season"), className="control-label"),
                                    dcc.RadioItems(
                                        id="season_radio",
                                        options=[
                                            {"label": "All ", "value": "all"},
                                            {"label": "Customize ", "value": "custom"},
                                        ],
                                        value="all",
                                        labelStyle={"display": "inline-block"},
                                        className="dcc_control",
                                        inputStyle={"margin": "5px"},
                                    ),
                                    dcc.Dropdown(
                                        id="dropdown_seasons",
                                        value=list(season_options[0].keys()),
                                        options=season_options,
                                        multi=True,
                                        className="dcc_control",
                                    )  

                                ]
                                   
                                    
                                ),
                            ],
                            className="row-controls",
                            ),

                        dbc.Row(
                            [
                                dbc.Col([
                                    html.Span(html.Strong("Filter by approach"), className="control-label"),
                                    dcc.RadioItems(
                                        id="appr_radio",
                                        options=[
                                            {"label": "All ", "value": "all"},
                                            {"label": "Customize ", "value": "custom"},
                                        ],
                                        value="all",
                                        labelStyle={"display": "inline-block"},
                                        className="dcc_control",
                                        inputStyle={"margin": "5px"},
                                    ),
                                    dcc.Dropdown(
                                        id="dropdown_approaches",
                                        value=list(appr_options[0].keys()),
                                        options=appr_options,
                                        multi=True,
                                        className="dcc_control",
                                        
                                    ),
                                    

                                ]
                                   
                                    
                                ),
                            ],
                            
                            className="row-controls",
                            ),
                        
                        dbc.Row(
                            [
                                dbc.Col([
                                    html.Span(html.Strong("Color of points"), className="control-label", ),
                                    dcc.Dropdown(
                                        options=[
                                            {'label': 'Hunted/Missed', 'value': 'hunted-missed'},
                                            {'label': 'Season', 'value': 'season'},
                                            {'label': 'Hunter', 'value': 'hunter'},
                                            {'label': 'Approach', 'value': 'approach'}
                                        ],
                                        value='hunted-missed',
                                        id="dropdown_colorofpoints",
                                    )  

                                ],
                                style={"margin-bottom":"10px","border-top":"1px solid lightgray"}, 
                                   
                                    
                                ),
                            ],
                           
                            ),

                            
                                

                        ],    
                        ),
                        
                         
                    ],
                    
                    
                    width=3,
                    id="col-filters",
                    align="center",
                    className="pretty_container",
                    
                ),
            #Map
                dbc.Col(
                    
                        children=[
                            
                                dcc.Graph(
                                id='map',
                                #figure=fig,
                                style={"height":"100%", "width":"100%"},
                        
                    
                    
                    )
                            ],
                    
                   className="pretty_container",
                ),
            ],

            className="row",
            justify="center",
        ),

#GRAPHS
        dbc.Row(
            [

            #Stats
                dbc.Col([

                        dbc.Container([
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6(id="num_deers_text"), html.P("No. of Deers hunted")],
                                    id="num_deers",
                                    className="mini_container",
                                    
                                ),
                            ],
                            style={"text-align": "center"},
                            
                            ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6(id="num_seasons_text"), html.P("No. of Seasons")],
                                    id="num_seasons",
                                    className="mini_container",
                                ),
                            ],
                            style={"text-align": "center"},
                            ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6(id="mean_points_text"), html.P("Mean Points")],
                                    id="mean_points",
                                    className="mini_container",
                                    
                                    
                                ),
                            ],
                            style={"text-align": "center"},
                            ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6(id="common_appr_text"), html.P("Most common approach")],
                                    id="common_appr",
                                    className="mini_container",
                                ),
                            ],
                            style={"text-align": "center"},
                            ),
                                

                        ],    
                        ),
                        
                         
                    ],
                    

             
                className="container_stats",
                width=2,
                ),


            #Pie chart
                dbc.Col(
                    dcc.Loading(
                        children=[dcc.Graph(
                        id='pie-chart',
                        #figure=pie_chart,
                       
                    ),],
                    
                    ),
                    className="pretty_container",
                    width=4,
                    
                ),

            #Graph+selector
                dbc.Col(
                    dbc.Container([

                    #Selector
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='bar_selector',
                                       options=[
                                            {'label': 'Points', 'value': 'points'},
                                            {'label': 'Approach', 'value': 'approach'},
                                            {'label': 'Hunter', 'value': 'hunter'},
                                            {'label': 'Season', 'value': 'season'}
                                        ],
                                        value='hunter',
                                        style={"margin-top":"8px"},
                                    ),

                                    
                                ),
                            ],
                            
                            #className="h-25",
                        ),
                        dbc.Row(

                        #Bar graph
                            [
                                dbc.Col(
                                    dcc.Loading(
                                        children=[
                                            dcc.Graph(
                                            id='bar-plot',
                                    
                                    ),
                                        ],
                                        
                                    )
                                    
                                    
                                ),
                                
                            ],
                            #className="h-75",
                        ),
                         
                    ],
                    #style={"height": "30vh"},
                    ),
                    className="pretty_container",
                    width=4,
                ),
                
            ],
            #className="h-25",
            justify="around",
            
        ),
        
    ],
    style={"height": "95%", "width": "95%"},
    fluid=True,
)

#Callbacks
 
#BAR GRAPH

@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    [Input(component_id='bar_selector', component_property='value')]
)
def update_figure(selector):

    if 'season' in selector:
        hunted_season =  hunted.groupby(by='Season')['Points'].count().sort_values(ascending=False).to_frame(name = 'Hunted Deers').reset_index()
        fig = px.bar(hunted_season, x="Season", y="Hunted Deers",  color="Season",color_discrete_sequence=colors)
        #fig.update_layout(legend=dict(orientation="h", xanchor="center", y=-9 ,x= 0))

    if 'points' in selector:
        hunted_points =  hunted.groupby(by='Points')['Points'].count().sort_values(ascending=False).to_frame(name = 'Hunted Deers').reset_index()
        fig = px.bar(hunted_points, x="Points", y="Hunted Deers", color="Points",color_discrete_sequence=colors)
        #fig.update_layout(legend=dict(orientation="h",))
    if 'approach' in selector:
        hunted_approach =  hunted.groupby(by='Approach')['Points'].count().sort_values(ascending=False).to_frame(name = 'Hunted Deers').reset_index()
        fig = px.bar(hunted_approach, x="Approach", y="Hunted Deers",  color="Approach",color_discrete_sequence=colors)
        #fig.update_layout(legend=dict(orientation="h",))
    if 'hunter' in selector:
        hunted_hunter =  hunted.groupby(by='Hunter')['Points'].count().sort_values(ascending=False).to_frame(name = 'Hunted Deers').reset_index()
        fig = px.bar(hunted_hunter, x="Hunter", y="Hunted Deers",  color="Hunter",color_discrete_sequence=colors)
        #fig.update_layout(legend=dict(orientation="h",))

    fig.update_layout(title_text="Hunted Deers by {}".format(selector))
    

    return fig


#STAT 1 
# Selectors -> stat1
@app.callback(
    Output("num_deers_text", "children"),
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_approaches", "value"),
        Input("dropdown_seasons", "value"),
    ],
)
def update_num_deers_text(slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons):

    dff = filter_dataframe(hunted, slider_points, dropdown_hunters ,dropdown_approaches,dropdown_seasons)
    
    return str(len(dff))

#id="num_seasons_text",len(hunted['Season'].unique())

#STAT 2
# Selectors -> stat2
@app.callback(
    Output("num_seasons_text", "children"),
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_approaches", "value"),
        Input("dropdown_seasons", "value"),
    ],
)
def update_num_seasons_text(slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons):

    dff = filter_dataframe(hunted, slider_points, dropdown_hunters ,dropdown_approaches,dropdown_seasons)
    return str(len(dff['Season'].unique()))

#STAT 3
# Selectors -> stat3
@app.callback(
    Output("mean_points_text", "children"),
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_approaches", "value"),
        Input("dropdown_seasons", "value"),
    ],
)
def update_num_seasons_text(slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons):

    dff = filter_dataframe(hunted, slider_points, dropdown_hunters ,dropdown_approaches,dropdown_seasons)
    mean = dff['Points'].mean()
    if np.isnan(mean):
        return "Select a point"
    return round(dff['Points'].mean(),2)

#STAT 4
# Selectors -> stat4
@app.callback(
    Output("common_appr_text", "children"),
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_approaches", "value"),
        Input("dropdown_seasons", "value"),
    ],
)
def update_num_seasons_text(slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons):

    dff = filter_dataframe(hunted, slider_points, dropdown_hunters ,dropdown_approaches,dropdown_seasons)
    if len(dff['Approach'].value_counts()) == 0:
        return "Select a point"
    return dff['Approach'].value_counts()[0:1].index.tolist()[0]


#Pie chart
# Selectors -> pie chart
@app.callback(
    Output("pie-chart", "figure"),
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_seasons", "value"),
    ],
)
def update_pie(slider_points, dropdown_hunters,dropdown_seasons):

    dff_hunted = filter_dataframe_notappr(hunted, slider_points, dropdown_hunters ,dropdown_seasons)
    dff_missed = filter_dataframe_missed(missed, dropdown_hunters ,dropdown_seasons)

    new_data={
    'hunted-missed':["Hunted", "Missed"],
    'Number':[len(dff_hunted), len(dff_missed)],
    }
    pie_df = pd.DataFrame.from_dict(new_data)
    pie_chart = px.pie(
        data_frame= pie_df,
        values='Number',
        names='hunted-missed',
        color='hunted-missed',
        color_discrete_sequence=colors_pie,
        labels={"hunted-missed":"Type"},
        hole=0.5,
        title="Hunted vs Missed",


    )

    return pie_chart


# Radio -> multi_hunters
@app.callback(
    Output("dropdown_hunters", "value"), [Input("hunter_radio", "value")]
)
def display_status(selector):
    if selector == "all":
        return cb_hunter_options
    return []

# Radio -> multi_seasons
@app.callback(
    Output("dropdown_seasons", "value"), [Input("season_radio", "value")]
)
def display_status(selector):
    if selector == "all":
        return cb_season_options
    return []

# Radio -> multi_approaches
@app.callback(
    Output("dropdown_approaches", "value"), [Input("appr_radio", "value")]
)
def display_status(selector):
    if selector == "all":
        return cb_appr_options
    return []


# controls -> map
@app.callback(
    Output("map", "figure"), 
    [
        Input("slider_points", "value"),
        Input("dropdown_hunters", "value"),
        Input("dropdown_approaches", "value"),
        Input("dropdown_seasons", "value"),
        Input("checklist_hm", "value"),
        Input("checklist_maptype", "value"),
        Input("dropdown_colorofpoints", "value"),
        
    ],

)

def change_map(slider_points,dropdown_hunters,dropdown_approaches,dropdown_seasons,checklist_hm,checklist_maptype,dropdown_colorofpoints):
    missed_f = filter_dataframe_missed(missed, dropdown_hunters,dropdown_seasons)
    hunted_f = filter_dataframe(hunted, slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons)
    result_f = filter_dataframe_result(result, slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons, checklist_hm)
    
    traces = []

    
    if checklist_maptype=="outdoors":
        layout["mapbox"]["style"] = "outdoors"
        

    if checklist_maptype=="satellite":
        layout["mapbox"]["style"] = "satellite"
        

        if "hunted" in checklist_hm:
            trace = dict(
                type="scattermapbox",
                        lon=hunted_f["Longitude"],
                        lat=hunted_f["Latitude"],
                        text="Hunter: " + hunted_f["Hunter"] 
                        +  " | Season: " + hunted_f["Season"] 
                        +  " | Date: " + hunted_f["Date"]
                        +  " | Points: " + hunted_f["Points"].apply(str) 
                        +  " | Approach: " + hunted_f["Approach"], #Poner mas info
                        marker=dict(size=2.5*hunted_f["Points"], opacity=1, color="white"),
                        name="",
                    )
            traces.append(trace)

        if "missed" in checklist_hm:
            trace = dict(
                type="scattermapbox",
                        lon=missed_f["Longitude"],
                        lat=missed_f["Latitude"],
                        text="Hunter: " + missed_f["Hunter"] 
                        +  " | Season: " + missed_f["Season"], #Poner mas info
                        marker=dict(size=16, opacity=1, color="white"),
                        name="",
                    )
            traces.append(trace)
    

    if dropdown_colorofpoints == "hunted-missed":
        types = list(hunted_f["Type"].unique())
        for type_of in missed_f["Type"].unique():
            if type_of not in types:
                types.append(type_of)

        
        colors_asigned = dict(zip(types, colors_pie))

        
        for type_of in types:
                
                result_ff = result_f[result_f["Type"]==type_of]
                    
                if len(result_ff) > 0:

                    test = transform_text(result_f, type_of, "Type")
                           
                    trace = dict(
                            type="scattermapbox",
                            lon=result_ff["Longitude"],
                            lat=result_ff["Latitude"],
                            text=test,
                            marker=dict(size=result_ff["Size"], opacity=0.8, color=colors_asigned.get(type_of)),
                            name=type_of,
                        )
                    traces.append(trace)

                
        if 'missed' in checklist_hm:
            trace = generate_trace_x(missed_f)
            traces.append(trace)   

        #Other way of doing it:
        '''
        if "hunted" in checklist_hm:
           
            trace = dict(
                type="scattermapbox",
                        lon=hunted_f["Longitude"],
                        lat=hunted_f["Latitude"],
                        text="Hunter: " + hunted_f["Hunter"] 
                        +  " | Season: " + hunted_f["Season"] 
                        +  " | Date: " + hunted_f["Date"]
                        +  " | Points: " + hunted_f["Points"].apply(str) 
                        +  " | Approach: " + hunted_f["Approach"]
                        , #Poner mas info
                        marker=dict(size=2*hunted_f["Points"], opacity=1, color = "#60BD68"),
                        name="Hunted",
                    )
            traces.append(trace)

        if "missed" in checklist_hm:
            trace = dict(
                type="scattermapbox",
                        lon=missed_f["Longitude"],
                        lat=missed_f["Latitude"],
                        text="Hunter: " + hunted_f["Hunter"] 
                        +  " | Season: " + hunted_f["Season"], 
                        marker=dict(size=12, opacity=0.5, color = "red"),
                        name="Missed",
                    )
            traces.append(trace)

            trace = generate_trace_x(missed_f)
            traces.append(trace)
        '''
    
    elif dropdown_colorofpoints == "hunter":

        hunters = list(hunted_f["Hunter"].unique())
        for hunter in missed_f["Hunter"].unique():
            if hunter not in hunters:
                hunters.append(hunter)

        
        colors_asigned = dict(zip(hunters, colors))

        
        for hunter in hunters:
                
                result_ff = result_f[result_f["Hunter"]==hunter]
                    
                if len(result_ff) > 0:

                    test = transform_text(result_f, hunter, "Hunter")
                           
                    trace = dict(
                            type="scattermapbox",
                            lon=result_ff["Longitude"],
                            lat=result_ff["Latitude"],
                            text=test,
                            marker=dict(size=result_ff["Size"], opacity=1, color=colors_asigned.get(hunter)),
                            name=hunter,
                        )
                    traces.append(trace)

                
        if 'missed' in checklist_hm:
            trace = generate_trace_x(missed_f)
            traces.append(trace)        
    
    elif dropdown_colorofpoints == "season":
        seasons = list(hunted_f["Season"].unique())
        for season in missed_f["Season"].unique():
            if season not in seasons:
                seasons.append(season)

        
        colors_asigned = dict(zip(seasons, colors))

        
        for season in seasons:
                
                result_ff = result_f[result_f["Season"]==season]

                    
                if len(result_ff) > 0:
                    test = transform_text(result_f, season, "Season")

                    trace = dict(
                            type="scattermapbox",
                            lon=result_ff["Longitude"],
                            lat=result_ff["Latitude"],
                            text=test, 
                            marker=dict(size=result_ff["Size"], opacity=1, color=colors_asigned.get(season)),
                            name=season,
                        )
                    
                    traces.append(trace)

                
        if 'missed' in checklist_hm:
            trace = generate_trace_x(missed_f)
            traces.append(trace)       

    elif dropdown_colorofpoints == "approach":
        approaches = list(hunted_f["Approach"].unique())
        
        colors_asigned = dict(zip(approaches, colors))

        for appr in approaches:

                result_ff = result_f[result_f["Approach"]==appr]

                    
                if len(result_ff) > 0:

                    test = transform_text(result_f, appr, "Approach")
                    
                    trace = dict(
                            type="scattermapbox",
                            lon=result_ff["Longitude"],
                            lat=result_ff["Latitude"],
                            text=test,
                            marker=dict(size=result_ff["Size"], opacity=1, color=colors_asigned.get(appr)),
                            name=appr,
                        )
                    traces.append(trace)

                
        if 'missed' in checklist_hm:
            trace = generate_trace_x(missed_f)
            traces.append(trace)        

    fig = dict(data=traces, layout=layout)    
    return fig
    


#Private functions

def filter_dataframe(df, slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons):
    dff = df[
        (df["Points"] >= slider_points[0])
        & (df["Points"] <= slider_points[1])
        & df['Hunter'].isin(dropdown_hunters)
        & df['Season'].isin(dropdown_seasons)
        & df['Approach'].isin(dropdown_approaches)

    ]
    return dff

def filter_dataframe_notappr(df, slider_points, dropdown_hunters,dropdown_seasons):
    dff = df[
        (df["Points"] >= slider_points[0])
        & (df["Points"] <= slider_points[1])
        & df['Hunter'].isin(dropdown_hunters)
        & df['Season'].isin(dropdown_seasons)
        

    ]
    return dff

def filter_dataframe_missed(df, dropdown_hunters,dropdown_seasons):
    dff = df[
         df['Hunter'].isin(dropdown_hunters)
        & df['Season'].isin(dropdown_seasons)
        

    ]
    return dff
def filter_dataframe_result(df, slider_points, dropdown_hunters,dropdown_approaches,dropdown_seasons, checklist_hm):

    if len(checklist_hm) == 0:
        return df
    
    if (len(checklist_hm) < 2):
        df = df[df["Type"]==checklist_hm[0]]        
        
    df = df[
         df['Hunter'].isin(dropdown_hunters)
        & df['Season'].isin(dropdown_seasons)
    ]
    
    for index, row in df.iterrows():
        if row['Type'] == 'hunted':
            
            if (row['Points']>slider_points[1]) or (row['Points']<slider_points[0]) or (row['Approach'] not in dropdown_approaches) :
                df.drop(index, inplace=True) 
        
    return df


def generate_trace_x(df):
     return dict(
                type="scattermapbox",
                        lon=df["Longitude"],
                        lat=df["Latitude"],
                        marker=dict(size=15, opacity=1),
                        name="",
                        mode="text", 
                        text="X",
                        
                    )

def transform_text(df,list_item,column_name):
    result_f = df[df[column_name]==list_item]
    test= result_f["Type"] + " * " + "Hunter: " + result_f["Hunter"] +  " | Season: " + result_f["Season"]  

    for index, value in test.items():
        if "hunted" in value:
            test[index] = test[index] + " | Date: " + result_f["Date"][index]+  " | Points: " + str(result_f["Points"][index]) +  " | Approach: " + result_f["Approach"][index]
            test[index] = test[index].split('*')[1].lstrip()
        else:
            test[index] = test[index].split('*')[1].lstrip()
            
    return test




if __name__ == '__main__':
    app.run_server(debug=True)


    