'''Exceptions raised by dbjudge'''


class DbjudgeError(Exception):
    '''Base class for exceptions related to dbjudge module '''


class ColumnReferenceNotFound(DbjudgeError):
    '''Exception raised while trying to resolve a column reference'''


class TableNotInContext(DbjudgeError):
    '''Exception raised while trying to resolve a specific table in'''


class FillerError(DbjudgeError):
    '''Exception raised while filling the database with fake data'''


class DuplicatedDatabaseError(FillerError):
    '''Exception raised while creating a database with a name already taken'''


class MissingDatabaseError(FillerError):
    '''Exception raised while accessing a database that does not exist, or is not part of dbjudge'''


class InvalidColumnTypeError(DbjudgeError):
    '''Exception raised when trying to generate data for an unsupported column type'''


class InvalidColumnFakeType(DbjudgeError):
    '''Exception raised when trying to generate data for an unsupported custom column type'''


class JudgeError(DbjudgeError):
    '''Exception raised while keeping track of user answers'''


class SessionNotFound(JudgeError):
    '''Exception raised while using the judge without a session'''
