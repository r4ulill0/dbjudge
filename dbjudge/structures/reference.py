"""Database column reference representation"""


class Reference:  # pylint: disable=too-few-public-methods
    """Database column reference representation"""

    def __init__(self, source, target):
        self.source = source
        self.target = target
