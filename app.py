import asyncio
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()
bot = Bot(token="token", parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


class Welcome(StatesGroup):
    name = State()


@dp.message_handler(lambda message: message.chat.type == "private", commands=['start'])
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(text="👋 <b>Добро пожаловать</b>")


@dp.message_handler(lambda message: message.chat.type == "private", text="Привет")
async def hello(message: types.Message, state: FSMContext):
    await Welcome.name.set()
    asyncio.create_task(wait_message(message, state), name=message.from_user.id)
    await message.answer(text="👋 <b>Привет, напиши своё имя</b>")


async def wait_message(message: types.Message, state: FSMContext):
    await asyncio.sleep(60)
    await state.finish()
    await message.answer("😔 <b>Жаль, что ты так и не ответил...</b>")


@dp.message_handler(state=Welcome.name, content_types=types.ContentTypes.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    await cancel_wait(message.from_user.id)
    await state.finish()
    await message.answer("😁 <b>Приятно познакомится, {}!</b>".format(message.text))


async def cancel_wait(task_id):
    for task in asyncio.all_tasks():
        if task.get_name() == task_id:
            task.cancel()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)