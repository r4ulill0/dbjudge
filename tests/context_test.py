import pytest

from dbjudge.structures.context import Context
from dbjudge.structures.reference import Reference
from dbjudge.exceptions import TableNotInContext
from dbjudge.exceptions import ColumnReferenceNotFound


def test_get_table_not_in_context():
    with pytest.raises(TableNotInContext):
        context = Context()
        context.get_table_by_name('table')


def test_resolve_reference_not_in_context():
    with pytest.raises(ColumnReferenceNotFound):
        context = Context()
        context.resolve_column_reference((('table', 'column')))
