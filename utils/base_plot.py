def create_base_plot(x, y):
    
    base_plot = dict({
        "data": [{
            "type": "scatter",
            "x": x,
            "y": y,
            "mode": "markers",
            "name": "experiment_0",
            "marker": {"color": "#636EFA"}
        }],
        "layout": {}        
    })

    return base_plot