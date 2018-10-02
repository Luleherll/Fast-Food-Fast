class Check:

    def clean(self, container):
        u = {'username': 'lule', 'password': 'dev', 'tel': '07777',
         'email': 'lule@dev.com', 'location': 'Nalya',
         'key_point': 'Acacia mall entrance'}
    """x = Users().register(u)
    print(x)"""
        y = {'name': 'rice', 'status': 'Available',
         'tags': '  meal  '}
        x = {'user_id': '17', 'food_id': '2', 'name': 'rice',
         'quantity': '2', 'comment': 'hurry',
         'location': 'Nalya', 'amount': '4000'}
        new_container = {}
        try:
            for key in container:
                value = str(container[key]).strip(' ')
                if value == '':
                    raise KeyError
                else:
                    new_container[key] = value
        except KeyError:
            return '[{}] is empty or missing.'.format(key)
        return new_container