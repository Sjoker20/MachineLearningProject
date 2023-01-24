from flask import Flask
import sys
from housing.logger import logging
from housing.exception import HousingExceptions



app=Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("We are raisisng an exception intensioly to validate the code.")
    except Exception as e:
        housing = HousingExceptions(e,sys) from e
        logging.info(housing.error_message)
        logging.info("We are creating logging module")
    return "CI CD pipeline has been established."


if __name__=="__main__":
    app.run(debug=True)
