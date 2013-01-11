#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import logging.config
import os
import sys

from twitter_bot import (Config, NicoSearch, YoutubeSearch, TwitterBotBase,
                         TwitterBot, JobManager)

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


class MeltyBloodBot(TwitterBotBase):
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret, search_keyword):
        # Init TwitterBotBase.
        TwitterBotBase.__init__(self, consumer_key, consumer_secret,
                                access_token, access_token_secret)
        self.search_keyword = search_keyword

        # Read config.
        config = Config(BOT_CONFIG)
        self.nico_user_id = config.get_value('user_id', section='niconico')
        self.nico_pass_word = config.get_value('pass_word', section='niconico')
        self.youtube_developer_key = config.get_value('developer_key',
                                                      section='youtube')

    def nico_video_post(self, prev_datetime):
        nico = NicoSearch(self.nico_user_id, self.nico_pass_word)
        nico.login()
        tweet_msgs = nico.tweet_msgs_for_latest_videos(self.search_keyword,
                                                       prev_datetime)
        self.tweet_msgs(tweet_msgs)

    def nico_comment_post(self, prev_datetime):
        nico = NicoSearch(self.nico_user_id, self.nico_pass_word)
        nico.login()
        tweet_msgs = nico.tweet_msgs_for_latest_comments(self.search_keyword,
                                                         prev_datetime)
        self.tweet_msgs(tweet_msgs)

    def youtube_video_post(self, prev_datetime):
        youtube = YoutubeSearch(self.youtube_developer_key)
        tweet_msgs = youtube.tweet_msgs_for_latest_videos(self.search_keyword,
                                                          prev_datetime)
        self.tweet_msgs(tweet_msgs)


## Main
def main(argv):
    """main function"""
    # Read config.
    config = Config(BOT_CONFIG, section='melty_blood_bot')
    screen_name = config.get_value('screen_name')
    consumer_key = config.get_value('consumer_key')
    consumer_secret = config.get_value('consumer_secret')
    access_token = config.get_value('access_token')
    access_token_secret = config.get_value('access_token_secret')

    logger.debug('Read config file: ' + 'screen_name=' + screen_name)

    with TwitterBot(screen_name, consumer_key, consumer_secret, access_token,
                    access_token_secret) as tw_bot:
        is_test = False
        if len(argv) >= 1:
            if argv[0] == 'test':
                is_test = True
                tw_bot.test = is_test
            elif argv[0] == 'init':
                # Initialize database.
                tw_bot.create_database()
                return
            elif argv[0] == 'follow':
                tw_bot.make_follow_list_from_followers()
                return
            else:
                raise Exception('Unknow argument: argv={}'.format(argv))

        with JobManager(tw_bot.db_name) as job_manager:
            #register_twitter_bot_jobs(job_manager, tw_bot)

            mb_bot = MeltyBloodBot(consumer_key, consumer_secret, access_token,
                                   access_token_secret, SEARCH_WORD)
            mb_bot.test = is_test
            register_melty_blood_bot_jobs(job_manager, mb_bot)

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


def register_melty_blood_bot_jobs(job_manager, bot):
    # Make func_and_intervals.
    func_and_intervals = []

    prev_datetime = job_manager \
        .get_job_called_datetime(MeltyBloodBot.__name__,
                                 MeltyBloodBot.nico_comment_post.__name__)
    func_tuple = (MeltyBloodBot.nico_comment_post, [prev_datetime],
                  None, 1.1 * 60)
    func_and_intervals.append(func_tuple)

    prev_datetime = job_manager \
        .get_job_called_datetime(MeltyBloodBot.__name__,
                                 MeltyBloodBot.youtube_video_post.__name__)
    func_tuple = (MeltyBloodBot.youtube_video_post, [prev_datetime],
                  None, 1.3 * 60)
    func_and_intervals.append(func_tuple)

    prev_datetime = job_manager \
        .get_job_called_datetime(MeltyBloodBot.__name__,
                                 MeltyBloodBot.nico_video_post.__name__)
    func_tuple = (MeltyBloodBot.nico_video_post, [prev_datetime],
                  None, 1.5 * 60)
    func_and_intervals.append(func_tuple)

    # Register.
    job_manager.register_jobs(bot, func_and_intervals)


if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]) or '.')
        logging.config.fileConfig(LOG_CONFIG)

        logger.info('Start melty_blood_bot.py cwd={}'.format(os.getcwd()))

        main(sys.argv[1:])

        logger.info('End melty_blood_bot.py')
        logger.info('-' * 80)
    except:
        logger.exception('Unhandled exception')
        raise
