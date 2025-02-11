from langgraph.graph import StateGraph

from models.states.qa_state import QAState
from models.nodes.qa_node import decide_flow_node, problem_flow_node, answer_flow_node

def build_qa_workflow() -> StateGraph:
    workflow = StateGraph(QAState)

    workflow.add_node("DecideFlowNode", decide_flow_node)
    workflow.add_node("ProblemFlowNode", problem_flow_node)
    workflow.add_node("AnswerFlowNode", answer_flow_node)

    workflow.set_entry_point("DecideFlowNode")

    workflow.add_conditional_edges(
        "DecideFlowNode",
        lambda output: "ProblemFlowNode" if output.current_flow == "problem"
                       else "AnswerFlowNode" if output.current_flow == "answer"
                       else None
    )

    return workflow
