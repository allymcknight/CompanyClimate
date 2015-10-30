from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import projectOHYEAH


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

    neg_results, pos_results, positive_values, negative_values = projectOHYEAH.get_results(search)

    return render_template("results.html", neg_results=neg_results,
                           pos_results=pos_results, positive_values=positive_values,
                           negative_values=negative_values)


if __name__ == "__main__":
    app.debug = True

    DebugToolbarExtension(app)

    app.run()
