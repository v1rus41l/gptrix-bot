from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.enums import ParseMode, ChatMemberStatus

from app.generate import ai_generate

from bot_create import bot
from dotenv import load_dotenv
import os

router = Router()

async def is_subscribed(user_id: int) -> bool:
    try:
        load_dotenv()
        member = await bot.get_chat_member(chat_id=os.getenv('CHAT_ID'), user_id=user_id)
        # Проверяем статус подписки
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

class Gen(StatesGroup):
    wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text='''✨ Приветствую! Ты только что нашел самого умного бота в Telegram — здесь живет ChatGPT!

📌 Правила просты:
1. Подпишись на наш канал: https://t.me/gptrix_space
2. Оставайся с нами и следи за новостями))

И сразу получишь:
• Мгновенные ответы на любые вопросы
• Помощь в учебе, работе и творчестве
• Генерацию текстов, кода, идей

🔥 Не теряй времени — подпишись и вливайся в мир AI!''')


@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="_Подождите, ваш запрос генерируется_.", parse_mode=ParseMode.MARKDOWN_V2)


@router.message()
async def generating(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await state.set_state(Gen.wait)
        await message.bot.send_message(chat_id=message.chat.id, text="*Ваш запрос генерируется\\.\\.\\.*", parse_mode=ParseMode.MARKDOWN_V2)
        try:
            response = await ai_generate(message.text)
            print(response)
            await message.answer(response, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            await message.answer("К сожалению я не могу ответить на ваш вопрос")
        await state.clear()
    else:
        await message.answer("Чтобы пользоваться ботом, необходимо подписаться на канал\n 👉https://t.me/gptrix_space")


