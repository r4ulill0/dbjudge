import random
import string
import datetime
import decimal
from psycopg2.extensions import IntervalFromPy

from dbjudge.structures.fake_types import Fake_type
from dbjudge.custom_fakes import custom_generator
from dbjudge import exceptions
from dbjudge import type_compatible


class Faker:
    def __init__(self, table, context, pool_size=100):
        if table not in context.tables:
            raise exceptions.TableNotInContext(
                'Table {0} not in context'.format(table.name))

        self._context = context
        self.column_data_pool = {}
        for _, column in table.columns.items():
            self.column_data_pool[column.name] = set()
            self.column_data_pool[column.name] = self._generate_data_pool(
                column, pool_size)

    def _generate_data_pool(self, column, size):
        pool = set()

        if (len(column.reference) != 0 and column.reference[0] != None):
            pool = self._fetch_foreing_key_pool(column.reference[0])

        else:
            while not self._is_pool_big_enough(len(pool), size, column):
                # for _ in range(size):
                pool.add(self._generate_fake(column))

        if column.nullable:
            pool.pop()
            pool.add('NULL')

        return pool

    def _fetch_foreing_key_pool(self, reference):
        column = self._context.resolve_column_reference(reference)
        pool = column.instances_pool
        return pool

    def _is_pool_big_enough(self, actual_size, target_size, column):
        response = (actual_size >= target_size
                    or (type_compatible.is_boolean(column.ctype) and actual_size >= 2)
                    or (type_compatible.is_string(column.ctype)
                        and column.max_char_len is not None
                        and actual_size >= len(string.ascii_letters)*column.max_char_len)
                    )
        return response

    def _generate_fake(self, column):
        if type_compatible.is_string(column.ctype):
            if column.fake_type.category != Fake_type.default:
                fake = custom_generator.gen_string(column)
            else:
                fake = self._gen_string(column.max_char_len)
            return fake

        elif type_compatible.is_integer(column.ctype):
            bytes_limit = type_compatible.bytes_limit(column.ctype)
            fake = self._gen_integer(
                bytes_limit, column.min_value, column.max_value)
            formatted_fake = str(fake)
            return formatted_fake

        elif type_compatible.is_boolean(column.ctype):
            fake = self._gen_boolean()
            formatted_fake = str(fake)
            return formatted_fake

        elif type_compatible.is_float(column.ctype):
            fake = self._gen_decimal(
                column.max_char_len, column.min_value, column.max_value)
            formatted_fake = str(fake)
            return formatted_fake

        elif type_compatible.is_date(column.ctype):
            fake = self._gen_datetime(column.min_value, column.max_value)
            formatted_fake = self._wrap_with_quote_marks(fake)
            return formatted_fake

        elif type_compatible.is_interval(column.ctype):
            fake = self._gen_interval()
            formatted_fake = self._format_interval(fake)
            return formatted_fake
        else:
            raise exceptions.InvalidColumnTypeError()

    def _gen_string(self, max_len):
        max_string_len = max_len if max_len != None else 10
        result = ""
        string_len = random.randint(1, max_string_len)
        for _ in range(string_len):
            result += random.choice(string.ascii_letters)
        return result

    def _gen_integer(self, bytes_limit, bottom_limit, top_limit):
        max_num_generated_with_bytes = (2**(bytes_limit*8))/2
        bottom = -max_num_generated_with_bytes
        top = max_num_generated_with_bytes - 1
        min_end_point = bottom_limit if bottom_limit else bottom
        max_end_point = top_limit if top_limit else top
        result = random.randint(min_end_point, max_end_point)

        return result

    def _gen_boolean(self):
        result = bool(random.getrandbits(1))
        return result

    def _gen_decimal(self, decimal_positions, min_value, max_value):
        default_max = decimal.Decimal('9999999.9999999')
        default_min = decimal.Decimal('-9999999.9999999')
        max_value = max_value if max_value else default_max
        min_value = min_value if min_value else default_min
        max_tuple = max_value.as_tuple()
        min_tuple = min_value.as_tuple()

        max_exp = max_tuple[2]
        min_exp = min_tuple[2]
        bigger_exp = max_exp if abs(max_exp) > abs(min_exp) else min_exp
        conversion_divisor = decimal.Decimal(10**(bigger_exp*-1))
        minimum = (min_value * conversion_divisor).to_integral()
        maximum = (max_value * conversion_divisor).to_integral()

        big_int = random.randint(minimum, maximum)
        result = decimal.Decimal(big_int)/decimal.Decimal(conversion_divisor)
        if decimal_positions:
            round(result, decimal_positions)
        return result

    def _gen_datetime(self, min_date, max_date):
        min_date = min_date if min_date else datetime.datetime.min
        max_date = max_date if max_date else datetime.datetime.max
        max_ordinal = max_date.toordinal()
        min_ordinal = min_date.toordinal()
        ordinal_date = random.randint(min_ordinal, max_ordinal)

        in_range = False
        while not in_range:
            hour = random.randint(0, 23)
            minit = random.randint(0, 59)
            sec = random.randint(0, 59)

            date = datetime.datetime.fromordinal(ordinal_date)
            result = date.replace(hour=hour, minute=minit, second=sec)

            in_range = min_date <= date and date <= max_date

        return result

    def _gen_interval(self):
        seconds_in_day = 3600*24
        seconds = random.randint(0, seconds_in_day)
        days = random.randint(-999999999, 999999999)

        result = datetime.timedelta(days=days, seconds=seconds)

        return result

    def _wrap_with_quote_marks(self, fake):
        envelope_particle = "\'"
        formatted_result = envelope_particle + str(fake) + envelope_particle
        return formatted_result

    def _format_interval(self, fake):
        adapter = IntervalFromPy(fake)
        binary_string = adapter.getquoted()
        formatted_result = binary_string.decode("UTF-8")

        return formatted_result

    def generate_fake(self, table):

        values_dict = {}
        while not self._valid_primary_key(table, values_dict):
            values_dict = {}

            if len(table.foreign_keys) != 0:
                for foreign_key in table.foreign_keys:
                    row_instance = random.choice(
                        foreign_key.target_table.row_instances)

                    for reference in foreign_key.get_column_references():
                        values_dict[reference.source] = row_instance[reference.target]

            for _, column in table.columns.items():
                if column.name in values_dict.keys():
                    continue

                fake = random.sample(self.column_data_pool[column.name], 1)[0]
                if column.unique and not self._has_pool_uniques(table, column):
                    actual_size = len(self.column_data_pool[column.name])
                    self.column_data_pool[column.name] = self._generate_data_pool(
                        column, actual_size)

                if column.unique:
                    while self._exists_in_instance(fake, table, column):
                        fake = random.sample(
                            self.column_data_pool[column.name], 1)[0]
                values_dict[column.name] = fake

        values = self._list_values(values_dict, table)
        table.row_instances.append(values_dict)

        return values

    def _valid_primary_key(self, table, values: dict):
        pk_column_names = table.primary_key
        is_correct_pk = True
        is_value_filled = len(table.columns) == len(values.keys())

        if not is_value_filled:
            return is_value_filled

        for instance in table.row_instances:
            for c_name in pk_column_names:
                is_correct_pk = not values[c_name] == instance[c_name]

                if not is_correct_pk:
                    return is_correct_pk

        return is_correct_pk

    def _has_pool_uniques(self, table, column):
        faker_pool = self.column_data_pool[column.name]
        instances_pool = set()
        for instance in table.row_instances:
            instances_pool.add(instance[column.name])
        diff = faker_pool - instances_pool

        condition = len(table.row_instances) == 0 or len(diff) > 0
        return condition

    def _exists_in_instance(self, fake, table, column):
        exists = False

        for instance in table.row_instances:
            if instance[column.name] == fake:
                exists = True
                break

        return exists

    def _list_values(self, dictionary, table):
        ordered_list = []
        for column_name in table.columns.keys():
            ordered_list.append(dictionary[column_name])

        return ordered_list
