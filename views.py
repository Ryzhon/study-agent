from flask import Blueprint, request, jsonify, render_template
from markdown import markdown

from models.workflows.qa_workflow import build_qa_workflow
from models.states.qa_state import QAState

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/chat')
def chat():
    return render_template('chat.html')

@views_blueprint.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message', '')

    qa_workflow = build_qa_workflow()
    compiled = qa_workflow.compile()

    current_state = QAState(query=user_message)

    result_dict = compiled.invoke(current_state)
    final_state = QAState(**result_dict)

    return jsonify({
        "output": markdown(final_state.final_message),
        "problem_text": markdown(final_state.problem_text),
        "explanation_text": markdown(final_state.explanation_text)
    })
