# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': sites[0], 'value': sites[0]},
                                                    {'label': sites[1], 'value': sites[1]},
                                                    {'label': sites[2], 'value': sites[2]},
                                                    {'label': sites[3], 'value': sites[3]}
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
         # Group data by Launch Site and calculate success count
        success_counts = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='count')
        fig = px.pie(success_counts, values='count', 
        names='Launch Site', 
        title='Total Success Launches by Site')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[ spacex_df['Launch Site'] == entered_site ]
        # Calculate Success vs Failure counts
        site_counts = filtered_df['class'].value_counts().reset_index(name='count')
        site_counts.columns = ['class', 'count']  # Rename columns for clarity

        fig = px.pie(site_counts, values='count', 
        names='class', 
        title=f'Success vs Failure for site {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output( component_id='success-payload-scatter-chart', component_property='figure' ),
    [Input( component_id='site-dropdown', component_property='value' ), 
     Input( component_id='payload-slider', component_property='value' )]
)

def get_scatter_chart(entered_site, payload_range ):

    # Filter the dataset by the selected payload range
    filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]

    # Check if a specific site is selected or 'ALL' is selected
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color="Booster Version Category",
                         title="Scatter Plot of Payload Mass vs. Launch Outcome", 
                         labels={"Payload Mass (kg)": "Payload Mass (kg)", "class": "Launch Outcome (1=Success, 0=Failure)"},
        )
    else:
        # Filter data for the selected site
        filtered_df = filtered_df[ filtered_df['Launch Site'] == entered_site ]
        fig = px.scatter(filtered_df,
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color="Booster Version Category",
                         title="Scatter Plot of Payload Mass vs. Launch Outcome", 
                         labels={"Payload Mass (kg)": "Payload Mass (kg)", "class": "Launch Outcome (1=Success, 0=Failure)"},
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


