from src.models.products import Product, Stock, Transaction
from src.database.intialize_database import db
import logging

log = logging.getLogger(__name__)


def add_product(data: dict):
    try:
        log.info("adding product")
        # Create a new product
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price']
        )

        # Add the product to the database
        db.session.add(new_product)
        # db.session.commit()

        # Check if 'stock' is present in the data dictionary
        stock_data = data.get('stock', {})
        quantity = stock_data.get('quantity', 0)

        # Create stock entry for the new product
        new_stock = Stock(quantity=quantity, product=new_product)

        # Add the stock to the database
        db.session.add(new_stock)
        # db.session.commit()
        purchase_transaction = Transaction(
            product=new_product,
            quantity=quantity,
            transaction_type='purchase'
        )

        # Add the purchase transaction to the database
        db.session.add(purchase_transaction)
        db.session.commit()
        log.info("Product Added")

        return True
    except Exception as e:
        log.error(e,exc_info=True)
        db.session.rollback()  # Rollback the changes if an error occurs
        return False


def get_all_products():
    try:
        products = Product.query.all()
        return [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.stock.quantity,
            }
            for product in products
        ]
    except Exception as e:
        log.error(e,exc_info=True)
        return []


def get_product_by_id(product_id):
    try:
        log.info(f"getting details for product_id :- {product_id}")
        product = Product.query.get_or_404(product_id)
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'quantity': product.stock.quantity,
        }
        log.info("details found")
        return {'product': product_data}
    except Exception as e:
        log.error(e,exc_info=True)
        return {}


def update_product_by_id(product_id, data):
    try:
        # Update product information
        log.info(f"updating product :- {product_id}")
        product = Product.query.get_or_404(product_id)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        db.session.commit()
        log.info("updated product")
        return {'message': 'Product updated successfully'}
    except Exception as e:
        log.error(e,exc_info=True)
        return {}


def delete_product_by_id(product_id):
    try:
        log.info(f"deleting product :- {product_id}")
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        log.info("deleted product")
        return {'message': 'Product deleted successfully'}
    except Exception as e:
        log.error(e,exc_info=True)
        return {}



def purchase_or_sale(data: dict):
    try:
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        transaction_type = data.get('transaction_type')

        log.info(f"transaction_type-{product_id},quantity {quantity}, type:- {transaction_type}")

        # Retrieve the product
        product = Product.query.get_or_404(product_id)

        # Update stock quantity based on the transaction type
        if transaction_type == 'purchase':
            product.stock.quantity += quantity
        elif transaction_type == 'sale':
            if quantity > product.stock.quantity:
                return {'message': 'Insufficient stock for sale', "status": False}
            product.stock.quantity -= quantity
        else:
            return {'message': 'Invalid transaction type', "status": False}

        # Record the transaction
        transaction = Transaction(
            product=product,
            quantity=quantity,
            transaction_type=transaction_type,
        )
        db.session.add(transaction)
        db.session.commit()
        log.info("transaction")
        return {'message': 'Transaction recorded successfully', "status": True}
    except Exception as e:
        log.error(e,exc_info=True)
        db.session.rollback()  # Rollback the changes if an error occurs
        return {'message': e, "status": False}
