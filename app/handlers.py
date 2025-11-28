from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generate import ai_generate

router = Router()


class Gen(StatesGroup):
    wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="*Добро пожаловать*, напишите ваш запрос")


@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="_Подождите, ваш запрос генерируется_.")


@router.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.bot.send_message(chat_id=message.chat.id, text="*Ваш запрос генерируется\\.\\.\\.*")
    try:
        response = await ai_generate(message.text)
        print(response)
        await message.answer(response, parse_mode="MarkdownV2")
    except Exception as e:
        await message.answer("К сожалению я не могу ответить на ваш вопрос :(")
    await state.clear()


