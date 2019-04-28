import pytest
import filler
from structures import Table, Column
from fake_data_gen import Faker

def test_generate_formatted_fake_values():
    table = Table("person","name")
    col= Column("name", "character varying")
    table.add_column(col)
    faker = Faker(table)

    output = filler.generate_formatted_fake_values(table.columns, faker)

    assert isinstance(output, str)

def test_format_columns_names():
    col_color = Column("color", "character")
    col_license = Column("license", "character varying")
    col_date = Column("time", "date")
    columns = [col_color, col_license, col_date]
    
    output = filler.format_columns_names(columns)
    expected = "color, license, time"
    assert output == expected
