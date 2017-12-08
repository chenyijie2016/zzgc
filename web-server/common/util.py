GET_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET',
               'Access-Control-Allow-Headers': 'x-requested-with,content-type'}

POST_HEADERS = {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'x-requested-with,content-type'}

HEADERS = {'Access-Control-Allow-Origin': '*',
           'Access-Control-Allow-Methods': '*',
           'Access-Control-Allow-Headers': 'x-requested-with,content-type'}

User = {
    'username': None,
    'password': None,
    'email': None,
    'authority': None,
    'money': None,
    'orders': [],
    'card_id': None
}

Order = {
    'id':None,
    'date': None,
    'device_name': None,
    'number': None,
    'status': None
}
