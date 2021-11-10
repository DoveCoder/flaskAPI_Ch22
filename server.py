from flask import Flask, abort, render_template, request
from mock_data import mock_data
from flask_cors import CORS
from config import db, json_parse
from config import db
import json
from bson import ObjectId

# notes

app = Flask(__name__) # magic variable (name)
print(__name__)
CORS(app) # allow anyone to call the server (**Danger**)

coupon_codes = [ 
    {
        "code": "qwerty",
        "discount": 10
    }
]

me = {
    "name": "Jimmy",
    "last": "Newtron",
    "age": 50,
    "email": "AlienInvasion@N64.com",
    "hobbies": [],
    "address": {
        "street": "EverGreen",
        "city": "Springfield",
    }
}


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about") # route should always start with a /
def about():
    # return full name from dictionary
    return render_template("about.html")

@app.route("/about/email")
def email():
    return me["email"]

@app.route("/about/address")
def address():
    return me["address"]["street"] + " " + me["address"]["city"]

@app.route("/test")
def test():
    return "Hello there!"



#############################
###### API Methods
#############################


@app.route("/api/catalog", methods=['GET'])
def get_catalog():
    # return json_parse(mock_data)
    cursor = db.products.find({})

    catalog = []
    for prod in cursor:
        catalog.append(prod)
    
    print( len(catalog) , "Records obtained from the database")

    return json_parse(catalog)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    # get request payload (body)
    product = request.get_json()

    # data validation 
    # 1 title exist and is longer than 5 chars
    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should contains at least 5 chars") # 400 = bad request

    # if not 'price' in product or not isinstance(product['price'], float) <= 0:
    #     return about(400, "Price is required, and should be a positive number > 0") # 400 = bad request

    if not 'price' in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should a valid float number")

    if product['price'] <= 0:
        return abort(400,"Price should be greater than 0")

    ## validate that title exist in the dic, if not abort(400)

    #save the product
    # mock_data.append(product)
    # product["_id"] = len(product["title"])

    # Save product with Mongo DB
    db.products.insert_one(product)

    return json_parse(product)

## /api/categories
#returns the list (string) of UNIQUE categories

@app.route("/api/categories")
def get_categories():
    cursor = db.products.find({}) # database cursor (from db)

    categories = []
    for prod in cursor:
        if prod["category"] not in categories:
            categories.append(prod["category"])
    return json_parse(categories) # logic
        

@app.route("/api/product/<id>")
def get_product(id):
    product = db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return abort(404)

    return json_parse(product)



@app.route("/api/catalog/<category>")
def get_category(category):
    # mongo to search case sensitive we use Regular Expressions
    cursor = db.products.find({"category": category})
    category_list = []

    for prod in cursor:
        category_list.append(prod)
    return json_parse(category_list)


@app.route("/api/cheapest")
def cheapest():
    cursor = db.products.find({})
    pivot = cursor[0]
    for prod in cursor:

        if prod['price'] < pivot["price"]:
            pivot = prod
    return json_parse(pivot)
             


##########################
####  Coupon Codes #######
##########################

# Post to /api/couponCodes
@app.route("/api/couponCodes", methods=["POST"])
def post_coupon():
    
    coupon = request.get_json()

    # validations
    db.couponCodes.insert_one(coupon)
    return json_parse(coupon)
    #save
    # coupon_codes.append(coupon)
    # coupon["_id"] = coupon["code"]
    # return json_parse(coupon)

# Get to /api/couponCodes
@app.route("/api/couponCodes", methods=["GET"])
def get_coupon():
    cursor = db.couponCodes.find({})
    all_coupons = []
    for cc in cursor:
        all_coupons.append(cc)

        return json_parse(all_coupons)

@app.route("/api/couponCouponCodes/<code>")
def get_coupon_by_code(code):
    coupon = db.couponCodes.find_one({"code": code})
    if coupon is None:
        return abort(404, "Invalid coupon code")  

    return json_parse(coupon)

@app.route("/test/onetime/filldb")
def fill_db():
    product = []
    
    for prod in mock_data:
        prod.pop("_id") # removes the id 
        db.products.insert_one(prod) # stores in a new list
    return "Done"

# start the server
# debug true will restart the server automatically
app.run(debug=True)