import pandas as pd
from dash import Dash , dcc , html , Input , Output
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

df_dev= pd.read_excel(r"C:\Users\utkar\Downloads\Developers.xlsx",index_col=[0])
df_exec=pd.read_excel(r"C:\Users\utkar\Downloads\Executives.xlsx",index_col=[0])

fig1 = px.treemap(df_dev, names= 'Position',  values='Number of employees' )
fig2 = px.pie(df_dev, values='Number of employees', names='Position',hole=0.65)

app.layout= html.Div([
html.Div([

    html.H1("SALARY FOR EXECUTIVES AND DEVELOPERS", style={'text-align': 'center'}),
    dcc.Dropdown(
        id="my_dropdown",
        options=[
            {'label': 'S/M/E', 'value': 'Salary/month/employee'},
            {'label': 'S/M', 'value': 'Salary/month'},
            {'label': 'S/Y/E', 'value': 'Salary/year/employee'},
            {'label': 'S/Y', 'value': 'Salary/year'}
        ],
        value='Salary/month',
        multi=False,
        style={"width": "50%"},
        disabled=False
    ),
    html.Div([
    dcc.Graph(id='tree_map',figure={}),

    html.Br(),
    dcc.Graph(id='Bar_chart',figure={})
    ])
    ])

@app.callback(
    Output(component_id='tree_map',component_property='figure'),
    Output(component_id='Bar_chart',component_property='figure'),
    [Input(component_id='my_dropdown',component_property='value')]
)
def gen_graph(val):
    dff=df_dev.copy()
    fig1= px.treemap(dff,names='Position',values= val,title= "Tree map of salary distribution")
    fig2= px.bar(dff,x= 'Position',y=val,height= 750,width=1200)
    return fig1,fig2

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)