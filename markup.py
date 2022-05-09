from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def buy_menu(is_url=True, url='', bill=''):
  qiwi_menu = InlineKeyboardMarkup(row_width=1)
  if is_url:
    btn_qiwi_url = InlineKeyboardButton(text='Payment url', url=url)
    qiwi_menu.insert(btn_qiwi_url)

  btn_check_url = InlineKeyboardButton(text='Check payment status', callback_data='check_'+bill)
  qiwi_menu.insert(btn_check_url)
  return qiwi_menu