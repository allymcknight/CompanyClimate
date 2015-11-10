from model import NASDAQNYSE

from model import connect_to_db, db
from server import app

def load_nasdaqnyse():
    """Load nasdaq info into database."""

    print "nasdaqnyse"

    NASDAQNYSE.query.delete()

    for row in open("seed_data/companylist.csv"):
        row = row.rstrip()
        row = row[:-1]
        row = row.replace('"', '')
        row_list = row.split(",")
        ticker_code, company_name = row_list[:2]
        bus_sector, bus_type = row_list[-3:-1]

        company_info = NASDAQNYSE(ticker_code=ticker_code, company_name=company_name,
                                  bus_sector=bus_sector, bus_type=bus_type)

        db.session.add(company_info)

    for row in open("seed_data/NYSE.csv"):
        row = row.rstrip()
        row = row[:-1]
        row = row.replace('"', '')
        row_list = row.split(",")
        ticker_code, company_name = row_list[:2]
        bus_sector, bus_type = row_list[-3:-1]

        company_info = NASDAQNYSE(ticker_code=ticker_code, company_name=company_name,
                                  bus_sector=bus_sector, bus_type=bus_type)

        db.session.add(company_info)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_nasdaqnyse()