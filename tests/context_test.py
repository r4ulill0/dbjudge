import pytest

from structures.context import Context
from structures.reference import Reference
from exceptions import TableNotInContext
from exceptions import ColumnReferenceNotFound


def test_get_table_not_in_context():
    with pytest.raises(TableNotInContext):
        context = Context()
        context.get_table_by_name('table')


def test_resolve_reference_not_in_context():
    with pytest.raises(ColumnReferenceNotFound):
        context = Context()
        context.resolve_column_reference((('table', 'column')))
