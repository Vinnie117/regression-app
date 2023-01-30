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
        # "layout": {"margin":{"l":20, "r":20, "t":20, "b": 20}}        
    })

    return base_plot