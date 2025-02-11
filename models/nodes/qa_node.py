import os
from dotenv import load_dotenv
from flask import session

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from lib.clearn_text import cleanup_text
from models.states.qa_state import QAState
from models.prompts.qa_prompt import (
    get_answer_explanation_prompt,
    get_explanation_quality_check_prompt,
    get_problem_maker_prompt,
    get_problem_quality_check_prompt,
    get_decision_prompt
    )

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", "")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, openai_api_key=openai_api_key)

def decide_flow_node(state: QAState) -> dict:
    prompt = get_decision_prompt()

    chain = prompt | llm | StrOutputParser()
    classification = chain.invoke({"query": state.query})

    if "answer" in classification.lower():
        flow = "answer"
    else:
        flow = "problem"

    return {"current_flow": flow}


def problem_flow_node(state: QAState) -> QAState:
    problem_prompt = get_problem_maker_prompt(state.query)
    chain1 = problem_prompt | llm | StrOutputParser()
    problem_raw = chain1.invoke({})

    problem_raw = cleanup_text(problem_raw)

    problem_quality_check_prompt = get_problem_quality_check_prompt(problem_raw)
    problem_quality_check_chain = problem_quality_check_prompt | llm | StrOutputParser()
    check_result = problem_quality_check_chain.invoke({})

    check_result = cleanup_text(check_result)

    final_problem_text = problem_raw
    if "修正案:" in check_result:
        splitted = check_result.split("修正案:")
        if len(splitted) > 1:
            corrected_text = splitted[1].strip()
            if corrected_text:
                final_problem_text = corrected_text

    state.problem_text = final_problem_text
    state.final_message = final_problem_text

    session["latest_problem_text"] = final_problem_text

    return state

def answer_flow_node(state: QAState) -> QAState:
    state.user_answer = state.query

    prev_problem = session.get("latest_problem_text", "")
    if not prev_problem:
        state.final_message = "前回の問題が見つかりません。先に問題を出題してください。"
        return state

    answer_explanation_prompt = get_answer_explanation_prompt(prev_problem, state.user_answer)
    answer_explanation_chain = answer_explanation_prompt | llm | StrOutputParser()
    explanation_raw = answer_explanation_chain.invoke({})
    explanation_raw = cleanup_text(explanation_raw)

    explanation_quality_check_prompt = get_explanation_quality_check_prompt(explanation_raw)
    explanation_quality_check_chain = explanation_quality_check_prompt | llm | StrOutputParser()
    check_result = explanation_quality_check_chain.invoke({})

    final_explanation_text = explanation_raw
    if "修正案:" in check_result:
        splitted = check_result.split("修正案:")
        if len(splitted) > 1:
            corrected_text = splitted[1].strip()
            if corrected_text:
                final_explanation_text = corrected_text

    final_explanation_text = cleanup_text(final_explanation_text)

    state.explanation_text = final_explanation_text
    state.final_message = final_explanation_text

    return state
