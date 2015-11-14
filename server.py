from jinja2 import StrictUndefined
from flask import Flask, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from projectOHYEAH import run_googlenews_api, article_scraper, analyze_sentiment, sort_results
from model import NASDAQNYSE, connect_to_db
from yahoo_finance import Share
from datetime import timedelta, datetime
from collections import OrderedDict

app = Flask(__name__)

app.secret_key = "ABCsgerhysdvc8c9u4wf"

app.jinja_env.undefined = StrictUndefined

def get_date_range():
    """Using Datetime, grabs the current date and the date of 10 days ago."""

    today = datetime.now()
    ten = timedelta(days=365)
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

    today, last_10_date = get_date_range()
    finance_object = Share(session['symbol'])
    history = finance_object.get_historical(last_10_date, today)

    stock_history = OrderedDict()
    for i in range(len(history)):
        stock_history[history[i]['Adj_Close']] = i


    return stock_history


@app.route('/')
def index():
    """Renders homepage."""

    return render_template("home.html")


@app.route('/results')
def search_results():
    """Renders page with results of search and sentiment analysis."""
    # Grabs the search item with a get request.
    search = request.args.get("search")

    # Querys my database for the search company's object.
    company = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == search).first()
    # Stores the ticker code in the session.
    ticker = company.ticker_code
    session['symbol'] = ticker
    # Grabs even more information about the company from the database.
    company_name = company.company_name
    industry = company.bus_sector
    sector = company.bus_type

    # Runs the search value through the functions (google API, web scraper, sentiment analysis API)
    news = run_googlenews_api(search)
    news_with_article_body = article_scraper(news)
    news_w_sent = analyze_sentiment(news_with_article_body)

    # Unpacks the results from the function that sorts the results of the functions above for passing.
    neg_results, pos_results, positive_values, negative_values, a, b, c = sort_results(news_w_sent)

    # Grabs today's date and the date of 10 days ago. 
    today_date, last_10_date = get_date_range()

    stock_history = get_historical_prices()


    return render_template("results.html", neg_results=neg_results,
                           pos_results=pos_results, positive_values=positive_values,
                           negative_values=negative_values, a=a, b=b, c=c,
                           ticker=ticker, company_name=company_name, industry=industry, 
                           sector=sector, stock_history=stock_history)

@app.route('/compareform')
def gather_comparing_comps():
    """Renders form for gathering 2 companies to compare."""

    return render_template("compareform.html")

@app.route('/comparisonresults')
def get_comparison_results():
    """Shows results of company comparison"""

    firstsearch = request.args.get("firstcompany")
    secondsearch = request.args.get("secondcompany")

    firstcompany = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == firstsearch).first()
    secondcompany = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == secondsearch).first()

    tickerone = firstcompany.ticker_code
    tickertwo = secondcompany.ticker_code

    session['symbolone'] = tickerone
    session['symboltwo'] = tickertwo

    first_company_name = firstcompany.company_name
    first_industry = firstcompany.bus_sector
    first_sector = firstcompany.bus_type

    second_company_name = secondcompany.company_name
    second_industry = secondcompany.bus_sector
    second_sector = secondcompany.bus_type

    first_news = run_googlenews_api(firstsearch)
    first_news_with_article_body = article_scraper(first_news)
    first_news_w_sent = analyze_sentiment(first_news_with_article_body)

    first_neg_results, first_pos_results, first_positive_values, first_negative_values, a1, b1, c1 = sort_results(first_news_w_sent)

    second_news = run_googlenews_api(secondsearch)
    second_news_with_article_body = article_scraper(second_news)
    second_news_w_sent = analyze_sentiment(second_news_with_article_body)

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
