import os
import sys
import traceback
import redis
from enum import Enum, auto
import logging.handlers
import datetime
import time
import json

APP_ROLE = os.getenv("APP_ROLE", "writer")
MAX_TIME = os.getenv("MAX_TIME", 0)
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "nodes")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "log")
LOG_FILENAME = os.getenv("LOG_FILENAME", "%s.log" % APP_ROLE)


class AppRole(Enum):
    reader = auto()
    writer = auto()
    unknown = auto()


class Communicator:
    log = logging.getLogger()

    def __init__(self, config_filename, log_level=None, redis_channel="nodes", max_seconds=0):
        self.log_level = log_level
        self.log_file = config_filename
        self.redis_channel = redis_channel
        self.max_seconds = int(max_seconds)

        self.setup_logging()
        self.log.info("Role: %s" % APP_ROLE)
        self.log.info("Max working time: %s" % MAX_TIME)

        self.log.info("Connecting to Redis: %s:%s" % (REDIS_HOST, REDIS_PORT))
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    @staticmethod
    def get_log_level(log_level):
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        if log_level is None:
            log_level = 'INFO'

        return log_levels.get(log_level.strip().upper(), logging.INFO)

    def setup_logging(self):
        self.log_level = self.get_log_level(self.log_level)
        self.log.setLevel(self.log_level)

        logging_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        log_handler_stream = logging.StreamHandler()
        log_handler_stream.setFormatter(logging_formatter)
        log_handler_stream.setLevel(self.log_level)

        log_handler_file = logging.handlers.TimedRotatingFileHandler(self.log_file, when='midnight')
        log_handler_file.setFormatter(logging_formatter)
        log_handler_file.setLevel(self.log_level)

        self.log.addHandler(log_handler_stream)
        self.log.addHandler(log_handler_file)

        sys.excepthook = self.exception_handler

    def exception_handler(self, *exception_data):
        self.log.critical('Unhandled exception:\n%s', ''.join(traceback.format_exception(*exception_data)))
        exit(1)

    def writer_communicate(self):
        writer_start_time = time.time()
        hostname = os.uname()[1]

        initial_val = "Up"
        self.log.info("Set key/value: %s/%s" % (hostname, initial_val))
        self.redis.set(hostname, initial_val)

        while True:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            node = {hostname: dt}
            publish_data = json.dumps(node)

            self.log.info("Publish message to '%s' channel: %s" % (self.redis_channel, publish_data))
            self.redis.publish(self.redis_channel, publish_data)

            if self.max_seconds and time.time() - writer_start_time > self.max_seconds:
                self.log.info("Writer completed after '%s' seconds" % self.max_seconds)
                break
            else:
                time.sleep(1)

        final_val = "Down"
        self.log.info("Set key/value: %s/%s" % (hostname, final_val))
        self.redis.set(hostname, final_val)
        self.log.info("Delete key: %s" % hostname)
        self.redis.delete(hostname)

    def reader_communicate(self):
        self.redis.execute_command("config set notify-keyspace-events KEA")
        redis_pubsub = self.redis.pubsub()
        redis_pubsub.psubscribe("*")
        reader_start_time = time.time()

        while True:
            message = redis_pubsub.get_message()

            if message:
                self.log.info("Got message: %s" % message)
            else:
                time.sleep(1)

            if self.max_seconds and time.time() - reader_start_time > int(self.max_seconds):
                self.log.info("Reader completed after '%s' seconds" % self.max_seconds)
                break

    def communicate(self, role=AppRole.writer):
        if role == AppRole.writer:
            self.writer_communicate()
        if role == AppRole.reader:
            self.reader_communicate()


if APP_ROLE == "writer":
    app_role = AppRole.writer
elif APP_ROLE == "reader":
    app_role = AppRole.reader
else:
    app_role = AppRole.unknown

if app_role == AppRole.unknown:
    print("Error. Unknown role: %s" % APP_ROLE)
    exit(1)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

c = Communicator(os.path.join(LOG_DIR, LOG_FILENAME), LOG_LEVEL, REDIS_CHANNEL, MAX_TIME)
c.communicate(app_role)

c.log.info("Finish")
