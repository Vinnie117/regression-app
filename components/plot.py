from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from utils.base_plot import create_base_plot
from dash_app import dash_app
import sys

plot = html.Div(
    dcc.Graph(id='scatterplot')
)


# callback to update the scatter plot given changes
@dash_app.callback(
    Output(component_id = 'scatterplot', component_property = 'figure'),
    Output(component_id = 'dict_traces', component_property = 'data'),
    Output(component_id = 'list_used_colors', component_property = 'data'),
    Input(component_id = 'table', component_property = 'data'),
    Input(component_id = 'xaxis-column', component_property = 'value'),
    Input(component_id = 'yaxis-column', component_property = 'value'),
    Input(component_id = 'regression_results', component_property = 'data'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    State(component_id = 'dict_traces', component_property = 'data'),
    State(component_id = 'list_used_colors', component_property = 'data'))
def update_scatterplot(data, x_axis_name, y_axis_name, model, n_clicks, dict_traces, list_used_colors):

    if dict_traces == None:
        dict_traces = {}

    if list_used_colors == None:
        list_used_colors = []

    # red, azure, purple (default for points is '#636EFA') -> colors order for lines
    color_map = ['#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    color_map = [color for color in color_map if color not in list_used_colors]

    if not model:
        # base plot
        x_axis = [d[x_axis_name] for d in data]
        y_axis = [d[y_axis_name] for d in data]
        base_fig = go.Figure(create_base_plot(x_axis, y_axis))

        return base_fig, dict_traces, list_used_colors

    elif model:

        # new_traces = []

        # build the OLS line of each respective experiment and store it
        for run in model:
            new_trace =go.Scatter(
                x=model[run]['x_range'],
                y=model[run]['y_range'], 
                mode='lines',
                marker={'color': color_map[list(model.keys()).index(run)]},  # colors will be hardcoded here
                name=run)                
            # new_traces.append(new_trace)   

            # build the store which collects all traces
            if run not in dict_traces:
                dict_traces[run] = new_trace

                # keep track of used colors (could also look into dict_traces instead of using list_used_colors)
                list_used_colors.append(color_map[list(model.keys()).index(run)])

        # delete experiment run in trace store 'dict_traces' if it is removed in model
        # -> not necessary bc it disappears in selected_experiments list

        # match dropdown selection by experiment run (common ID)
        selected_experiments = []
        for run in model:
            if x_axis_name == model[run]['predictor_var'] and y_axis_name == model[run]['target_var']:
                selected_experiments.append(run)

        # print(selected_experiments)

        # fetch traces from trace store that match the experiment run
        available_traces = []
        for trace_key, trace_val in dict_traces.items():
            if trace_key in selected_experiments:
                available_traces.append(trace_val)

        # print(available_traces)

        # return the plot
        x_axis = [d[x_axis_name] for d in data]
        y_axis = [d[y_axis_name] for d in data]
        base_trace = create_base_plot(x_axis, y_axis)
        base_trace = [base_trace['data'][0]]

        fig = go.Figure(data= base_trace + available_traces, layout={'showlegend': True})
        print("The size of the dict_traces is {} bytes".format(sys.getsizeof(dict_traces)))  # 232 Bytes


        return fig, dict_traces, list_used_colors




