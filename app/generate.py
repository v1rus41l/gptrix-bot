from openai import AsyncOpenAI

from dotenv import load_dotenv
import os
import re
import openai

load_dotenv()
client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("AI_TOKEN"),
)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def format_for_markdown_v2(text: str) -> str:
    """Форматирует текст для MarkdownV2"""
    
    # Если есть блоки кода с ```
    if '```' in text:
        parts = []
        segments = text.split('```')
        
        for i, segment in enumerate(segments):
            if i % 2 == 0:  # Обычный текст
                # Экранируем специальные символы
                parts.append(escape_markdown_v2(segment))
            else:  # Код внутри ```
                # Для блока кода не экранируем, используем монопространственный шрифт
                parts.append(f"```\n{segment}\n```")
        
        return ''.join(parts)
    else:
        # Просто экранируем весь текст
        return escape_markdown_v2(text)
    

async def ai_generate(text: str):
    completion = await client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
                {
                  "role": "system",
                  "content": "Ты телеграмм бот от GPTrix Space. В своих ответах категорически нельзя использовать markdown разметку (например ** и т.д.)\\. Для кода используй блоки с тройными обратными кавычками ```код```."
                },
                {
                  "role": "user",
                  "content": text
                }
              ]
    )
    response = completion.choices[0].message.content
    
    # Форматируем для MarkdownV2
    formatted_response = format_for_markdown_v2(response)
  
    return formatted_response