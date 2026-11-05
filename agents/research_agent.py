import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def run(task: str, context: dict) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
Você é um pesquisador de marketing digital especializado no setor {context['sector']}.
Escreva sempre em português brasileiro.

CLIENTE: {context['name']}
SETOR: {context['sector']}

Sua tarefa: {task}

Formato da resposta:
1. Resumo do que foi pesquisado (2-3 parágrafos)
2. 5 insights ou tendências relevantes (lista numerada)
3. 3 sugestões de pauta para redes sociais baseadas na pesquisa
"""

    response = model.generate_content(prompt)
    return response.text.strip()
