STOPCHARS = "; |, |\*|\n|\t|\W+"

DEFAULT_FILES = [
    "shakespeare/kinglear.txt",
    "shakespeare/othello.txt",
    "shakespeare/romeoandjuliet.txt",
]

DEFAULT_BUCKET = "apache-beam-samples"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(asctime)s %(levelname)s:%(name)s]: %(message)s"},
        "detailed": {
            "format": "[%(asctime)s %(levelname)s:%(name)s.%(funcName)s:%(lineno)d]: %(message)s"  # noqa
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {"weasyprint": {"level": "ERROR"}},
}
