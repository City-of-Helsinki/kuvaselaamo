

class BasketLine(object):
    def __init__(self, basket, data=None):
        self.basket = basket
        self.data = data or {}

    def __repr__(self):
        return '<BasketLine %r>' % self.data

    def __getattr__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def add_quantity(self, quantity):
        self.data['quantity'] = int(max(0, self.data['quantity'] + quantity))


    # def cache_info(self, request):
    #     product = self.product
    #     self.data['taxful_unit_price'] = self.product.price
    #     self.data

    line_id = property(lambda self: self.data['line_id'])
    name = property(lambda self: self.text)
    product = property(lambda self: self.basket.get_product(self.product_id))
    line_details = property(lambda self: self.basket.get_line_details(self.order_pk))
    total_price = property(lambda self: self.product.price * self.quantity)
