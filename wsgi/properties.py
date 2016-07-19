# coding=utf-8
import logging
import os
import sys

__author__ = 'alesha'


# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()

def module_path():
    if hasattr(sys, "frozen"):
        return os.path.dirname(
            sys.executable
        )
    return os.path.dirname(__file__)


cacert_file = os.path.join(module_path(), 'cacert.pem')

logger = logging.getLogger()

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s[%(levelname)s]%(name)s|%(processName)s(%(process)d): %(message)s')
formatter_process = logging.Formatter('%(asctime)s[%(levelname)s]%(name)s|%(processName)s: %(message)s')
formatter_human = logging.Formatter('%(asctime)s[%(levelname)s]%(name)s|%(processName)s: %(message)s')

sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

mongo_uri = "mongodb://3030:sederfes100500@ds055525.mongolab.com:55525/reddit_people"
db_name = "reddit_people"

states_redis_address = "pub-redis-17140.us-east-1.1.azure.garantiadata.com"
states_redis_port = 17140
states_redis_password = "sederfes100500"

posts_redis_address = "pub-redis-17040.us-east-1-4.3.ec2.garantiadata.com"
posts_redis_port = 17040
posts_redis_password = "sederfes100500"

process_director_redis_address = "pub-redis-17359.us-east-1-3.4.ec2.garantiadata.com"
process_director_redis_port = 17359
process_director_redis_password = "sederfes100500"

redis_max_connections = 2

SEC = 1
MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7
WEEK_DAYS = {0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA", 6: "SU"}

TIME_TO_WAIT_NEW_COPIES = 3600 * 24
TIME_TO_RELOAD_SUB_POSTS = 3600 * 2  # at live random in consumer

DEFAULT_LIMIT = 500
# DEFAULT_LIMIT = 20

min_copy_count = 3
min_comment_create_time_difference = 3600 * 24 * 10

shift_copy_comments_part = 5  # общее количество комментариев / это число  = сколько будет пропускаться
min_donor_comment_ups = 5
max_donor_comment_ups = 100000
min_donor_num_comments = 50

max_consuming = 80
min_consuming = 60

min_voting = 65
max_voting = 85

step_time_after_trying = 60
tryings_count = 10

time_step_less_iteration_power = 0.85

want_coefficient_max = 100

# imgur properties
ImgrClientID = 'd7e9f9350ebe5a8'
ImgrClientSecret = '945c124e48fd9ca208788c70028d7e8d8c7dc7c1'

# youtube props
YOUTUBE_DEVELOPER_KEY = "AIzaSyCYF4GPkVpdYjZ5RpDaSMcbpRpfkavnUzc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

force_post_manager_sleep_iteration_time = 3600  # время через которое он будет сканировать ютуб

test_mode = os.environ.get("RR_TEST", "false").strip().lower() in ("true", "1", "yes")
print "TEST? ", test_mode

logger.info(
    "Reddit People MANAGEMENT SYSTEM STARTED... \nEnv:%s" % "\n".join(
        ["%s:\t%s" % (k, v) for k, v in os.environ.iteritems()]))

WORKED_PIDS_QUERY = "python"