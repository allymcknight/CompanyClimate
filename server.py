from jinja2 import StrictUndefined
from flask import Flask, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from projectOHYEAH import run_googlenews_api, article_scraper, analyze_sentiment, sort_results
from model import NASDAQNYSE, connect_to_db
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
    session['symbol'] = ticker

    company_name = company.company_name
    industry = company.bus_sector
    sector = company.bus_type

    stock = Share(ticker)
    stock_closing_price = stock.get_open()

    news = run_googlenews_api(search)
    news_with_article_body = article_scraper(news)
    news_w_sent = analyze_sentiment(news_with_article_body)

    neg_results, pos_results, positive_values, negative_values, a, b, c = sort_results(news_w_sent)

    return render_template("results.html", neg_results=neg_results,
                           pos_results=pos_results, positive_values=positive_values,
                           negative_values=negative_values, a=a, b=b, c=c,
                           ticker=ticker, stock_closing_price=stock_closing_price,
                           company_name=company_name, industry=industry, sector=sector)

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
