from flask import Blueprint, render_template, request, jsonify
from responses.question_answer_response import question_answer_response
from responses.learning_plan_response import learning_plan_response
from responses.motivation_response import motivation_response

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def index():
    return render_template('index.html')

@views_blueprint.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    current_tab = request.form['tab']

    if current_tab == 'question-answer':
        ai_response = question_answer_response(user_message)
    elif current_tab == 'learning-plan':
        ai_response = learning_plan_response(user_message)
    elif current_tab == 'motivation':
        ai_response = motivation_response(user_message)
    else:
        ai_response = "不明なタブです。"

    return jsonify({'response': ai_response})

