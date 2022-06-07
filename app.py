import requests as httpClient
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#import os



app = Flask(__name__)

#basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'  #+ os.path.join(basedir, 'weather.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'city', 'temperature', 'description')

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)
   

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=63319dd07403648f07b9698cf116c1a3'
    
    new_city = request.form.get('city')

        
    try:
        r = httpClient.get(url.format(new_city)).json()
        weather = {
                'city' : new_city,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                    }
            
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
               

        return product_schema.jsonify(weather)
    

    except:
        return "Code: 404 - City not found"
            

    

        
        #cities = City.query.distinct()
        

       

        #weather_data = []

        #for city in cities:

        
        #weather_data.append(weather)
            
        
        
        

    # name = request.json['name']
    # description = request.json['description']
    # price = request.json['price']
    # qty = request.json['qty']

    # new_product = Product(name, description, price, qty)

    #return r
    #print (weather)

  
    
    


        



#from app import routes