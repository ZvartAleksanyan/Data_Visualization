import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go


mouse_data = pd.read_csv('data/Mouse_metadata.csv')
study_results = pd.read_csv('data/Study_results.csv')
merged_df = pd.merge(mouse_data, study_results, on='Mouse ID')

color_choices = {
    'light-blue': '#7FAB8',
    'light-grey': '#F7EFED',
    'light-red': '#F1485B',
    'dark-blue': '#33546D',
    'middle-blue': '#61D4E2'
}

drug_colors = {
    'Placebo': '#29304E',
    'Capomulin': '#27706B',
    'Ramicane': '#71AB7F',
    'Ceftamin': '#9F4440',
    'Infubinol': '#FFD37B',
    'Ketapril': '#FEADB9',
    'Naftisol': '#B3AB9E',
    'Propriva': '#ED5CD4',
    'Stelasyn': '#97C1DF',
    'Zoniferol': '#8980D4'
}

grouped_drugs = {
    'lightweight': ['Ramicane', 'Capomulin'],
    'heavyweight': ['Infubinol', 'Ceftamin', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol'],
    'placebo': ['Placebo']
}

colors = {
    'full-background': color_choices['light-grey'],
    'chart-background': color_choices['light-grey'],
    'histogram-color-1': color_choices['dark-blue'],
    'histogram-color-2': color_choices['light-red'],
    'block-borders': color_choices['dark-blue']
}

margins = {'block-margins': '4px 4px 4px 4px'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

div_title = html.Div(html.H1('Title'),
                     style={
                         'border': f'3px {colors["block-borders"]} solid',
                         'margin': margins['block-margins'],
                         'text-align': 'center'
                     })

chart1_checklist = dcc.Checklist(
    id='weight-histogram-checklist',
    options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
    value=['Placebo'],
    labelStyle={'display': 'inline-block'}
)

chart1_graph = dcc.Graph(id='weight-histogram')

div_1_1 = html.Div([chart1_checklist, chart1_graph],
                   style={
                       'border': f'1px {colors["block-borders"]} solid',
                       'margin': margins['block-margins'],
                       'width': '50%',
                       'display': 'inline-block'
                   })

chart2_radio = dcc.RadioItems(
    id='drug-compare-radio',
    options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
    value='Placebo',
    labelStyle={'display': 'inline-block'}
)

chart2_graph = dcc.Graph(id='drug-compare-histogram')  # <-- This line fixes the error

div_1_2 = html.Div([chart2_radio, chart2_graph],
                   style={
                       'border': f'1px {colors["block-borders"]} solid',
                       'margin': margins['block-margins'],
                       'width': '50%',
                       'display': 'inline-block'
                   })

chart3_checklist = dcc.Checklist(
    id='group-histogram-checklist',
    options=[{'label': group, 'value': group} for group in grouped_drugs],
    value=['placebo'],
    labelStyle={'display': 'inline-block'}
)

chart3_graph = dcc.Graph(id='group-histogram')

div_2_1 = html.Div([chart3_checklist, chart3_graph],
                   style={
                       'border': f'1px {colors["block-borders"]} solid',
                       'margin': margins['block-margins'],
                       'width': '50%',
                       'display': 'inline-block'
                   })

chart4_checklist = dcc.Checklist(
    id='survival-checklist',
    options=[{'label': group, 'value': group} for group in grouped_drugs],
    value=['placebo'],
    labelStyle={'display': 'inline-block'}
)

chart4_graph = dcc.Graph(id='survival-line-chart')

div_2_2 = html.Div([chart4_checklist, chart4_graph],
                   style={
                       'border': f'1px {colors["block-borders"]} solid',
                       'margin': margins['block-margins'],
                       'width': '50%',
                       'display': 'inline-block'
                   })

app.layout = html.Div([
    div_title,


    html.Div([
        div_1_1,
        div_1_2
    ], style={'display': 'flex'}),


    html.Div([
        div_2_1,
        div_2_2
    ], style={'display': 'flex'})

], style={'backgroundColor': colors['full-background']})


@app.callback(
    Output('weight-histogram', 'figure'),
    Input('weight-histogram-checklist', 'value')
)
def update_chart1(drug_names):
    traces = [
        go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.9,
            marker=dict(color=drug_colors[drug])
        ) for drug in drug_names
    ]
    return {
        'data': traces,
        'layout': go.Layout(
    height=400,
    barmode='overlay',
    xaxis={'title': 'mouse weight', 'showgrid': False},
    yaxis={'title': 'number of mice', 'showgrid': False},
    plot_bgcolor=colors['chart-background'],
    paper_bgcolor=colors['chart-background'],
    )
    }


@app.callback(
    Output('drug-compare-histogram', 'figure'),
    Input('drug-compare-radio', 'value')
)
def update_chart2(selected_drug):
    bin_config = dict(
        start=merged_df['Weight (g)'].min(),
        end=merged_df['Weight (g)'].max(),
        size=1  # adjust bin width as needed
    )

    traces = [
        go.Histogram(
            x=merged_df['Weight (g)'],
            name='all mice',
            opacity=0.6,
            marker=dict(color=colors['histogram-color-1']),
            xbins=bin_config
        ),
        go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == selected_drug]['Weight (g)'],
            name=selected_drug,
            opacity=1,
            marker=dict(color=drug_colors[selected_drug]),
            xbins=bin_config
        )
    ]

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='overlay',
			xaxis={'title': 'mouse weight', 'showgrid': False},
			yaxis={'title': 'number of mice', 'showgrid': False},
            plot_bgcolor=colors['chart-background'],
            paper_bgcolor=colors['chart-background'],
            legend=dict(x=0, y=1)
        )
    }


@app.callback(
    Output('group-histogram', 'figure'),
    Input('group-histogram-checklist', 'value')
)
def update_chart3(groups):
    traces = []
    for group in groups:
        for drug in grouped_drugs[group]:
            traces.append(
                go.Histogram(
                    x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
                    name=drug,
                    opacity=0.8,
                    marker=dict(color=drug_colors[drug])
                )
            )
    return {
        'data': traces,
        'layout': go.Layout(
            barmode='overlay',
			xaxis={'title': 'mouse weight', 'showgrid': False},
			yaxis={'title': 'number of mice', 'showgrid': False},
            plot_bgcolor=colors['chart-background'],
            paper_bgcolor=colors['chart-background'],
        )
    }


@app.callback(
    Output('survival-line-chart', 'figure'),
    Input('survival-checklist', 'value')
)
def update_chart4(groups):
    traces = []
    for group in groups:
        for drug in grouped_drugs[group]:
            group_df = merged_df[merged_df['Drug Regimen'] == drug]
            survival = group_df.groupby('Timepoint')['Mouse ID'].nunique().sort_index(ascending=True)
            traces.append(
                go.Scatter(
                    x=survival.index,
                    y=survival.values,
                    mode='lines+markers',
                    name=drug,
                    line=dict(shape='linear'),
                    marker=dict(color=drug_colors[drug])
                )
            )
    return {
        'data': traces,
        'layout': go.Layout(
			xaxis={'title': 'time point'},
			yaxis={'title': 'number of mice alive', 'showgrid': False},
            plot_bgcolor=colors['chart-background'],
            paper_bgcolor=colors['chart-background'],
        )
    }


if __name__ == '__main__':
    app.run(debug=True, port=8081)

