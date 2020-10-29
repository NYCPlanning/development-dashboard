import dash_html_components as html
import dash_bootstrap_components as dbc


def create_headers():

    headers = dbc.CardDeck(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Text Section 1", className="card-title"),
                        html.P(
                            "Some explanation about the housing data base.... "
                            "bit longer than the second card.",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="success", className="mt-auto"
                        ),
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Text Section 2", className="card-title"),
                        html.P(
                            "Continue explanations for database...",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="warning", className="mt-auto"
                        ),
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Text Section 3", className="card-title"),
                        html.P(
                            "This card has some text content, which is longer "
                            "than both of the other two cards, in order to "
                            "demonstrate the equal height property of cards in a "
                            "card group.",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="danger", className="mt-auto"
                        ),
                    ]
                )
            ),
        ]
    )
    return headers 