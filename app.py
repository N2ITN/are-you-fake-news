from chalice import Chalice

app = Chalice(app_name='fakenewsapp')

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/cities/{city}')
def state_of_city(city):
    return {'state': CITIES_TO_STATE[city]}
