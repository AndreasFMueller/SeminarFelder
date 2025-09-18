from dash import Dash, html, dcc, callback, Output, Input, State, callback_context


def dash_app(figs: list):

    app = Dash()

    # Requires Dash 2.17.0 or later
    app.layout = [
        html.H1(children="Rossby Waves", style={"textAlign": "center"}),
        dcc.Graph(id="graph-content", figure=figs[0]),
        html.Div(
            [
                html.Button("⬅️ Back", id="back-btn", n_clicks=0),
                html.Button("Next ➡️", id="next-btn", n_clicks=0),
            ],
            style={"textAlign": "center", "marginTop": "1rem", "color": "#e5ecf6"},
        ),
        dcc.Store(id="frame-index", data=0),
    ]

    @app.callback(
        Output("graph-content", "figure"),
        Output("frame-index", "data"),
        Input("back-btn", "n_clicks"),
        Input("next-btn", "n_clicks"),
        State("frame-index", "data")
    )
    def step_frames(back_clicks, next_clicks, current_index):
        ctx = callback_context
        if not ctx.triggered:
            return figs[current_index], current_index

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "back-btn":
            new_index = max(0, current_index - 1)
        elif button_id == "next-btn":
            new_index = min(len(figs) - 1, current_index + 1)
        else:
            new_index = current_index

        print(new_index)
        return figs[new_index], new_index

    return app
