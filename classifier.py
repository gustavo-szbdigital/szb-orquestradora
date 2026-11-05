from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você é um classificador de tarefas para uma agência de marketing digital.
Dado um pedido, responda APENAS com uma dessas palavras exatas:
- copy       → se for criar texto, legenda, post, caption, CTA, roteiro
- research   → se for pesquisar tendências, dados, concorrentes, pautas
- analysis   → se for relatório, diagnóstico, estratégia, auditoria, análise

Responda somente a palavra, sem pontuação, sem explicação.
"""

async def classify_task(task: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ],
        max_tokens=10,
        temperature=0,
    )
    result = response.choices[0].message.content.strip().lower()

    if result not in ("copy", "research", "analysis"):
        return "copy"

    return result
