from flask import Blueprint, render_template, request, jsonify
from flask import request, jsonify
from langchain.chains.llm import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/chat')
def chat():
    return render_template('chat.html')

@views_blueprint.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']

    system_template = SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant."
    )
    user_template = HumanMessagePromptTemplate.from_template("{query}")

    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])

    chat_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = LLMChain(
        llm=chat_model,
        prompt=chat_prompt
    )

    result = chain({"query": user_message})

    final_response = result["text"]
    return jsonify({'response': final_response})

