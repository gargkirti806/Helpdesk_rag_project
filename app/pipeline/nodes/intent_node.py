# -------------------------
# intent_node.py
# -------------------------

from app.llm.llm_factory import get_intent_llm
from app.llm.prompts import STRICT_INTENT_PROMPT  # define a prompt template for intent classification

def classify_intent(state):
    """
    Node to classify user query intent as HR_Policy or IT_guidelines
    Updates `state.intent`
    """
    llm = get_intent_llm()  # get LLM instance from factory

    # Build prompt using the query
    prompt = STRICT_INTENT_PROMPT.format(question=state.user_query)
    response = llm.invoke(prompt)
    
    state.intent = response.Intent
    
    return state
