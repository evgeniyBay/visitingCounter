from flask import Flask, render_template, request, make_response
import json
import os

app = Flask(__name__)

if os.path.exists('visit_data.json'):
    with open('visit_data.json', 'r') as json_file:
        data = json.load(json_file)
        visit_data = {
            'total_visits': data['total_visits'],
            'unique_visits': set(data['unique_visits'])
        }
else:
    visit_data = {
        'total_visits': 0,
        'unique_visits': set()
    }

def save_visit_data():
    data = {
        'total_visits': visit_data['total_visits'],
        'unique_visits': list(visit_data['unique_visits'])
    }
    with open('visit_data.json', 'w') as json_file:
        json.dump(data, json_file)


@app.route('/')
def home():
    global visit_data
    visit_data['total_visits'] += 1
    client_ip = request.remote_addr

    if client_ip not in visit_data['unique_visits']:
        visit_data['unique_visits'].add(client_ip)

    response = make_response(render_template('index.html',
                                             visit_data=visit_data))

    save_visit_data()

    return response




if __name__ == '__main__':
    app.run(debug=True)
