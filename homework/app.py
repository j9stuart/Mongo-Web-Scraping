from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scraping"
mongo = PyMongo(app)


@app.route("/")
def index():

    # Find records of data from mongo database
    data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=data)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_scrape = mission_to_mars.get_data()

    # Update the Mongo database using update an upsert=True
    mongo.db.collection.update({}, mars_scrape, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)