from structures.column import Column
from structures.fake_types import Fake_type
from structures.fake_types import Regex
from connection_manager.manager import Manager
from utils.metaclasses import Singleton
from xeger import Xeger


class Custom_cache(metaclass=Singleton):
    def __init__(self, input_type):
        self.cached_type = input_type
        self.cached_data = None
        self._update_data()

    def _update_data(self):
        manager = Manager.singleton_instance
        self.cached_data = manager.get_custom_fakes(self.cached_type)

    def check_cache(self, fake_type):
        if(fake_type != self.cached_type):
            self.cached_type = fake_type
            self._update_data()
        if(len(self.cached_data) == 0):
            self._update_data()


def gen_string(column: Column):

    if(column.fake_type.category == Fake_type.regex):
        regex_data = column.fake_type
        result = _gen_regex(regex_data.expression, column.max_char_len)

    elif(column.fake_type.category == Fake_type.custom):
        custom_data = column.fake_type
        result = _gen_custom_fake(custom_data.custom_type)

    return result


def _gen_regex(regex, max_len):
    generator = Xeger(limit=max_len)
    random_string = generator.xeger(regex)

    return random_string


def _gen_custom_fake(fake_type):
    cache = Custom_cache(fake_type)
    cache.check_cache(fake_type)
    data = cache.cached_data

    return data.pop()
