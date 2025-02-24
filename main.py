from lib.databasing import DataBase
from lib.whitelist import MinecraftWhitelist

import lib.helper as helper
import lib.hashing as hashing

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

WAITING_FOR_NEW_NICKNAME = 1
WAITING_FOR_CHANGE_NICKNAME = 2

keyboard = [
        [InlineKeyboardButton("Добавить ник", callback_data='add_nickname')],
        [InlineKeyboardButton("Изменить ник", callback_data='change_nickname')],
    ]

class Bot:
    def __init__(self):
        token = helper.get_token()

        self.public_key = hashing.load_key()
        self.database = DataBase()
        self.whitelist_manager = MinecraftWhitelist()


        self.application = Application.builder().token(token).build()


        self.start_handler = CommandHandler('start', self.start)
        self.start_handler = CommandHandler('delete', self.delete)
        self.conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.button_callback)],
            states={
                WAITING_FOR_NEW_NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_add_nickname)],
                WAITING_FOR_CHANGE_NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_change_nickname)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
    def run(self):
        self.application.add_handler(self.start_handler)
        self.application.add_handler(self.conv_handler)

        self.application.run_polling()

    def nexus(self, user_id: str):
        text = f"Текущий ник: {self.database.get_nickname(user_id)}\n"
        text += f"Дата добавления: {self.database.get_date(user_id)}\n\n"
        text += helper.oneline_text_from_file("nexus_massage")
        return text

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id

        if self.database.id_is_in(user_id):
            await context.bot.send_message(update.effective_chat.id, self.nexus(user_id), 
                                           reply_markup=InlineKeyboardMarkup([keyboard[1]]))
        else:
            await context.bot.send_message(update.effective_chat.id, helper.oneline_text_from_file("nexus_massage_first"),
                                           reply_markup=InlineKeyboardMarkup([keyboard[0]]))


    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        query = update.callback_query
        await query.answer()

        if query.data == "add_nickname":
            await context.bot.send_message(update.effective_chat.id, "Скинь ник")
            return WAITING_FOR_NEW_NICKNAME
    
        elif query.data == "change_nickname":
            await context.bot.send_message(update.effective_chat.id, "Скинь новый ник")
            return WAITING_FOR_CHANGE_NICKNAME 
    
    
    async def handle_add_nickname(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        nickname = update.message.text
        user_username = hashing.encrypt_data(self.public_key, update.effective_user.username)


        nick_check = helper.nick_is_not_valid(nickname)
        match nick_check:
            case 101:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... Почему такой короткий❔")
                return WAITING_FOR_CHANGE_NICKNAME
            case 102:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... ну и чего ты понапихал❔")
                return WAITING_FOR_CHANGE_NICKNAME
            case 103:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... сам то веришь что твой ник❔")
                return WAITING_FOR_CHANGE_NICKNAME
        

        self.database.insert_user((user_id, nickname, None, helper.get_date(), user_username))
        self.whitelist_manager.add_player(nickname)

        await context.bot.send_message(update.effective_chat.id, "Ну все братан, ты в пиве ✅")
        await context.bot.send_message(update.effective_chat.id, self.nexus(user_id),
                                               reply_markup=InlineKeyboardMarkup([keyboard[1]]))

        return ConversationHandler.END
    
    async def handle_change_nickname(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        nickname = update.message.text
        user_username = hashing.encrypt_data(self.public_key, update.effective_user.username)
        print(user_username)


        nick_check = helper.nick_is_not_valid(nickname)
        match nick_check:
            case 101:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... Почему такой короткий❔")
                return WAITING_FOR_CHANGE_NICKNAME
            case 102:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... ну и чего ты понапихал❔")
                return WAITING_FOR_CHANGE_NICKNAME
            case 103:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... сам то веришь что твой ник❔")
            case 104:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Братан... ну и че поменялось❔")
                return WAITING_FOR_CHANGE_NICKNAME

        self.whitelist_manager.update_player_name(nickname, self.database.get_nickname(user_id))
        self.database.modify_user(user_id, nickname, user_username)
        

        await context.bot.send_message(update.effective_chat.id, "Ну все братан Ты в пиве Снова ✅")
        await context.bot.send_message(update.effective_chat.id, self.nexus(user_id),
                                               reply_markup=InlineKeyboardMarkup([keyboard[1]]))

        return ConversationHandler.END


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id

        await context.bot.send_message(update.effective_chat.id, "Отмена братан")
        if self.database.id_is_in(user_id):
            await context.bot.send_message(update.effective_chat.id, helper.oneline_text_from_file("nexus_massage"), 
                                           reply_markup=InlineKeyboardMarkup([keyboard[1]]))
        else:
            await context.bot.send_message(update.effective_chat.id, helper.oneline_text_from_file("nexus_massage"),
                                           reply_markup=InlineKeyboardMarkup([keyboard[0]]))
        
        return ConversationHandler.END
            
    async def delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id

        self.whitelist_manager.remove_player(self.database.get_nickname(user_id))
        self.database.dlete_user(user_id)        

        await context.bot.send_message(update.effective_chat.id, "Ну и вали")
        if self.database.id_is_in(user_id):
            await context.bot.send_message(update.effective_chat.id, helper.oneline_text_from_file("nexus_massage"), 
                                           reply_markup=InlineKeyboardMarkup([keyboard[1]]))
        else:
            await context.bot.send_message(update.effective_chat.id, helper.oneline_text_from_file("nexus_massage"),
                                           reply_markup=InlineKeyboardMarkup([keyboard[0]]))


        return ConversationHandler.END

if __name__ == "__main__":
    bot = Bot()
    bot.run()