

class Order:

    def __init__(self, name, quantity, wanted_in, customer, location):
        self.name = name
        self.quantity = quantity
        self.time = wanted_in
        self.customer = customer
        self.location = location

class Orders:

    def __init__(self):
        self.orders = []
        self.n = 1
    
    def check(self, order_id):
        for order in self.orders:
            if order['id'] == order_id:
                return order

        return False

    def not_found(self, order_id):
        return 'Order with Id: {} not found.'.format(order_id)

    def status(self, order_id, state):
        if state =='Q':
            state = 'Queued'
        elif state == 'P':
            state = 'Pending'
        elif state == 'C':
            state = 'Completed'
        else:
            state = 'Undefined'

        order = self.check(order_id)
        if order is False:
            self.not_found(order_id)
        else:
            order['status'] = state
    
    def success(self, act, order_id):
        if act == 'P':
            act = 'placed'
        elif act == 'U':
            act == 'updated'

        return 'Your order was successfully {}. Order Id: {}'.format(act,order_id)

    def place_order(self, order):
        sheet = {'id': self.n, 'name': order.name, 'quantity': order.quantity, 'wanted_in': order.time, 
                  'requester': order.customer, 'where': order.location}

        order_id = self.n
        self.orders.append(sheet)
        self.status(self.n,'Q')
        self.n += 1

        self.success('P', order_id)

    def get_order(self, order_id):
        order = self.check(order_id)
        if order is False:
            self.not_found(order_id)
        else:
            return order

    def update_order(self, order_id, state):
        order = self.check(order_id)
        if order is False:
            self.not_found(order_id)
        else:
            self.status(order_id, state)
            self.success('U', order_id)

    def all_orders(self):
        return self.orders