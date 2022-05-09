import asyncio
from enum import auto
import logging

from markup import buy_menu

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from dotenv import dotenv_values

from pyqiwip2p import QiwiP2P

config = dotenv_values(".env")

amount = 5 # cost of item
lifetime = 10 # mins bill will be living 
comment = 'hi' # comment in bill

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

#alt url for pay url
p2p = QiwiP2P(auth_key=config['secret_key'], alt=config['ALT_DOMAIN'])#, alt='example.com'
loop = asyncio.get_event_loop()
bot = Bot(config['BOT_TOKEN'], parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)

# Setup payments
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment)

    #alt_url redirect to pay url
    await bot.send_message(message.from_user.id, f'payment_url: {bill.alt_url}', 
                            parse_mode='html',
                            reply_markup=buy_menu(url=bill.alt_url, bill=bill.bill_id))

# handler payment status
@dp.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    if str(p2p.check(bill_id=bill).status) == 'PAID':
        await bot.send_message(callback.from_user.id, 'payment successfully')
    else:
        await bot.send_message(callback.from_user.id, 'payment failed', reply_markup=buy_menu(False, bill=bill))

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
