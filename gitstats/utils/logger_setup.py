import logging
import sys

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

def success(self, message: str, *args, **kargs) -> None:
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, stacklevel=2, **kargs)

logging.Logger.success = success

class CustomFormatter(logging.Formatter):
    COLORS = {
        "CRITICAL": "\x1b[31;1m",     # bold red
        "ERROR": "\x1b[31;20m",       # red
        "SUCCESS": "\x1b[32;20m",     # green
        "WARNING": "\x1b[33;20m",     # yellow
        "INFO": "\x1b[34;20m",        # blue
        "DEBUG": "\x1b[38;20m",       # grey
    }
    RESET = "\x1b[0m"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def __init__(self, use_color=True):
        super().__init__(self.LOG_FORMAT)
        self.use_color = use_color and sys.stdout.isatty()
        self.level_formatters = {}
        for level, color in self.COLORS.items():
            fmt = f"{color}{self.LOG_FORMAT}{self.RESET}" if self.use_color else self.LOG_FORMAT
            self.level_formatters[level] = logging.Formatter(fmt)

        # fallback formatter for unknown levels
        self.default_formatter = logging.Formatter(self.LOG_FORMAT)

    def format(self, record):
        formatter = self.level_formatters.get(record.levelname, self.default_formatter)
        return formatter.format(record)


def setup_logging(level=logging.DEBUG):
    """Global logging setup: all loggers will use CustomFormatter automatically."""
    root = logging.getLogger()
    root.setLevel(level)

    # Remove default handlers (optional, in case Python already added one)
    while root.handlers:
        root.removeHandler(root.handlers[0])

    # Add console handler with custom formatter
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(CustomFormatter())
    root.addHandler(ch)
