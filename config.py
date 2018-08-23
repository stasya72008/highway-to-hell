import configparser
from os import path

import logging
from logging.config import fileConfig


class Config(object):
    def __init__(self, section):
        self._parser = configparser.RawConfigParser()
        self._config_file = path.join(path.dirname(__file__), 'config.ini')
        self._section = ''
        try:
            self._parser.read(self._config_file)
        except configparser.Error, exc:
            raise configparser.Error(
                "Error reading config file {conf_file}: {error}".format(
                    conf_file=self._config_file, error=str(exc)))

        if not self._parser.has_section(section):
            # print 'Available sections:'
            # print self._parser.sections()
            raise configparser.NoSectionError
        else:
            self._section = section

    def get_property(self, property_name):
        """
            Get property value from config.default.ini file

            Arguments:
                :param property_name: property name

            Return:
                :return: (str): property value
        """
        return self._parser.get(self._section, property_name)


class GlobalConfig(Config):
    def __init__(self):
        super(GlobalConfig, self).__init__('global')


class RestConfig(Config):
    def __init__(self):
        super(RestConfig, self).__init__('rest')

    @property
    def host(self):
        return self.get_property('host')

    @property
    def port(self):
        return self.get_property('port')

    @property
    def debug(self):
        return self.get_property('debug')


class RestEndpointConfig(Config):
    def __init__(self):
        super(RestEndpointConfig, self).__init__('rest_endpoint')

    @property
    def host(self):
        return self.get_property('host')

    @property
    def port(self):
        return self.get_property('port')


class CalendarConfig(Config):
    def __init__(self):
        super(CalendarConfig, self).__init__('calendar')

    @property
    def host(self):
        return self.get_property('host')

    @property
    def port(self):
        return self.get_property('port')

    @property
    def debug(self):
        return self.get_property('debug')


class DBConfig(Config):
    def __init__(self):
        super(DBConfig, self).__init__('database')

    @property
    def host(self):
        return self.get_property('host')

    @property
    def port(self):
        return self.get_property('port')

    @property
    def user(self):
        return self.get_property('user')

    @property
    def password(self):
        return self.get_property('pass')


class LogConfig:
    def __init__(self):
        logging.config.fileConfig(
            path.join(path.dirname(__file__), 'log_config.ini'),
            defaults={'logfilename': path.join(path.dirname(__file__),
                                               'hop-hey-lala-ley.log')})
