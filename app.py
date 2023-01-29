from flask import Flask
import sys
from housing.logger import logging
from housing.exception import HousingExceptions



app=Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    return "CI CD pipeline has been established."


if __name__=="__main__":
    app.run(debug=True)
