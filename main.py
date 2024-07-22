import os
import django
import asyncio
from django.db.models import F
from django.db import IntegrityError

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')  # 'config.settings' ni o'z loyihangiz nomi bilan almashtiring
django.setup()

from botapp.models import User, \
    RefFriendModel  # O'z modelingizni import qiling (botapp ni to'g'ri nom bilan almashtiring)

from telegram import Update, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, Application
import logging
import re
import aiohttp

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

CHANNEL_ID = '@testchannelbots2dw'  # O'z kanal nomingizni kiriting
BOT_TOKEN = '7384714328:AAHvieSEyVWe_JwUsg8wvXxwWQSiZBzHBkY'  # Bot tokeningiz


async def add_user(telegram_id, coins, limit=1000, energy=1000, tap=1):
    loop = asyncio.get_event_loop()
    user, created = await loop.run_in_executor(None, lambda: User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={'coins': coins, 'limit': limit, 'energy': energy, 'tap': tap}
    ))
    return created


async def inv_friend(telegram_id, ref_friend):
    loop = asyncio.get_event_loop()

    user = await loop.run_in_executor(None, lambda: RefFriendModel.objects.create(
        telegram_id=telegram_id,
        ref_friend=ref_friend,
    ))

    return user


async def update_user_coins(telegram_id, amount):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None,
                               lambda: User.objects.filter(telegram_id=telegram_id).update(coins=F('coins') + amount))


async def check_subscription(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}') as response:
            result = await response.json()

            return result.get('result', {}).get('status') in ['member', 'administrator', 'creator']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    args = context.args

    # Check if referral code is provided
    referred_user_id = None
    if args and args[0].startswith('r_'):
        referral_code = args[0]
        referred_user_id = re.search(r'r_(\d+)', referral_code).group(1)
        logger.info(f"User {user_id} was referred by {referred_user_id}")

    # Check subscription status
    is_subscribed = await check_subscription(user_id)

    if not is_subscribed:
        # If not subscribed, send the subscription message
        await update.message.reply_text(
            "Please subscribe to our channel to use this bot. Once you subscribe, you can use all features.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Subscribe", url=f"https://t.me/{CHANNEL_ID}")],
                ]
            )
        )
        return

    # If subscribed, proceed with the regular bot functionality
    referral_link = f"https://t.me/RPGCOINBOT?start=r_{user_id}"
    welcome_message = """
Hey! Welcome to R-P-G Bot!
Tap on the coin and see your balance rise.

R-P-G is a cutting-edge financial platform where users can earn tokens by leveraging the mining app's various features. The majority of R-P-G Token (TAPS) distribution will occur among the players here.

Do you have friends, relatives, or co-workers?
Bring them all into the game.
More buddies, more coins.

A huge reward awaits you at the end of the project for inviting your friends. It remains a mystery for now\n\n"""

    loop = asyncio.get_event_loop()
    if referred_user_id:
        user_exists = await loop.run_in_executor(None, lambda: User.objects.filter(telegram_id=user_id).exists())
        if not user_exists:
            created = await add_user(user_id, coins=5000)
            await inv_friend(referred_user_id, user_id)

            if created:
                welcome_message += f" You have been referred by your friend {referred_user_id}!"

                # Update coins for the referred user
                await update_user_coins(referred_user_id, 1000)
            else:
                welcome_message += f" User already exists {referred_user_id}!"
        else:
            welcome_message += f" User already exists {referred_user_id}!"
    else:
        user_exists = await loop.run_in_executor(None, lambda: User.objects.filter(telegram_id=user_id).exists())
        if not user_exists:
            await add_user(user_id, coins=0)

    # Send welcome message with referral link and web app button
    await update.message.reply_text(
        f"{welcome_message}Refer your friends using the following link: {referral_link}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="PLAY!",
                                web_app=WebAppInfo(url=f"https://611a-213-230-93-155.ngrok-free.app/{user_id}/"))],
            ] if is_subscribed else [],  # PLAY tugmasi faqat obuna bo'lgan foydalanuvchilarga ko'rsatiladi
            resize_keyboard=True
        ),
    )


def main() -> None:
    # Start the bot
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
