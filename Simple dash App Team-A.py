import pandas as pd
from dash import Dash , dcc , html , Input , Output
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

df_dev= pd.read_excel(r"C:\Users\utkar\Downloads\Developers.xlsx",index_col=[0])
df_exec=pd.read_excel(r"C:\Users\utkar\Downloads\Executives.xlsx",index_col=[0])

app.layout = html.Div( children=[
    # Add title to the dashboard
    html.H1('Salary Expenditure',
            style={'text allign': 'center',
                   'color': '#503D36',
                   'font-size': 24}),
    #Dropdown creation
    html.Div([
        # Add an division
        html.Div([

            html.Div([
                html.H2('Position type:', style={
                    'margin-right': '2em'})
            ]
            ),
            # Add a dropdown

            dcc.Dropdown(id='input-Ptype',
                         options=[
                             {'label': 'Executives',
                              'value': 'OPT1'},
                             {'label': 'Developers',
                              'value': 'OPT2'}
                         ],
                         placeholder='Select a Position type',
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-allign': 'center'})

        ], style={'display': 'flex'}),

        # Add next division
        html.Div([

            html.Div(
                [
                    html.H2('Choose type of expense:', style={
                        'margin-right': '2em'})
                ]
            ),
            dcc.Dropdown(id='input-Etype',
                         # Update dropdown values using list comphrehension
                         options=[
                             {'label': 'Salary per month per employee',
                              'value': 'Salary/month/employee'} ,
                             {'label': 'Salary per month' ,
                              'value': 'Salary/month/employee'},
                             {'label': 'Salary per year per employee',
                              'value': 'Salary/month/employee'},
                            {'label': 'Salary per year' ,
                              'value': 'Salary/month/employee'} ],
                         placeholder="Type of expense",
                         style={'width': '60%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),

        ], style={'display': 'flex'}),
        ]),
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2'),
            html.Div([], id='plot3')],
            ),
    ])







@app.callback([ Output(component_id='plot1', component_property='children'),
                Output(component_id='plot2', component_property='children'),
                Output(component_id='plot3', component_property='children')],
               [Input(component_id='input-Ptype', component_property='value'),
                Input(component_id='input-Etype', component_property='value')])

def get_graph(chart, inp):


    if chart == 'OPT1':

        bar_fig = px.bar(df_exec, x='Position', y=inp,
                         title='Salary comparison')

        tree_fig = px.treemap(data_frame=df_exec, path=[px.Constant('Executives'), 'Position'], values=inp,
                          title='Salary distribution')


        pie_fig = px.pie(df_exec, values='Number of employees', names='Position',
                         title='% of Positions in company')


        return [dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig)
                ]
    else:

        bar_fig = px.bar(df_dev, x='Position', y=inp,
                         title='Salary comparison')


        tree_fig = px.treemap(data_frame=df_dev, path=[px.Constant('Developers'), 'Position'], values=inp,
                          title='Salary distribution')


        pie_fig = px.pie(df_dev, values='Number of employees', names='Position',
                         title='% of Positions in company')






        return [dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig)
                ]

if __name__ == '__main__':
    app.run_server(debug=True)