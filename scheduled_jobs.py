from telegram import Bot
from data_model import Kratjes, db_session
from datetime import datetime
from config import Config
import asyncio


async def get_expired_bets(bot: Bot):
    while True:
        session = db_session()
        kratjes = session.query(Kratjes).order_by(Kratjes.created_date).all()
        message_text = 'De volgende kratjes zijn verschuldigd! \n\n'
        for bet in kratjes:
            if bet.due_date and bet.due_date < datetime.now():
                message_text += f'{bet.better} stelt: '
                bet.due_date = bet.due_date.strftime('%d-%m-%Y') if bet.due_date else 'het einde van dit leven'
                message_text += '"{1}" voor "{2}" met "{0}" als onderpand\n\n'.format(
                        bet.stake, bet.bet_description, bet.due_date)
        bot.send_message(chat_id=Config.HHPC_CHAT_ID, text=message_text)

        # wait for 1 hours
        await asyncio.sleep(60*60*24)
