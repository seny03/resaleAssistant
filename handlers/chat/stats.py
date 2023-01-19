from loader import bot, dp, types, db, logger
from filters import isAdmin, isUser, haveDbAccess


@dp.message_handler(haveDbAccess(), commands=["stats"])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    stats = db.get_stats()
    stats_message = f"<b>Quantity: {stats['quantity']}</b>\n" \
                    f"<b>\nPrice: </b>" \
                    f"\n\t[+] Max price: {stats['price']['max_price']}₽" \
                    f"\n\t[-] Min price: {stats['price']['min_price']}₽" \
                    f"\n\t[!] Mean price: {stats['price']['mean_price']}₽" \
                    f"\n\t[+] Good deals: {stats['price']['good_deals']}\n" \
                    f"<b>\nDescription: </b>" \
                    f"\n\t[+] Max length: {stats['desc']['max_length']}" \
                    f"\n\t[-] Min length: {stats['desc']['min_length']}" \
                    f"\n\t[!] Mean length: {int(stats['desc']['mean_length'])}"
    await bot.send_message(chat_id, stats_message, parse_mode='html')
    logger.debug(f"Statistics has been sent chat_id={chat_id}, username={message.chat.username}")
