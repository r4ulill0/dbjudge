import pytest
import filler
from structures import Context, Table, Column
from fake_data_gen import Faker
import datetime
def test_generate_fake_values():
    table = Table("person","name")
    col= Column("name", "character varying")
    table.add_column(col)
    context = Context()
    context.add_table(table)
    faker = Faker(table,context)

    output = filler.generate_fake_values(table.columns, faker)

    for value in output:
        assert isinstance(value, str), "non string value: {0} detected".format(value)

def test_format_fake_values():
    date = "'4286-03-08 13:39:16'"
    test_values = ['str',25,date,False]
    output = filler.format_fake_values(test_values)
    expected = "str,25,\'4286-03-08 13:39:16\',False"
    assert output == expected


def test_format_columns_names():
    col_color = Column("color", "character")
    col_license = Column("license", "character varying")
    col_date = Column("time", "date")
    columns = {'color':col_color, 'license':col_license, 'time':col_date}
    
    output = filler.format_columns_names(columns)
    assert 'color' in output
    assert 'license' in output
    assert 'time' in output
    assert ', ' in output
    

def test_fill_table():
    #TODO pensar en como probar este procedimiento
    pass