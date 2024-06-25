import logging
from .log_mode import get_log_mode, set_log_mode

class LogConfig:
    _instance = None
    MODES = {
        "all": 1,
        "debug_BRUH": 10,
        "debug_wtf": 20,
        "debug_deep": 30,
        "debug": 40,
        "test": 90,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogConfig, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        for name, level in self.MODES.items():
            logging.addLevelName(level, name.upper())
        self.logger = logging.getLogger('custom_logger')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.set_debug_mode(get_log_mode())

    def debug_custom(self, message, mode = get_log_mode(), *args, **kwargs):
        # print("current mode:", get_log_mode(), "mode:", mode)
        if self.logger.isEnabledFor(self.MODES[mode]):
            self.logger._log(self.MODES[mode], message, args, **kwargs)

    def set_debug_mode(self, mode):
        current_mode = get_log_mode()
        # print(f"Setting debug mode from {current_mode} -> to {mode}")
        if mode not in self.MODES: raise ValueError(f"Invalid mode: {mode}")
        set_log_mode(mode)
        self.logger.setLevel(self.MODES[mode])

    def get_debug_mode(self):
        return get_log_mode()

log_config = LogConfig()
