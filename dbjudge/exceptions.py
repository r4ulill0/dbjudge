class DbjudgeError(Exception):
    '''Base class for exceptions related to dbjudge module '''
    pass


class ColumnReferenceNotFound(DbjudgeError):
    pass


class TableNotInContext(DbjudgeError):
    pass


class FillerError(DbjudgeError):
    '''Exception raised while filling the database with fake data'''
    pass


class DuplicatedDatabaseError(FillerError):
    pass


class MissingDatabaseError(FillerError):
    pass


class InvalidColumnTypeError(DbjudgeError):
    pass


class InvalidColumnFakeType(DbjudgeError):
    pass


class JudgeError(DbjudgeError):
    '''Exception raised while keeping track of user answers'''
    pass


class SessionNotFound(JudgeError):
    pass
