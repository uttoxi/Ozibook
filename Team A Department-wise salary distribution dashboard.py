#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from dash import Dash , dcc , html , Input , Output, State
import dash_bootstrap_components as dbc
import plotly.express as px


# In[2]:


app=Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


# In[3]:


df_dev=pd.read_excel(r"C:\Users\utkar\Downloads\Developers.xlsx",index_col=[0])
df_exec=pd.read_excel(r"C:\Users\utkar\Downloads\Executives.xlsx",index_col=[0])


# In[4]:


df_dev


# In[5]:


df_exec


# In[6]:


def compute_data_choice_1(df_exec):
    
    bar_data = df_exec
    pie_data= df_exec
    tree_data = df_exec
    return bar_data,tree_data, pie_data


# In[7]:


def compute_data_choice_2(df_dev):
   
    bar_data = df_dev
    pie_data= df_dev
    tree_data = df_dev
    return bar_data,tree_data, pie_data


# In[ ]:


exp_list= ['Salary/month/employee','Salary/month','Salary/year/employee','Salary/year']   #to give variable inputs 
 
app.layout = html.Div(children=[                                               #parent Division
    html.H1(' Ozibook Department wise Salary Expenditure',
            style={'text-align':'center',
                   'color':'#DE3163',
                   'font-size': 32}),
    html.H2('Executives & Developers Distribution',
            style={'text-align':'center',
                   'font-family':'verdana',
                   'text-color': 'cerise',
                   'font-size': 30}),
    html.H3('By Team-A',
            style={'text-align':'center',
                   'font-family':'verdana',
                   'text-color': 'cerise',
                   'font-size': 28}),
    html.Div([                                                        #Division for position dropdown                                  
      
        html.Div([
            html.Div([
                html.H2('Department:', style={
                    'margin-left': '1em','font-size':'20px'})
            ]
            ),
           
            dcc.Dropdown(id='ptype',
                         options=[
                             {'label': 'Executive',
                              'value': 'OPT1'},
                             {'label': 'Developer',
                              'value': 'OPT2'}
                         ],
                         placeholder='Select a report type',
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align': 'center'})
            
        ], style={'display': 'flex'}),

      
    html.Div([                                                     #division for report type dropdown
            
            html.Div(
                [
                    html.H2('Salary Type:', style={
                        'margin-left': '1em','font-size':'20px'})
                ]
            ),
            dcc.Dropdown(id='etype',
                        
                         options=[
                             {'label': i, 'value': i} for i in exp_list],
                         placeholder="Expense type",
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
           
        ], style={'display': 'flex'}),

    
    
    ]),
    
    
    
    
    html.Div([
        html.Div([], id='plot1',style={'border-style':'ridge','width':'50%'}), 
        html.Div([], id='plot2',style={'border-style':'ridge','width':'50%'})],
        style={'display': 'flex','border-style': 'ridge'}),                                    #Division for plots
    
    
    
    html.Div([html.Div([], id='plot3',style={'border-style':'ridge','width':'50%'}),   
 html.Div([
            html.H2('Yearly Salary of Departments'),
            html.H5('Calculate the salary spent per year on employees'),

            html.Br(),
            html.Br(),

            html.H4('Enter The Role: '),

            html.Br(),

            dcc.Dropdown(id='calc_dd', options=list(df_dev['Position']),
                         value=list([df_dev['Position']])[0], style={'width': '65%'}),
            
            html.Br(),
            html.Br(),

            html.H4('Enter the Number \n of Employees'),
            html.Br(),
            dcc.Input(id='calc_input', type="numbers", min=0, step=1, debounce=True, value=''),
            html.Br(),
            html.Br(),
            html.H4(id='calc_output')
        ])
        
                                                             
       ],style={'display':'flex','border-style': 'ridge'})                     #to put bottom rows plots and cal side by side

   

    ],style={'background-color':'powderblue'})                                 #for background color


@app.callback(
    [Output(component_id='plot1', component_property='children'),
                Output(component_id='plot2', component_property='children'),
                Output(component_id='plot3', component_property='children')],
               [Input(component_id='ptype', component_property='value'),
                Input(component_id='etype', component_property='value')],
               [State("plot1", 'children'), State("plot2", "children"),
                State("plot3", "children")])

def get_graph(chart, inp, c1,c2,c3):                                    #callback for graph           
      
        if chart == 'OPT1':
            bar_data, tree_data, pie_data = compute_data_choice_1(df_exec)
            
           
            bar_fig = px.bar(bar_data, x='Position', y=inp, title='Dept. Salary in Amount')
            
            
            pie_fig = px.pie(pie_data, values=inp, names='Position',hole= 0.4, title='Expenditure Share')
            
           
            tree_fig = px.treemap(tree_data, path=['Position', inp], 
                      values= inp ,
                    
                      color_continuous_scale='RdBu',
                      title='Structure of the Department'
                )
            
            
          
            return [dcc.Graph(figure=tree_fig), 
                    dcc.Graph(figure=pie_fig),
                    dcc.Graph(figure=bar_fig),
                   ]
        else:
            bar_data, tree_data, pie_data = compute_data_choice_2(df_dev)
            
           
            bar_fig = px.bar(bar_data, x='Position', y=inp, title='Dept. Salary in Amount')
            
            
            pie_fig = px.pie(pie_data, values=inp, names='Position', hole=0.5,title='Expenditure Share')
            
            tree_fig = px.treemap(tree_data, path=['Position', inp], 
                      values= inp ,
                    
                      color_continuous_scale='RdBu',
                      title='Structure of the Department'
                )
            
            return [dcc.Graph(figure=tree_fig), 
                    dcc.Graph(figure=pie_fig),
                    dcc.Graph(figure=bar_fig),
                   ]
                                                                                #callback for calculator
@app.callback(
    Output('calc_output', 'children'),
    [
        Input('calc_dd', 'value'),
        Input('calc_input', 'value')]
)
def calc(calc_dd_value, calc_input_value):
    print(calc_dd_value)
    print(type(calc_dd_value))
    print(calc_input_value)
    calc_input_value = int(calc_input_value)
    print(type(calc_input_value))

    dff = df_dev[df_dev['Position'] == calc_dd_value]
    tot_sal = int(dff['Salary/year/employee']) * calc_input_value
    tot_sal = "{:,}".format(tot_sal)
    return f'The total salary spent for {calc_input_value} {calc_dd_value} yearly is \n{tot_sal}'



if __name__ == '__main__':
    app.run_server(port=8002)


# In[ ]:




