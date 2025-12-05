from app.llm.llm_factory import get_answer_generation_llm
from app.llm.prompts import STRICT_RAG_PROMPT

def generate_answer(state):
    context = "\n\n".join([d.page_content for d in (state.compressed_docs or [])])
    prompt = STRICT_RAG_PROMPT.format(context=context, question=state.user_query)
    llm = get_answer_generation_llm()
    # use invoke like original; respect temp=0 in factory


    response = llm.invoke(prompt)
     
    state.kb_answer = response.answer
    return state
