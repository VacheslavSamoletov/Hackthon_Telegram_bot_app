import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from firebase import ref
# Включение логирования
logging.basicConfig(level=logging.INFO)
# Инициализация бота и диспетчера
bot = Bot(token='6549467564:AAG8_dsFHNrJBsr459C4avVJqkb-Rl9jBuo')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class TextState(StatesGroup):
    waiting_for_text = State()
class LocationState(StatesGroup):
    waiting_for_location = State()
class AddTrashState(StatesGroup):
    waitingfordata = State()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Волонтеру ", "Добавить свалку"]
    keyboard.add(*buttons)
    await message.answer("Добро пожаловать в бот", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text=="Волонтеру")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")


@dp.message_handler(lambda message: message.text == "Добавить свалку")
async def without_puree(message: types.Message):
    await message.reply("Добавьте информацию о свалке")
    keyboardADD_TRASH = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonsADD_TRASH = ["Фото", "Текст", "Локация"]
    keyboardADD_TRASH.add(*buttonsADD_TRASH)
    await message.answer("Какие данные хотите внести?", reply_markup=keyboardADD_TRASH)


# @dp.message_handler(commands="geo" ,content_types=types.ContentTypes.LOCATION)
# async def get_geocode(message: types.Message):
#     g location = list(dict(message.location).values())

@dp.message_handler(commands="repeat")
async def get_last_message(message: types.Message):
    last_message = message.text
    await message.reply(f"Последнее сообщение: {last_message}")

#
# @dp.message_handler(lambda message: message.text == "Текст")
# async def handle_text(message: types.Message):
#     # Получаем данные из сообщения
#     await message.reply("Добавьте описание свалки ----->")
#     print(get_last_message(message))
#
#
#     text = message.text
#     chat_id = message.chat.id
#     # Сохраняем данные в Firebase
#     ref.child(f'chats/{chat_id}/messages').push().set({'text': text})
#     # Отправляем ответное сообщение
#     await message.reply('Сообщение сохранено в Firebase!')

@dp.message_handler(lambda message: message.text == "Добавить свалку")
async def without_puree(message: types.Message, state: FSMContext):
    await AddTrashState.waiting_for_data.set()
    await message.reply("Добавьте информацию о свалке")
    keyboardADD_TRASH = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonsADD_TRASH = ["Фото", "Текст", "Локация"]
    keyboardADD_TRASH.add(*buttonsADD_TRASH)
    await message.answer("Какие данные хотите внести?", reply_markup=keyboardADD_TRASH)


@dp.message_handler(state=TextState.waiting_for_text)
async def handle_waiting_for_text(message: types.Message, state: FSMContext):
    # Получаем данные из сообщения
    text = message.text
    chat_id = message.chat.id

    # Сохраняем данные в Firebase
    ref.child(f'chats/{chat_id}/messages').push().set({'text': text})

    # Отправляем ответное сообщение
    await message.reply('Сообщение сохранено в Firebase!')

    # Сбрасываем состояние
    await state.finish()

# @dp.message_handler(lambda message: message.text == "Фото")
# async def handle_photo(message: types.Message):
#     # Получаем данные из фотографии
#     await message.reply("Добавьте фотографию свалки ----->")
#     photo_id = message.photo[-1].file_id
#     chat_id = message.chat.id
#     # Сохраняем данные в Firebase
#     ref.child(f'chats/{chat_id}/photos').push().set({'photo_id': photo_id})
#     # Отправляем ответное сообщение
#     await message.reply('Фотография сохранена в Firebase!')

@dp.message_handler(lambda message: message.text == "Фото")
async def handle_photo(message: types.Message):
    if message.photo:
        # Получаем данные из фотографии
        await message.reply("Добавьте фотографию свалки ----->")
        photo_id = message.photo[-1].file_id
        chat_id = message.chat.id
        # Сохраняем данные в Firebase
        ref.child(f'chats/{chat_id}/photos').push().set({'photo_id': photo_id})
        # Отправляем ответное сообщение
        await message.reply('Фотография сохранена в Firebase!')
    else:
        # If no photo is attached, handle the error
        await message.reply('Пожалуйста, прикрепите фотографию свалки.')


@dp.message_handler(lambda message: message.text == "Локация")
async def handle_location(message: types.Message):
    # Получаем данные из сообщения
    await message.reply("Добавьте геометку свалки----->")
    # Устанавливаем состояние ожидания геометки
    await LocationState.waiting_for_location.set()
@dp.message_handler(content_types=types.ContentType.LOCATION, state=LocationState.waiting_for_location)
async def handle_waiting_for_location(message: types.Message, state: FSMContext):
    # Получаем данные о геометке
    latitude = message.location.latitude
    longitude = message.location.longitude
    # Сохраняем данные в Firebase
    chat_id = message.chat.id
    ref.child(f'chats/{chat_id}/locations').push().set({'latitude': latitude, 'longitude': longitude})
    # Отправляем ответное сообщение
    await message.reply('Локация сохранена в Firebase!')
    await state.finish()


if __name__ == '__main__':
    # Запуск бота
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)