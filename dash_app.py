    # imports
    import zipfile as zp
    from typing import Type

    import pandas as pd
    import numpy as np
    import plotly.offline as pyo
    import plotly.figure_factory as ff
    import plotly.graph_objs as go
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output

    # ------------------------------------------------- IMPORTING DATA -----------------------------------------------------

    # Reading Airbnb df
    from pandas import DataFrame

    df = pd.read_csv("./data/final_df.csv")



    # ----------------------------------------------------- FIGURES --------------------------------------------------------
    fig_map = go.Figure(
        data=go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            mode="markers"),
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken="pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ",
                style="dark",
                center={'lat': 39, 'lon': -9.2},
                zoom=8.5,
            )
        )
    )

    fig_pie = go.Figure(
        data=go.Pie(
            labels=df['room_type'].value_counts().index,
            values=df['room_type'].value_counts().values,
            textinfo='text+value+percent',
            text=df['room_type'].value_counts().index,
            hoverinfo='label',
            showlegend=False),
        layout=go.Layout(
            margin=go.layout.Margin(l=0, r=0, t=70, b=0),
            title='Proportion of Room Type')
    )

    fig_bar = go.Figure(
        data=go.Bar(
            x=df['ordinal_rating'].value_counts().values,
            y=df['ordinal_rating'].value_counts().index,
            orientation='h'),
        layout=go.Layout(
            margin=go.layout.Margin(l=0, r=0, t=70, b=0),
            title="Listing Rating Frequency")
    )

    fig_hist = go.Figure(
        data=ff.create_distplot(
            [df['price']],
            ['distplot'],
            bin_size=30,
            show_rug=False),
        layout=go.Layout(
            margin=go.layout.Margin(l=0, r=0, t=70, b=0),
            title="Listing Rating Frequency",
            sliders=[dict(active=4,
                          currentvalue={"prefix": "bin size: "},
                          pad={"t": 20},
                          steps=[dict(label=i,
                                      method='restyle',
                                      args=['xbins.size', i]) for i in range(1, 20)]
                          )
                     ]
            )
    )

    fig_hist.data[0].marker.line = dict(color='black', width=2)
    fig_hist.data[1].line.color = 'red'
    fig_hist.update_layout(xaxis_title='Price ($)',
                           yaxis_title='Relative frequencies',
                           showlegend=False,
                           title='Price distribution')

    # ------------------------------------------------------- APP ----------------------------------------------------------
    app = dash.Dash(__name__, assets_folder="./assets")

    # Add the following line before deployment
    # server = app.server

    # ------------------------------------------------------- HTML ---------------------------------------------------------

    app.layout = html.Div([
        html.Div([
            html.H1('Airbnb Lisbon: a client focused application'),
            ], id='html_title'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_map, id="dcc_map_graph")
            ], id='html_map', className='eight columns'),
            html.Div([
                dcc.Dropdown(
                    options=[{'label': i, 'value': i} for i in
                             ["All"] + df["neighbourhood_group_cleansed"].unique().tolist()],
                    value='All',
                    # placeholder="Select Municipality",
                    id='dcc_neighbourhood_dropdown'
                ),
                dcc.Dropdown(
                    options=[{'label': i, 'value': j} for i, j in zip(
                        ["Availability", "Superhost","Cancellation Policy"],
                        ["availability_next_30", "host_is_superhost", "cancellation_policy"])],
                    value='host_is_superhost',
                    # placeholder="Select Variable",
                    id='dcc_variable_dropdown'
                ),
                dcc.Graph(figure=fig_pie, id="dcc_pie_graph"),
                dcc.Graph(figure=fig_bar, id="dcc_bar_graph"),
                dcc.Graph(figure=fig_hist, id="dcc_hist_graph")
                ], id="html_non_map", className="four columns")
            ], id="html_row", className="row")
        ])

    # --------------------------------------------------- CALLBACKS --------------------------------------------------------
    rates = list(df.ordinal_rating.unique())
    neig = list(df.neighbourhood_group_cleansed.unique())
    price = [[df.price.min(), df.price.max()]]
    room = list(df.room_type.unique())

    def slice_df(neig=neig, rates=rates, price=price, room=room):
        aux = df.copy()
        # slice neighbourhood
        aux = aux.loc[aux['neighbourhood_group_cleansed'].isin(neig)]
        # slice rating
        aux = aux.loc[aux['ordinal_rating'].isin(rates)]
        # slice room type
        aux = aux.loc[aux['room_type'].isin(room)]
        # slice price
        aux = aux.loc[(aux['price'] > price[0]) & (aux['price'] < price[-1])]
        return aux

    list_of_neighbourhoods = {
        "All": {"lat": 39, "lon": -9.2, "zoom": 8.5},
        "Amadora": {"lat": 38.7578, "lon": -9.2245, "zoom": 11},
        "Cascais": {"lat": 38.6979, "lon": -9.42146, "zoom": 11},
        "Cadaval": {"lat": 39.2434, "lon": -9.1027, "zoom": 11},
        "Arruda Dos Vinhos": {"lat": 38.9552, "lon": -8.989, "zoom": 11},
        "Vila Franca De Xira": {"lat": 38.9552, "lon": -8.989, "zoom": 11},
        "Oeiras": {"lat": 38.6969, "lon": -9.3146, "zoom": 11},
        "Loures": {"lat": 38.8315, "lon": -9.1741, "zoom": 11},
        "Sobral De Monte Agrao": {"lat": 39.0188, "lon": -9.1505, "zoom": 11},
        "Alenquer": {"lat": 39.0577, "lon": -9.014, "zoom": 11},
        "Odivelas": {"lat": 38.7954, "lon": -9.1852, "zoom": 11},
        "Torres Vedras": {"lat": 39.0918, "lon": -9.26, "zoom": 11},
        "Lourinhã": {"lat": 39.2415, "lon": -9.313, "zoom": 11},
        "Mafra": {"lat": 38.9443, "lon": -9.3321, "zoom": 11},
        "Sintra": {"lat": 38.8029, "lon": -9.3817, "zoom": 11},
        "Lisboa": {"lat": 38.7223, "lon": -9.1393, "zoom": 11},
        "Azambuja": {"lat": 39.0696, "lon": -8.8693, "zoom": 11},
    }
    # Define a new df with the colors

    df_colors = df[["property_id","host_is_superhost","cancellation_policy","available"]].set_index("property_id")
    df_colors.columns = ["superhost","cancellation","availability"]

    #Superhost colors
    df_colors["superhost_colors"] = "red"
    df_colors.loc[df_colors["superhost"] == 1, "superhost_colors"] = "green" #verde
    #Cancellation colors
    df_colors["cancellation_colors"]= "red" #vermelho strict
    df_colors.loc[df_colors["cancellation"] == "flexible", "cancellation_colors"] = "green"
    df_colors.loc[df_colors["cancellation"] == "moderate", "cancellation_colors"] = "yellow"
    #Availability colors
    df_colors["availability_colors"] = "red" #low
    df_colors.loc[df_colors["availability"] == "Medium", "availability_colors"] = "yellow"
    df_colors.loc[df_colors["availability"] == "High", "availability_colors"] = "green"


    @app.callback(
        Output("dcc_map_graph", "figure"),
        [
            Input("dcc_neighbourhood_dropdown", "value"),
            Input("dcc_variable_dropdown", "value")
        ]
    )
    def update_map(selectedlocation, selectedvariable):
        latInitial = 39
        lonInitial = -9.2
        zoomInitial =  8.5
        # host_years = df["Years_host"]
        # customdata = np.dstack((df.Years_host, df.price))

        if selectedlocation != "All": #Pass the parameters for the neighbourhoods
            latInitial = list_of_neighbourhoods[selectedlocation]["lat"]
            lonInitial = list_of_neighbourhoods[selectedlocation]["lon"]
            zoomInitial = list_of_neighbourhoods[selectedlocation]["zoom"]

        # Dropdown for the variables

        if selectedvariable == "host_is_superhost":
            return go.Figure(
            # Data
                data = [
                    go.Scattermapbox(
                        ids=df["property_id"],
                        lat=df["latitude"],
                        lon=df["longitude"],
                        mode="markers",
                        marker = dict(
                                color= df_colors["superhost_colors"]
                        ),
                    ),
                ],
            # Layout
                layout = go.Layout(
                        autosize=True,
                        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                        showlegend=False,
                        mapbox=dict(
                            accesstoken="pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ",
                            center = {'lat': latInitial, 'lon': lonInitial},
                            zoom=zoomInitial,
                            style="dark",
                        )
                )
            )
        elif selectedvariable == "cancellation_policy":
            return go.Figure(
                # Data
                data=[
                    go.Scattermapbox(
                        ids=df["property_id"],
                        lat=df["latitude"],
                        lon=df["longitude"],
                        mode="markers",
                        marker=dict(
                            color=df_colors["cancellation_colors"]
                        ),
                    ),
                ],
                # Layout
                layout=go.Layout(
                    autosize=True,
                    margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                    showlegend=False,
                    mapbox=dict(
                        accesstoken="pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ",
                        center={'lat': latInitial, 'lon': lonInitial},
                        zoom=zoomInitial,
                        style="dark"
                    )
                )
            )

        elif selectedvariable == "availability_next_30":
            return go.Figure(
                # Data
                data=[
                    go.Scattermapbox(
                        ids=df["property_id"],
                        lat=df["latitude"],
                        lon=df["longitude"],
                        mode="markers",
                        marker=dict(
                            color=df_colors["availability_colors"]

                        ),
                        customdata =[df.price,df.Years_host],

                        hovertemplate= '<i>Price</i>: %{customdata[0]:$.2f}'+
                                        '<br>Nº of years as host: %{customdata[1]}<br>'

                                        # 'Nº of years as host: %{customdata[0]} <br> Price: %{customdata[1]:$.2f} '
                                        #"<br>Nº of years as host: %{customdata[0]} <br>Price: %{customdata[1]:$.2f}",
                                        #"Price: %{customdata[1]:$.2f}<extra></extra>",
                                        #"<br>Nº of years as host: %{customdata}<br>",
                    ),
                ],
                # Layout
                layout=go.Layout(
                    autosize=True,
                    margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                    showlegend=False,
                    mapbox=dict(
                        #hovermode = "closest",
                        accesstoken="pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ",
                        style="dark",
                        center={'lat': latInitial, 'lon': lonInitial},
                        zoom=zoomInitial,
                    )
                )
    )
    if __name__ ==  '__main__':
        app.run_server()
