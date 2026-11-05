import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def run(task: str, context: dict) -> str:
    system_prompt = f"""
Você é um analista estratégico de marketing digital.
Escreva sempre em português brasileiro, de forma clara e objetiva.

CLIENTE: {context['name']}
SETOR: {context['sector']}
TOM DE VOZ: {context['tone']}
INSTRUÇÕES EXTRAS: {context.get('extra_instructions', 'Nenhuma.')}
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": f"{system_prompt}\n\nTarefa: {task}"}
        ],
    )

    return message.content[0].text.strip()
