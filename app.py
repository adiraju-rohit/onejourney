from flask import Flask, render_template, request, jsonify
import modl, os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'nextop')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tracker')
def tracker():
    routes = modl.get_all_routes()
    return render_template('tracker.html', routes=routes)

@app.route('/api/routes')
def api_routes():
    return jsonify(modl.get_all_routes())

@app.route('/api/stops/<route_id>')
def api_stops(route_id):
    return jsonify(modl.get_stops(route_id))

@app.route('/api/nearby')
def api_nearby():
    try:
        route_id  = request.args.get('route_id', '')
        lat       = float(request.args.get('lat', 0))
        lng       = float(request.args.get('lng', 0))
        threshold = float(request.args.get('threshold', 1.0))
        nearby    = modl.get_nearby_stops(lat, lng, route_id, threshold)
        stops     = modl.get_stops(route_id)
        return jsonify({'nearby': nearby, 'all_stops': stops})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
