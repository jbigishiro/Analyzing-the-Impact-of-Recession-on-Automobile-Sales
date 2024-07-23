# Create Dashboard using Plotly and Dash

import pandas as pd
from dash import Input, Output, State, Dash, dcc, html
import plotly.graph_objects as go
import plotly.express as px

#Create app
app = Dash(__name__)

# Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year
#Layout Section of Dash


#Task 1 Add the Title to the Dashboard
app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24})]

# TASK 2: Add drop-down menus to your dashboard with appropriate titles and options
                        html.Div([
                            dcc.Dropdown(id='dropdown-statistics', 
                                options=[
                                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'}
                                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                                        ],
                                    placeholder='Select a report type', value = 'Select Statistics'
                                style={'width': '80%', 'padding': '3px',
                                'text-align-last':'center'})
                        

                            dcc.Dropdown(id='select-year', 
                                options=[{'label': i, 'value': i} for i in year_list], value='Select-year'
                                placeholder='Select-year'
                               )

        ])
    #outer division ends

])

#Place to add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')])
#TASK 5: Add the callback function.   
#Place to define the callback function .
def reg_year_display(input_region,input_year):  
    #data
   region_data = df[df['Region'] == input_region]
   y_r_data = region_data[region_data['Year']==input_year]
    #Plot one - Monthly Average Estimated Fire Area   
   est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
   fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month', title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))   
     #Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
   veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
   fig2 = px.bar(veg_data, x='Month', y='Count', title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))    
   return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2) ]
if __name__ == '__main__':
    app.run_server()
    