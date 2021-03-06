
import telegram
import random
import logging
import re
from time import sleep
from telegram.error import *

import gif
logger = logging.getLogger(__name__)


counter = {}
msg_limit = {}
my_chat_id = 113426151


def query_limit(update, context):
    user = update.message.from_user.id
    chat = update.message.chat_id
    if update.message.chat_id not in msg_limit:
        random_limit(update)
    logger.info(f'Limit query on {update.message.chat.title}'
                f' by {update.message.from_user.first_name}.'
                f' Limit: {msg_limit[update.message.chat_id]}')
    update.message.reply_text(f"Current limit: {get_limit(update.message.chat_id)}\n"
                              f"Your count: {get_count(chat, user)}")
    logger.info('================================================')


def random_limit(update):
    global msg_limit
    msg_limit[update.message.chat_id] = random.randint(8, 12)
    # context.bot.send_message(chat_id=my_chat_id,
    #                  text=f'New random limit set on {update.message.chat.title}: {msg_limit[update.message.chat_id]}')
    logger.info(f'Random limit of {msg_limit[update.message.chat_id]} set on {update.message.chat.title}')
    logger.info('================================================')
    return msg_limit[update.message.chat_id]


def set_limit(update):
    logger.debug(update.message.text)
    global msg_limit
    msg = update.message.text
    if not re.match(r'^/set_limit [0-9]+$', msg):
        update.message.reply_text("Nah... I didn't get that. Use a number only, stupid!")
    else:
        msg_limit[update.message.chat_id] = int(re.findall('[0-9]+', msg)[0])
        logger.info(f'New Limit set by {update.message.from_user.first_name}'
                    f' on {update.message.chat.title}: {msg_limit[update.message.chat_id]}')
        logger.info('================================================')
        # context.bot.send_message(chat_id=my_chat_id,
        #                  text=f'Manual limit set on {update.message.chat.title}'
        #                       f' by {update.message.from_user.first_name}: {msg_limit[update.message.chat_id]}')


# MONOLOGNATE STUFF
def delete_messages(context, user, chat):
    # Delete messages from group
    for m in set(counter[chat][user]['msg_ids']):
        context.bot.delete_message(chat_id=chat, message_id=m)


def add_count(chat, user, update):
    global counter
    user_counter = counter[chat][user]
    user_counter['count'] += 1
    user_counter['msg_ids'].append(update.message.message_id)
    user_counter['msgs'].append(update.message.text)


def initialize_count(chat, user, update):
    global counter
    logger.info(f'Initializing counter on {chat}, {user}')
    # if chat not in counter:
    counter[chat] = {}
    counter[chat][user] = {}
    user_counter = counter[chat][user]
    user_counter['count'] = 1
    user_counter['msg_ids'] = [update.message.message_id]
    user_counter['msgs'] = [update.message.text]
    counter[chat]['latest_by'] = user


def reset_count(chat, user, update):
    global counter
    # previous_user = counter[chat]['latest_by']
    logger.info(f"Resetting the counter on {update.message.chat.title}")
    # counter[chat].pop(previous_user)
    # initialize_count(chat, user, update)
    counter[chat] = {}


def get_count(chat, user):
    return counter[chat][user]['count']


def get_limit(chat):
    return msg_limit[chat]


def hit_limit(chat, user, update):
    if chat not in msg_limit:
        random_limit(update)
        return False
    chat_limit = get_limit(chat)

    if get_count(chat, user) == chat_limit:
        # Reset counter. limit and return True
        random_limit(update)
        return True
    return False


def monolognate(chat, user, update, context):
    logger.info(f'Monologue by {update.message.from_user.first_name}')
    monologue = '\n'.join(counter[chat][user]['msgs'])
    delete_messages(context, user, chat)
    gif.send_random_tenor(update, context, 'tsunami')

    try:
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except BadRequest as e:
        logger.info(f'BadRequest: {e}')
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except RetryAfter as e:
        logger.info(f'RetryAfter: {e.retry_after}')
        sleep(int(e.retry_after))
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except TimedOut as e:
        logger.info(f'TimedOut: {e}')
        sleep(1)
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except Unauthorized as e:
        logger.info(f'Unauthorized: {e}')
        sleep(0.25)
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except NetworkError as e:
        logger.info(f'NetworkError: {e}')
        sleep(1)
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
    except Exception as e:
        logger.info(f'Some Shit happened: {e}')
        sleep(1)
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='*Monologue by {}*:\n\n`{}`'.format(
                             update.message.from_user.first_name,
                             monologue),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         timeout=15)
        # Send monologue back as a single message
    finally:
        reset_count(chat, user, update)


def handle_counter(update, context):
    user = update.message.from_user.id
    chat = update.message.chat_id
    message = update.message
    logger.info(f'Msg on {update.message.chat.title}({chat})'
                f' from {update.message.from_user.first_name}({user}): {update.message.text}')

    # If it's a new user or the count was reset earlier
    if chat not in counter or user not in counter[chat] and not message.reply_to_message:
        initialize_count(chat, user, update)
    else:
        # if we seen the user before, check if previous msg was by the same user
        # if it was, increase counter and add msgs
        if user == counter[chat].get('latest_by') and not message.reply_to_message:
            add_count(chat, user, update)
            logger.info(f'Count for {update.message.from_user.first_name}'
                        f' on {update.message.chat.title}: {get_count(chat, user)}')
            # Check if user hit  chat limit. If it did, monolognate it
            if hit_limit(chat, user, update):
                monolognate(chat, user, update, context)
                reset_count(chat, user, update)
        else:
            reset_count(chat, user, update)

