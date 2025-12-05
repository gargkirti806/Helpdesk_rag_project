# app/pipeline/nodes/postprocess_node.py

from app.original.langraph_pipeline_typed_original import PipelineState
from app.utils.ticket import create_ticket_api  # helper for creating tickets

def postprocess(state: PipelineState) -> PipelineState:
    """
    Post-processing node: decides final response, ticket creation, escalation.
    """
    response = {}

    # KB answer
    if state.eval_sufficient:
        response["answer"] = state.kb_answer
    else:
        response["answer"] = "KB answer insufficient. Escalating to human/HR."

    # Ticket creation logic
    create_ticket = False
    ticket_summary = None

    if state.intent == "IT_guidelines":
        create_ticket = True
        ticket_summary = f"IT Ticket for user query: {state.user_query}"
    elif state.intent == "HR_Policy":
        if not state.eval_sufficient:
            create_ticket = True
            ticket_summary = f"HR Ticket for user query: {state.user_query}"

    if create_ticket:
        ticket_id = create_ticket_api(ticket_summary)
        response["ticket_id"] = ticket_id
        response["ticket_summary"] = ticket_summary

    # Escalation if KB answer insufficient
    if not state.eval_sufficient:
        response["escalation"] = "Human/HR team assigned"
        response["reason"] = state.eval_reason

    state.final_response = response
    return state
