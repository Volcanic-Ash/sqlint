import os
from typing import Optional
from configparser import (
    ConfigParser,
    NoSectionError,
    NoOptionError
)

# section name in ini file
SECTION = 'sqlint'

# type of each config values
NAME_TYPES = {
  'comma-position': str,  # Comma position in breaking a line
  'keyword-style': str,  # Reserved keyword style
  'indent-steps': int  # indent steps in breaking a line
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INI = os.path.join(BASE_DIR, 'default.ini')


class ConfigLoader(object):
    def __init__(self, config_file: Optional[str] = DEFAULT_INI):
        self.values = {}

        # load default configs
        default_config = ConfigParser()
        default_config.read(DEFAULT_INI)
        self._load(default_config)

        # load user config
        self.user_config_file: Optional[str]
        if config_file is not None and config_file != DEFAULT_INI:
            self.user_config_file = config_file
            user_config = ConfigParser()
            user_config.read(config_file)

            # load user configs
            self._load(user_config)

    @staticmethod
    def _get_with_type(config_parser: ConfigParser, name: str, _type: type):
        """

        Args:
            config_parser:
            name:
            _type:

        Returns:

        """
        if _type == int:
            return config_parser.getint(SECTION, name)
        elif _type == float:
            return config_parser.getfloat(SECTION, name)
        elif _type == bool:
            return config_parser.getboolean(SECTION, name)

        # type is str or others
        return config_parser.get(SECTION, name)

    def _load(self, config_parser: ConfigParser):
        """Loads config values

        Returns:

        """
        # load default settings
        for name, _type in NAME_TYPES.items():
            try:
                self.values[name] = self._get_with_type(config_parser, name, _type)
            except NoSectionError as e:
                raise e
            except NoOptionError as e:
                # raise Error
                raise e
            except ValueError as e:
                # TODO: raise config Error
                raise e

    def get(self, name, default=None):
        """

        Args:
            name:
            default:

        Returns:

        """
        if name in self.values:
            return self.values[name]

        return default