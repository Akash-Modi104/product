from flask import current_app as app
from flask import jsonify, request
from src.controller.product_controller import add_product, get_all_products, purchase_or_sale, get_product_by_id, \
    delete_product_by_id,update_product_by_id


# Create a new product
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    result = add_product(data)
    if result:
        return jsonify({'message': 'Product created successfully'}), 201
    return jsonify({'message': 'failed'}), 400


# Retrieve all products
@app.route('/api/products', methods=['GET'])
def get_products():
    product_list = get_all_products()
    if product_list:
        return jsonify({'products': product_list}), 200
    return jsonify({'products': "something went wrong"}), 400


#
# Retrieve a specific product
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    result = get_product_by_id(product_id)
    if result:
        return jsonify(result), 200
    return jsonify("something went wrong"), 400


#
# Update a product
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    result = update_product_by_id(product_id,data)
    if result:
        return jsonify(result), 200
    return jsonify("something went wrong"), 400


# Delete a product
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = delete_product_by_id(product_id)
    if result:
        return jsonify(result), 200
    return jsonify("something went wrong"), 400


#
# Record a transaction (purchase or sale)
@app.route('/api/transactions', methods=['POST'])
def record_transaction():
    data = request.get_json()
    result = purchase_or_sale(data)
    return jsonify(result["message"])
