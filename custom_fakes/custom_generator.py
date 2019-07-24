from structures.column import Column
from structures.fake_types import Fake_type
from structures.fake_types import Regex
from xeger import Xeger


def gen_string(column: Column):

    if(column.fake_type.category == Fake_type.regex):
        regex_data = column.fake_type
        result = _gen_regex(regex_data.expression, column.max_char_len)

    return result


def _gen_regex(regex, max_len):
    generator = Xeger(limit=max_len)
    random_string = generator.xeger(regex)

    return random_string
