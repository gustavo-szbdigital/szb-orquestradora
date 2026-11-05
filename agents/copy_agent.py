from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run(task: str, context: dict) -> str:
    system_prompt = f"""
Você é um redator especialista em marketing digital para redes sociais.
Escreva sempre em português brasileiro.

CLIENTE: {context['name']}
SETOR: {context['sector']}
TOM DE VOZ: {context['tone']}
INSTRUÇÕES EXTRAS: {context.get('extra_instructions', 'Nenhuma.')}

Suas regras:
- Sempre gere 3 variações numeradas (1., 2., 3.)
- Cada legenda deve ter no máximo 150 palavras
- Inclua de 3 a 5 hashtags relevantes ao final de cada variação
- Adapte o tom de voz do cliente em cada variação
"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ],
        max_tokens=1000,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()
