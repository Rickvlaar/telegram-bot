from telegram import Bot
from data_model import Kratjes, db_session
from datetime import datetime
import asyncio


async def get_expired_bets(bot: Bot):
    while True:
        session = db_session()
        kratjes = session.query(Kratjes).order_by(Kratjes.created_date).all()
        message_text = ''
        for bet in kratjes:
            message_text += f'{bet.better} stelt: '
            bet.due_date = bet.due_date.strftime('%d-%m-%Y') if bet.due_date else 'het einde van dit leven'
            message_text += '"{1}" voor "{2}" met "{0}" als onderpand\n\n'.format(
                    bet.stake, bet.bet_description, bet.due_date)
        bot.send_message(chat_id='', text=message_text)
        # wait for 1 hours
        await asyncio.sleep(12000)
