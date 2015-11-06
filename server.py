from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import projectOHYEAH
import json
from model import NASDAQNYSE, connect_to_db, db
from yahoo_finance import Share


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

    company = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == search).first()
    ticker = company.ticker_code
    company_name = company.company_name
    industry = company.bus_sector
    sector = company.bus_type

    stock = Share(ticker)
    stock_closing_price = stock.get_open()
    
    neg_results, pos_results, positive_values, negative_values, a, b, c = projectOHYEAH.get_results(search)

    return render_template("results.html", neg_results=neg_results,
                           pos_results=pos_results, positive_values=positive_values,
                           negative_values=negative_values, a=a, b=b, c=c, 
                           ticker=ticker, stock_closing_price=stock_closing_price,
                           company_name=company_name, industry=industry, sector=sector)


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run()
