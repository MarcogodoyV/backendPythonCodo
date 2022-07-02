from math import prod
from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products


@app.route("/products", methods=["GET"])
def getProducts():
    return jsonify({"message": "Product's list", "products": products})


@app.route("/products/<string:product_name>", methods=["GET"])
def getProduct(product_name):
    productFound = [product for product in products if product["name"] == product_name]
    if len(productFound) > 0:
        print(productFound)
        return jsonify({"message": "Product found", "product": productFound})
    else:
        return {"message": "Product not found"}


@app.route("/products", methods=["POST"])
def addProduct():
    new_product = {
        "name": request.json["name"],
        "price": request.json["price"],
        "quantity": request.json["quantity"],
    }
    products.append(new_product)
    return jsonify({"message": "Product Added to List", "product": products})


@app.route("/products/<string:product_name>", methods=["PUT"])
def editProduct(product_name):
    productFound = [product for product in products if product["name"] == product_name]
    if len(productFound) > 0:
        if request.json["name"] != "":
            productFound[0]["name"] = request.json["name"]

        if request.json["price"] != "" and request.json["price"] >= 0:
            productFound[0]["price"] = request.json["price"]

        if request.json["quantity"] > -1:
            productFound[0]["quantity"] = request.json["quantity"]

        return jsonify(
            [{"message": "Product Updated", "Product": productFound}, products]
        )
    else:
        return jsonify({"message": "Product not found"})


@app.route("/products/<string:product_name>", methods=["DELETE"])
def deleteProduct(product_name):
    productFound = [product for product in products if product["name"] == product_name]

    if len(productFound) > 0:
        products.remove(productFound[0])
        return jsonify(
            {
                "message": "Product Removed " + productFound[0]["name"],
                "products": products,
            }
        )
    else:
        return jsonify({"message": "Product not found"})


if __name__ == "__main__":
    app.run(debug=True, port=4000)
