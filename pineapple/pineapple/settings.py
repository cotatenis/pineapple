BOT_NAME = 'pineapple'
VERSION = "0-1-1"

SPIDER_MODULES = ['pineapple.spiders']
NEWSPIDER_MODULE = 'pineapple.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SPIDERMON_CUSTOM_MIN_ITEMS = {
    'pineapple-adidas' : 250,
    'pineapple-nike' : 850,
}

MAGIC_FIELDS = {
    "timestamp": "$isotime",
    "spider": "$spider:name",
    "url": "$response:url",
}
SPIDER_MIDDLEWARES = {
    "scrapy_magicfields.MagicFieldsMiddleware": 100,
}
SPIDERMON_ENABLED = True
EXTENSIONS = {
    'pineapple.extensions.SentryLogging' : -1,
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}
ITEM_PIPELINES = {
    "pineapple.pipelines.DiscordMessenger" : 100,
    "pineapple.pipelines.GCSPipeline": 300,
}
SPIDERMON_SPIDER_CLOSE_MONITORS = (
'pineapple.monitors.SpiderCloseMonitorSuite',
)

SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = False
SPIDERMON_PERIODIC_MONITORS = {
'pineapple.monitors.PeriodicMonitorSuite': 30, # time in seconds
}
SPIDERMON_SENTRY_DSN = ""
SPIDERMON_SENTRY_PROJECT_NAME = ""
SPIDERMON_SENTRY_ENVIRONMENT_TYPE = ""

#THROTTLE
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 5

#GCP
GCS_PROJECT_ID = ""
GCP_CREDENTIALS = ""
GCP_STORAGE = ""
GCP_STORAGE_CRAWLER_STATS = ""
#FOR IMAGE UPLOAD
IMAGES_STORE = f''

#DISCORD
DISCORD_WEBHOOK_URL = ""
DISCORD_THUMBNAIL_URL = ""
SPIDERMON_DISCORD_WEBHOOK_URL = ""

#LOG LEVEL
LOG_LEVEL='INFO'