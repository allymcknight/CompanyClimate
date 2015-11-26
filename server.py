from jinja2 import StrictUndefined
from flask import Flask, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from sentimentfuncs import run_googlenews_api, article_scraper, analyze_sentiment, sort_results, process_funcs
from model import NASDAQNYSE, connect_to_db
from yahoo_finance import Share
from datetime import timedelta, datetime
from collections import OrderedDict
from datetime import datetime

app = Flask(__name__)

app.secret_key = "ABCsgerhysdvc8c9u4wf"

app.jinja_env.undefined = StrictUndefined

def get_date_range():
    """Using Datetime, grabs the current date and the date of 10 days ago."""

    today = datetime.now()
    ten = timedelta(days=200)
    last_ten = today - ten
    today_year= str(today.year)
    today_month = str(today.month)
    today_day = str(today.day)
    today_date = today_year + "-" + today_month + "-" + today_day

    last_10_year = str(last_ten.year)
    last_10_month = str(last_ten.month)
    last_10_day = str(last_ten.day)
    last_10_date = last_10_year + "-" + last_10_month + "-" + last_10_day

    return today_date, last_10_date

def get_historical_prices():
    """Creates an OrderedDict which contains the days from current day and the 
    closing stock price on that day."""

    today, last_10_date = get_date_range()
    finance_object = Share(session['symbol'])
    history = finance_object.get_historical(last_10_date, today)

    stock_history = OrderedDict()
    for i in range(len(history)):
        stock_history[-i] = history[i]['Adj_Close']

    return stock_history


@app.route('/')
def index():
    """Renders homepage."""

    return render_template("home.html")

def get_company_info(search):
    """Gets the company information from database"""
    company = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == search).first()
    company_name = company.company_name
    industry = company.bus_sector
    sector = company.bus_type
    ticker = company.ticker_code
    return company_name, industry, sector, ticker



@app.route('/results')
def search_results():
    """Renders page with results of search and sentiment analysis."""
    # Grabs the search item with a get request.
    search = request.args.get("search")

    try:
        # Querys my database for the search company's object.
        company = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == search).first()
        ticker = company.ticker_code
        # Grabs even more information about the company from the database.
        company_name, industry, sector, ticker = get_company_info(search)

        # Stores the ticker code in the session.
        session['symbol'] = ticker

        # Gets the current date and time
        d = datetime.now()
        now = d.strftime("%c")

        # Runs the search value through the functions (google API, web scraper, sentiment analysis API)
        news_w_sent = process_funcs(search)

        # Unpacks the results from the function that sorts the results of the functions above for passing.
        neg_results, pos_results, positive_values, negative_values, a, b, c = sort_results(news_w_sent)

        # Grabs today's date and the date of 10 days ago. 
        today_date, last_10_date = get_date_range()

        stock_history = get_historical_prices()


        return render_template("results.html", neg_results=neg_results,
                               pos_results=pos_results, positive_values=positive_values,
                               negative_values=negative_values, a=a, b=b, c=c,
                               ticker=ticker, company_name=company_name, industry=industry, 
                               sector=sector, stock_history=stock_history, now=now)
    except AttributeError:
        return render_template("error.html")    

@app.route('/compareform')
def gather_comparing_comps():
    """Renders form for gathering 2 companies to compare."""

    return render_template("compareform.html")

@app.route('/comparisonresults')
def get_comparison_results():
    """Shows results of company comparison"""
    try:
        firstsearch = request.args.get("firstcompany")
        secondsearch = request.args.get("secondcompany")

        firstcompany = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == firstsearch).first()
        secondcompany = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == secondsearch).first()

        first_company_name, first_industry, first_sector, tickerone = get_company_info(firstsearch)
        session['symbolone'] = tickerone

        second_company_name, second_industry, second_sector, tickertwo = get_company_info(secondsearch)
        session['symboltwo'] = tickertwo

        first_news_w_sent = process_funcs(firstsearch)

        first_neg_results, first_pos_results, first_positive_values, first_negative_values, a1, b1, c1 = sort_results(first_news_w_sent)

        second_news_w_sent = process_funcs(secondsearch)

        second_neg_results, second_pos_results, second_positive_values, second_negative_values, a2, b2, c2 = sort_results(second_news_w_sent)

        return render_template("comparisonresults.html", first_neg_results=first_neg_results,
                               first_pos_results=first_pos_results, first_positive_values=first_positive_values,
                               first_negative_values=first_negative_values, 
                               a1=a1, b1=b1, c1=c1,
                               tickerone=tickerone, first_company_name=first_company_name, first_industry=first_industry,
                               first_sector=first_sector, 
                               second_neg_results=second_neg_results,
                               second_pos_results=second_pos_results, second_positive_values=second_positive_values,
                               second_negative_values=second_negative_values, 
                               a2=a2, b2=b2, c2=c2,
                               tickertwo=tickertwo, second_company_name=second_company_name, second_industry=second_industry,
                               second_sector=second_sector)

    except AttributeError:
        return render_template("error.html")  

@app.route('/currentstockprice')
def get_current_price():
    """Returns most current stock price"""

    finance_object = Share(session['symbol'])

    current_price = finance_object.get_price()

    return current_price

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run()
