from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import projectOHYEAH
import json


app = Flask(__name__)

app.secret_key = "ABCsgerhysdvc8c9u4wf"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Renders homepage."""

    return render_template("home.html")


@app.route('/results')
def search_results():
    """Renders page with results of search and sentiment analysis."""

    search = request.args.get("search")
    session["search"] = search
    print session["search"]

    neg_results, pos_results, positive_values, negative_values, a, b, c = projectOHYEAH.get_results(search)

    return render_template("results.html", neg_results=neg_results,
                           pos_results=pos_results, positive_values=positive_values,
                           negative_values=negative_values, a=a, b=b, c=c)

# @app.route('/sentiment-ratio.json')
# def melon_types_data():
#     """Return data about sentiment ratio."""
#     print session["search"]
#     neg_results, pos_results, positive_values, negative_values, a, b, c = projectOHYEAH.get_results(session["search"])
#     print a, b, c

#     data_list_of_dicts = {
#         'sentiments': [
#             {
#                 "value": a,
#                 "color": "#46BFBD",
#                 "highlight": "#46BFBD",
#                 "label": "Positive"
#             },
#             {
#                 "value": b,
#                 "color": "#F7464A",
#                 "highlight": "#F7464A",
#                 "label": "Negative"
#             },
#             {
#                 "value": c,
#                 "color": "#C0C0C0",
#                 "highlight": "#C0C0C0",
#                 "label": "Neutral"
#             },
#         ]
#     }
#     return jsonify(data_list_of_dicts)


if __name__ == "__main__":
    app.debug = True

    DebugToolbarExtension(app)

    app.run()
