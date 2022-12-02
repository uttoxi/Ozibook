#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from dash import Dash , dcc , html , Input , Output, State
import dash_bootstrap_components as dbc
import plotly.express as px


# In[2]:


app=Dash(__name__,external_stylesheets=[dbc.themes.LUX])
app.config.suppress_callback_exceptions = True


# In[3]:


df_dev=pd.read_excel(r"C:\Users\utkar\Downloads\Developers.xlsx",index_col=[0])
df_exec=pd.read_excel(r"C:\Users\utkar\Downloads\Executives.xlsx",index_col=[0])


# In[4]:


def compute_data_choice_1(df_exec):
    
    bar_data = df_exec
    pie_data= df_exec
    tree_data = df_exec
    return bar_data,tree_data, pie_data


# In[5]:


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
                   'font-family':'verdana',
                   'text-color': 'cerise',
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
                html.H2('Position type:', style={
                    'margin-right': '2em','font-size':'20px'})
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
                    html.H2('Monthly/Yearly:', style={
                        'margin-right': '2em','font-size':'20px'})
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
    
    
    
    html.Div([html.Div([], id='plot3',style={'border-style':'ridge','width':'53%'}),   
    html.Div([                                                                               #Division for calculator
        html.H2(' Calculator for salary based on number of employees', style={
                    'margin-right': '2em','font-size':'20px'}),
            
        html.Div(["Number of Interns: ",
              dcc.Input(id='intern', value='inr', type='number')]),
            
    html.Br(),
            
         html.Div(["Number of Freshers: ",
              dcc.Input(id='fresh', value='f', type='number')]),
            
    html.Br(),
            
         html.Div(["Number of Freshers team lead: ",
              dcc.Input(id='freshtl', value='ftl', type='number')]),
            
    html.Br(),
            
         html.Div(["Number of QA tester: ",
              dcc.Input(id='qatest', value='qt', type='number')]),
            
    html.Br(),
            
         html.Div(["Number of Frontend developer: ",
              dcc.Input(id='front', value='fed', type='number')]),
            
    html.Br(),
            
        html.Div(["Number of Backend developer: ",
              dcc.Input(id='front', value='fed', type='number')]),
            
    html.Br(),
         html.Div(["Number of Head of engineering: ",
                   
              dcc.Input(id='head', value='hoe', type='number')]),
            
    html.Br(),
            
     html.H2('Total Employees expense is: ', style={'text-align': 'left'}), 
            
    html.Div(id='my-output')                                                   #division for output
        ],style={'border-style':'ridge'})
        
                                                             
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
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='intern', component_property='value'),
     Input(component_id='fresh', component_property='value'),
     Input(component_id='freshtl', component_property='value'),
     Input(component_id='qatest', component_property='value'),
     Input(component_id='front', component_property='value'),
     Input(component_id='back', component_property='value'),
     Input(component_id='head', component_property='value')]
     )
def exp_calc(inr,f,ftl,qt,fed,bed,hod,o):   
    f_sum = f * df_dev.iat[5,2]           
    inr_sum = inr * df_dev.iat[6,2]
    ftl_sum = ftl * df_dev.iat[4,2]
    qt_sum = qt * df_dev.iat[3,2]  
    fed_sum = fed * df_dev.iat[2,2]
    bed_sum = bed * df_dev.iat[1,2]
    hod_sum = hod * df_dev.iat[0,2]
    Tot_exp = inr_sum + f_sum + ftl_sum + qt_sum + fed_sum + bed_sum + hod_sum
    return Tot_exp

if __name__ == '__main__':
    app.run_server()


# In[ ]:




