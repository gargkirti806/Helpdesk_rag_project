STRICT_INTENT_PROMPT = """
Classify the following user query into one of the two categories:
- HR_Policy (e.g., leave policy, holidays, maternity leave, appraisal)
- IT_guidelines (e.g., laptop issues, VPN, password reset, software access)

Return ONLY the category name (HR_Policy or IT_guidelines).

Question: {question}
"""
STRICT_RAG_PROMPT = """You are a strict RAG assistant. Only answer based on the given context.
Do not use any external knowledge or make assumptions.

Context:
{context}

Question:
{question}

Answer strictly from the context:"""