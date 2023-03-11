def create_base_plot(x, y, type):
    

    if type == 'object':
        base_plot = dict({
            "data": [{
                "type": "box",
                "x": x,
                "y": y,
                "showlegend": False,
                "marker": {"color": "#636EFA"},
                "boxpoints": "all",
                "jitter": 0.3,
                "pointpos": 0
            }],
            # "layout": {"margin":{"l":20, "r":20, "t":20, "b": 20}}    
            "layout": {"margin":{"l":0, "t":35, "r":0}}       
        })

    elif type  == 'numeric':
        base_plot = dict({
            "data": [{
                "type": "scatter",
                "x": x,
                "y": y,
                "mode": "markers",
                "showlegend": False,
                "marker": {"color": "#636EFA"}
            }],
            # "layout": {"margin":{"l":20, "r":20, "t":20, "b": 20}} 
            "layout": {"margin":{"l":0, "t":35, "r":0}}          
        })


    return base_plot