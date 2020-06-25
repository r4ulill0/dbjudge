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
'''Exceptions raised by dbjudge'''


class DbjudgeError(Exception):
    '''Base class for exceptions related to dbjudge module '''


class NoDatabaseSelected(Exception):
    '''Exception raised if trying to use a manager method without having one database selected'''


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
