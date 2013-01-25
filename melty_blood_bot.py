#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import logging.config
import os
import sys

from twitter_bot import TwitterBot, TwitterVideoBot, JobManager
import define


# Set default encording.
try:
    if sys.version_info[0] >= 3:
        from imp import reload
    reload(sys)
    sys.setdefaultencoding('utf-8')
except ImportError:
    pass

SEARCH_WORD = 'mbaacc'

# Config.
LOG_CONFIG = 'config/log.cfg'
BOT_CONFIG = 'config/bot.cfg'

# Initialize logger.
logger = logging.getLogger('app')


## Main
def main(argv):
    """main function"""
    with TwitterBot(BOT_CONFIG) as tw_bot:
        is_test = False
        if len(argv) >= 1:
            if argv[0] == 'test':
                is_test = True
                tw_bot.is_test = is_test
            elif argv[0] == 'init':
                # Initialize database.
                tw_bot.create_database()
                return
            elif argv[0] == 'follow':
                tw_bot.make_follow_list_from_followers()
                return
            else:
                raise Exception('Unknow argument: argv={}'.format(argv))

        with JobManager() as job_manager:
            #register_twitter_bot_jobs(job_manager, tw_bot)

            video_bot = TwitterVideoBot(BOT_CONFIG)
            video_bot.is_test = is_test
            register_twitter_video_bot_jobs(job_manager, video_bot)

            # Run jobs.
            job_manager.run()


def register_twitter_bot_jobs(job_manager, bot):
    # Make func_and_intervals.
    func_and_intervals = []

    func_tuple = (TwitterBot.update_database, None, None, 12 * 60)
    func_and_intervals.append(func_tuple)

    func_tuple = (TwitterBot.retweet_mentions, None, None, 11)
    func_and_intervals.append(func_tuple)

    func_tuple = (TwitterBot.retweet_retweeted_of_me, None, None, 23)
    func_and_intervals.append(func_tuple)

    func_tuple = (TwitterBot.follow_not_following_users, None, None, 7 * 60)
    func_and_intervals.append(func_tuple)

    # Register.
    job_manager.register_jobs(bot, func_and_intervals)


def register_twitter_video_bot_jobs(job_manager, bot):
    # Make func_and_intervals.
    func_and_intervals = []

    prev_datetime = job_manager \
        .get_job_called_datetime(TwitterVideoBot.__name__,
                                 TwitterVideoBot.nico_comment_post.__name__)
    func_tuple = (TwitterVideoBot.nico_comment_post,
                  [SEARCH_WORD, prev_datetime, filter_func_for_nico_comment_post],
                  None, 1.1 * 30)
    func_and_intervals.append(func_tuple)

    prev_datetime = job_manager \
        .get_job_called_datetime(TwitterVideoBot.__name__,
                                 TwitterVideoBot.youtube_video_post.__name__)
    func_tuple = (TwitterVideoBot.youtube_video_post, [SEARCH_WORD, prev_datetime],
                  None, 1.3 * 30)
    func_and_intervals.append(func_tuple)

    prev_datetime = job_manager \
        .get_job_called_datetime(TwitterVideoBot.__name__,
                                 TwitterVideoBot.nico_video_post.__name__)
    func_tuple = (TwitterVideoBot.nico_video_post, [SEARCH_WORD, prev_datetime],
                  None, 1.5 * 30)
    func_and_intervals.append(func_tuple)

    # Register.
    job_manager.register_jobs(bot, func_and_intervals)


def filter_func_for_nico_comment_post(video):
    if video.id in define.NG_ID:
        return True
    return False

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]) or '.')
        logging.config.fileConfig(LOG_CONFIG)

        logger.info('Start melty_blood_bot.py argv={}, cwd={}'
                    .format(sys.argv[1:], os.getcwd()))

        main(sys.argv[1:])
    except:
        logger.exception('Unhandled exception')
        raise
    finally:
        logger.info('End melty_blood_bot.py')
        logger.info('-' * 80)
