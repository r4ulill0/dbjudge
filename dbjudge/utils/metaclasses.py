"""Metaclasses for inheritance in other parts of the app"""


class Singleton(type):
    """Singleton object. Only one instance can exists at the same time."""
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "singleton_instance"):
            cls.singleton_instance = super().__call__(*args, **kwargs)
        return cls.singleton_instance
