from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Инициализация счетчиков
visit_data = {
    'total_visits': 0,
    'unique_visits': set()
}


@app.route('/')
def home():
    global visit_data
    visit_data['total_visits'] += 1
    session_id = request.cookies.get('session_id')

    if session_id is not None:
        if session_id not in visit_data['unique_visits']:
            visit_data['unique_visits'].add(session_id)

    response = make_response(render_template('index.html',
                                             visit_data=visit_data))
    if session_id is None:
        session_id = str(hash(request.user_agent))
        response.set_cookie('session_id', session_id)
    return response


if __name__ == '__main__':
    app.run(debug=True)
