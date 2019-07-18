from customFakes.types import CustomFakeType
from xeger import Xeger


def gen_strin(custom_type, max_len):
    # NOT IMPLEMENTED YET
    pass


def gen_regex(regex, max_len):
    generator = Xeger(limit=max_len)
    random_string = generator.xeger(regex)
