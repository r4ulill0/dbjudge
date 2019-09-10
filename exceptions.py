class DbjudgeError(Exception):
    '''Base class for exceptions related to dbjudge module '''
    pass


class ColumnReferenceNotFound(Exception):
    pass


class TableNotInContext(Exception):
    pass


class FillerError(DbjudgeError):
    '''Error while filling the database with fake data'''
    pass


class DuplicatedDatabaseError(FillerError):
    pass


class MissingDatabaseError(FillerError):
    pass
