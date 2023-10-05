from telegram import  Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime


# Create a dictionary to store attendance data
attendance_dict = {}
admins =[155438187,818466324]

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    # Check if the user is the admin
    if user_id in admins:
        if chat_id in attendance_dict:
            if attendance_dict[chat_id]["active"] == True:
                await update.message.reply_text("Attendance has already been started!")
            else:
                attendance_dict[chat_id]["active"] = True
                await update.message.reply_text("Attendance has started!")
        else:
            attendance_dict[chat_id] = {
                "admin_id": user_id,
                "attendance": [],
                "excused":[],
                "longterm":[],
                "active": True,  # Flag to indicate if attendance tracking is active
            }
            await update.message.reply_text("Group has been registered and started attendance")
    else:
        await update.message.reply_text("Welcome to the Attendance Bot! Use /done to mark your attendance.")

async def reset(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Check if the user is the admin
    if user_id in admins:
        if chat_id in attendance_dict:
            attendance_dict[chat_id]["active"] = False # Attendance tracking is inactive
            attendance_dict[chat_id]["attendance"]=[] # Reset the attendance list
            attendance_dict[chat_id]["excused"] = [] # Reset the excused list
            await update.message.reply_text("Attendance tracking has been reset")
        else:
            await update.message.reply_text("This group has not been registered. Enter /start to register!")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

async def done(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    chat_id = update.message.chat_id
    # Check if attendance tracking is active in this group
    if chat_id in attendance_dict:
        if attendance_dict[chat_id]["active"] == True:
            if user_name not in attendance_dict[chat_id]["attendance"]:
                # attendance_dict[chat_id]["attendance"].append({"user_id": user_id, "user_name": user_name})
                attendance_dict[chat_id]["attendance"].append(user_name)
                await update.message.reply_text(f"Attendance marked for @{user_name}.")
            else:
                await update.message.reply_text("Your attendance has already been marked")
        else:
            await update.message.reply_text("Attendance has not been started yet!")

    else:
        await update.message.reply_text("This group is not registered with our bot.")


async def list(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    print(chat_id)

    # Check if the user is the admin
    if user_id in admins:
        if chat_id in attendance_dict:
            usernames = [users for users in attendance_dict[chat_id]["attendance"]]
            excused = [users for users in attendance_dict[chat_id]["excused"]]
            others = [users for users in attendance_dict[chat_id]["longterm"]]
            done_list = "\n@".join(usernames)
            excused_list = "\n@".join(excused)
            others_list = "\n@".join(others)
            print(others_list)
            await update.message.reply_text(f"SENT:\n@{done_list} \n\n EXCUSED:\n \n@{excused_list} \n\n LONG EXCUSE:\n \n@{others_list} ")
        else:
            await update.message.reply_text("This group has not been registered with our bot")
    else:
        await update.message.reply_text("You are not authorized to use this command.")


async def excuse(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    chat_id = update.message.chat_id

    # Check if attendance tracking is active in this group
    if chat_id in attendance_dict:
        if attendance_dict[chat_id]["active"] == True:
            excuse_text = context.args  # Get the excuse text provided by the user
            if excuse_text:
                    excuse_text = " ".join(excuse_text)
                    if user_name not in attendance_dict[chat_id]["excused"]:
                        attendance_dict[chat_id]["excused"].append(user_name)
                        await update.message.reply_text(f"Excuse recorded for {user_name}: {excuse_text}")
                    else:
                        await update.message.reply_text("Your excuse for this week has already been noted")
            else:
                await update.message.reply_text("Please provide an excuse after the /excuse command.")
        else:
            await update.message.reply_text("Attendance has not been started yet!")

    else:
        await update.message.reply_text("This group has not been registered with our group")

async def longexcuse(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    chat_id = update.message.chat_id

    # Check if attendance tracking is active in this group
    if chat_id in attendance_dict:
        excuse_text = context.args  # Get the excuse text provided by the user
        if excuse_text:
            excuse_text = " ".join(excuse_text)
            if user_name not in attendance_dict[chat_id]["longterm"]:
                attendance_dict[chat_id]["longterm"].append(user_name)
                await update.message.reply_text(f"Excused for long term, admins please take note {user_name}: {excuse_text}")
            else:
                await update.message.reply_text("Your long excuse has already been noted")
        else:
            await update.message.reply_text("Please provide why you are excused after the command. Thanks!")
    else:
        await update.message.reply_text("This group has not been registered with our group")

def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    # Your Telegram Bot API Token
    token = "5845800147:AAHmANu_9EveZMNmiviemc4AxNI33DENgGY"

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done",done))
    application.add_handler(CommandHandler("list",list))
    application.add_handler(CommandHandler("excuse",excuse))
    application.add_handler(CommandHandler("others",longexcuse))
    application.add_handler(CommandHandler("reset",reset))



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
