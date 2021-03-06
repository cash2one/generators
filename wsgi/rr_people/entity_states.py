# coding=utf-8
import logging

import redis

from rr_lib.cm import ConfigManager
from wsgi.properties import redis_max_connections
from wsgi.rr_people import S_STOP

HASH_STATES_PG = "pg_states_hashset"

STATE_CF = lambda x: "cf_state_%s" % x
STATE_PG = lambda x: "pg_state_%s" % x

HUMAN_STATES = "hs_hashset"
HUMAN_STATE = lambda x: "h_state_%s" % x

log = logging.getLogger("states")


class StatesHandler(object):
    def __init__(self, name="?", clear=False, max_connections=redis_max_connections):
        cm = ConfigManager()
        self.redis = redis.StrictRedis(host=cm.get('states_redis_address'),
                                       port=int(cm.get('states_redis_port')),
                                       password=cm.get('states_redis_password'),
                                       db=0,
                                       max_connections=max_connections
                                       )

        if clear:
            self.redis.flushdb()

        log.info("States handler inited for [%s]" % name)

    def set_posts_generator_state(self, sbrdt, state, ex=None):
        pipe = self.redis.pipeline()
        pipe.hset(HASH_STATES_PG, sbrdt, state)
        pipe.set(STATE_PG(sbrdt), state, ex=ex or 3600)
        pipe.execute()

    def get_posts_generator_state(self, sbrdt):
        return self.redis.get(STATE_PG(sbrdt))

    def remove_post_generator(self, sbrdt):
        pipe = self.redis.pipeline()
        pipe.hdel(HASH_STATES_PG, sbrdt)
        pipe.delete(STATE_PG(sbrdt))
        pipe.execute()

    def get_posts_generator_states(self):
        result = self.redis.hgetall(HASH_STATES_PG)
        for k, v in result.iteritems():
            ks = self.get_posts_generator_state(k)
            if v is None or ks is None:
                result[k] = S_STOP
        return result
