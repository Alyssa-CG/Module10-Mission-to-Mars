from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# initialise Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# # app.config["MONGO_URI"] tells Python that our app will connect to 
# # Mongo using a URI, a uniform resource identifier similar to a URL.
# # "mongodb://localhost:27017/mars_app" is the URI we’ll be using to 
# # connect our app to Mongo. This URI is saying that the app can reach 
# # Mongo through our localhost server, using port 27017, using a 
# # database named
# # mars_app”.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# run Flask
if __name__ == "__main__":
   app.run()
   