import logging
from aiogram import Bot, Dispatcher, executor, types
from model import create_model
from get_prediction import get_winner

API_TOKEN = '1961293599:AAHZ1GMuuPBWydF-fUcv6jbB_sIFn-w5o7Q'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
my_model = create_model()


@dp.message_handler()
async def send_welcome(message: types.Message):
    if 'https://www.hltv.org/matches/' in message.text:
        team_winner, coefA, coefB, teamA, teamB = await get_winner(my_model, message.text)
        if team_winner:
            await message.reply(f'Кэфы {teamA}:{coefA}, {teamB}:{coefB}')
            await message.answer(f'Я SurenNet (нейросеть) считаю, что выиграет команда - {team_winner}')
        else:
            await message.reply('Ставок пока нет')

executor.start_polling(dp)
