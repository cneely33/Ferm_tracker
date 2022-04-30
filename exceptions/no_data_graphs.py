#
# Return an empty line graph filter if no invalid options are selected
#   alternative to raise.prevent.update 

def figure_none_line():
    import plotly.graph_objects as go
    fig_none = go.Figure()
    background="white"
    fig_none.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        y=[0, 4, 5, 1, 2, 3, 2, 4, 2, 1],
        mode="lines+markers+text",
        text=["","","","", "No Data", "","","", "", ''],
        textfont_size=40,
    ))
    fig_none.update_layout(
        paper_bgcolor=background,
        plot_bgcolor=background      
    )
    fig_none.update_layout(
        xaxis = dict(
            showgrid=False,
            gridcolor=background,
            zerolinecolor=background),
        yaxis = dict(
            showgrid=False,
            gridcolor=background,
            zerolinecolor=background))
    
    return fig_none
