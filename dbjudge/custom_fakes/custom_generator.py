# MIT License

# Copyright (c) 2020 Raúl Medina González <raulmgcontact@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Tools to generate data of custom data types"""
from xeger import Xeger

from dbjudge.structures.column import Column
from dbjudge.structures.fake_types import FakeType
from dbjudge.connection_manager.manager import Manager
from dbjudge.utils.metaclasses import Singleton
from dbjudge.exceptions import InvalidColumnFakeType


class CustomCache(metaclass=Singleton):  # pylint: disable=too-few-public-methods
    """Cache object to reduce the amount of times
    preloaded data needs to be gathered.
    """

    def __init__(self, input_type):
        self.cached_type = input_type
        self.cached_data = None
        self._update_data()

    def _update_data(self):
        manager = Manager.singleton_instance
        self.cached_data = manager.get_custom_fakes(self.cached_type)

    def check_cache(self, fake_type):
        """Check cache status and updates it if needed.

        :param fake_type: The type you want to generate data of.
        :type fake_type: string
        """
        if fake_type != self.cached_type:
            self.cached_type = fake_type
            self._update_data()
        if not self.cached_data:
            self._update_data()


def gen_string(column: Column):
    """Generate data of string based custom types.

    :param column: The column you are generating data for.
    :type column: Column
    :raises InvalidColumnFakeType: If the column custom is neither regex nor custom.
    :return: Random value of the specified custom type.
    :rtype: string
    """
    if column.fake_type.category == FakeType.regex:
        regex_data = column.fake_type
        result = _gen_regex(regex_data.expression, column.max_char_len)

    elif column.fake_type.category == FakeType.custom:
        custom_data = column.fake_type
        result = _gen_custom_fake(custom_data.custom_type)
    else:
        raise InvalidColumnFakeType()
    return result


def _gen_regex(regex, max_len):
    generator = Xeger(limit=max_len)
    random_string = generator.xeger(regex)

    return random_string


def _gen_custom_fake(fake_type):
    cache = CustomCache(fake_type)
    cache.check_cache(fake_type)
    data = cache.cached_data

    return data.pop()[0]
