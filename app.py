######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.express as px


###### Define your variables #####
sourceurl = 'https://github.com/cohos-method/304-titanic-dropdown/blob/main/assets/bank-additional.csv'
githublink = 'https://github.com/cohos-method/304-titanic-dropdown'

filename = "assets/bank-additional.csv"
variables_list=['Marital', 'Housing', 'Contact']
tabtitle = 'Cohos Method Bank Data Exploration'

grpby = ['education', 'job']
aggcols=['marital.divorced', 'marital.married','marital.single', 'marital.unknown', 'housing.no', 'housing.unknown', 'housing.yes', 'contact.cellular', 'contact.telephone']

###### Functions #######
create_df = lambda f,s: pd.read_csv(f, sep=s)

prefix_column = lambda colist, prefix : [prefix + i for i in colist]

build_dict = lambda test_keys, test_values : {test_keys[i]: test_values[i] for i in range(len(test_keys))}

def create_dummies(df, dum_col):
    df_dum = pd.get_dummies(df[dum_col])
    cols = df_dum.columns
    pcols = prefix_column(cols,dum_col+".")
    d = build_dict(cols, pcols)
    df_dum.rename(columns=d, inplace=True)
    return pd.concat([df, df_dum], axis='columns')

def create_grpby_df(df, grpby_cols):
    return df.groupby(by=grpby_cols, axis=0, sort=True)

def create_grpby_avg_df(df, grpby_cols, cols):
    return df[cols].mean()

def create_grpby_sum_df(df, grpby_cols, cols):
    return df[cols].sum()

def create_grpby_count_df(df, grpby_cols, cols):
    return df[cols].count()

def drawfig(dfx, choice_made, x_col):

    marital= [  'marital.divorced'
              , 'marital.married'
              , 'marital.single'
              , 'marital.unknown']

    housing = [ 'housing.no'
               , 'housing.unknown'
               , 'housing.yes']

    contact = [  'contact.cellular'
               , 'contact.telephone']

    color_pal=['#92A5E8'
           , '#8E44AD'
           , '#FFC300'
           ,'#AAA100']

    choice = {  "Marital" : marital
              , "Housing" : housing
              , "Contact" : contact}


    mydata = []

    print(choice[choice_made][0], x_col)

    for it in range(len(choice[choice_made])):
        col = choice[choice_made][it]
        # print(col)
        myd = go.Bar(x=dfx[x_col], y=dfx[col], name = col.title(), marker=dict(color=color_pal[it]))
        mydata.append(myd)
        # print (myd)

    mylayout = go.Layout(
        title=f'Grouped Bar Chart by {x_col.title()}',
        xaxis = dict(title = x_col.title()), # x-axis label
        yaxis = dict(title = str(choice_made).title()), # y-axis label

    )
    fig = go.Figure(data=mydata, layout=mylayout)
    return fig


###### Import a dataframe #######
df = create_df(filename, ";")

df = create_dummies(df, 'marital')
df = create_dummies(df, 'housing')
df = create_dummies(df, 'contact')

#df = df.query(" job == 'student' ")
dfg = create_grpby_df(df, grpby)
#dfa = create_grpby_avg_df(dfg, grpby, aggcols)
#dfc = create_grpby_count_df(dfg, grpby, aggcols)
dfs = create_grpby_sum_df(dfg, grpby, aggcols)

dfx = pd.DataFrame(dfs)
dfx.reset_index(inplace=True)
#dfx = dfx.query("education == 'basic.9y' ")


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H1('Bank Additional Data'),
    html.H2('Every line of this code is done fresh.'),
    html.H3('Choose a continuous variable to explore the bank data:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value1'),
    dcc.Graph(id='display-value2'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value1', 'figure')
             ,Output('display-value2', 'figure')
             ,[Input('dropdown', 'value')])
def display_value(continuous_var):
    print (continuous_var)
    fig1 = drawfig(dfx, continuous_var, 'job')
    fig2 = drawfig(dfx, continuous_var, 'education')

    # grouped_mean=df.groupby(['Cabin Class', 'Embarked'])[continuous_var].mean()
    # results=pd.DataFrame(grouped_mean)
    # # Create a grouped bar chart
    # mydata1 = go.Bar(
    #     x=results.loc['first'].index,
    #     y=results.loc['first'][continuous_var],
    #     name='First Class',
    #     marker=dict(color=color1)
    # )
    # mydata2 = go.Bar(
    #     x=results.loc['second'].index,
    #     y=results.loc['second'][continuous_var],
    #     name='Second Class',
    #     marker=dict(color=color2)
    # )
    # mydata3 = go.Bar(
    #     x=results.loc['third'].index,
    #     y=results.loc['third'][continuous_var],
    #     name='Third Class',
    #     marker=dict(color=color3)
    # )
    #
    # mylayout = go.Layout(
    #     title='Grouped bar chart',
    #     xaxis = dict(title = 'Port of Embarkation'), # x-axis label
    #     yaxis = dict(title = str(continuous_var)), # y-axis label
    #
    # )
    # fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig1,fig2,


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
