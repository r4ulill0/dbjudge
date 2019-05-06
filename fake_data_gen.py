import random
import string
import datetime
from psycopg2.extensions import IntervalFromPy
from structures import Table, Column, Context
import exceptions
import type_compatible

class Faker:
    def __init__(self, table, context):
        if table not in context.tables:
            raise exceptions.TableNotInContext('Table {0} not in context',table.name)
        
        self._context = context
        self.column_data_pool = {}
        for key, column in table.columns.items():
            self.column_data_pool[column.name] = self._generate_data_pool(column, table.fake_data_size)
    
    def _generate_data_pool(self, column, size):
        pool = set()
        
        if (len(column.reference)!= 0 and column.reference[0] != None):
            pool = self._fetch_foreing_key_pool(column.reference[0])
            
        elif (column.fake_type == 'default'):
            # while (len(pool)!= size):
            for _ in range(size):
                pool.add(self._generate_default_fake(column.ctype))
        return pool

    def _fetch_foreing_key_pool(self, reference):
        column = self._context.resolve_column_reference(reference)
        pool = column.instances_pool
        return pool

    def _generate_default_fake(self, ctype):
        if (type_compatible.is_string(ctype)):
            fake = self._gen_string()
            formatted_fake = self._wrap_with_quote_marks(fake)
            return formatted_fake
        
        elif (type_compatible.is_integer(ctype)):
            bytes_limit = type_compatible.bytes_limit(ctype)
            fake = self._gen_integer(bytes_limit)
            formatted_fake = str(fake)
            return formatted_fake

        elif (type_compatible.is_boolean(ctype)):
            fake = self._gen_boolean()
            formatted_fake = str(fake)
            return formatted_fake
        
        elif (type_compatible.is_float(ctype)):
            fake = self._gen_float()
            formatted_fake = str(fake)
            return formatted_fake

        elif(type_compatible.is_date(ctype)):
            fake = self._gen_datetime()
            formatted_fake = self._wrap_with_quote_marks(fake)
            return formatted_fake

        elif (type_compatible.is_interval(ctype)):
            fake = self._gen_interval()
            formatted_fake = self._format_interval(fake)
            return formatted_fake
    
    def _gen_string(self):
        STRING_LEN = 10
        result = ""
        for _ in range(STRING_LEN):
            result += random.choice(string.ascii_letters)
        return result
    
    def _gen_integer(self, bytes_limit):
        max_num_generated_with_bytes = (2**(bytes_limit*8))/2
        bottom = -max_num_generated_with_bytes
        top = max_num_generated_with_bytes -1
        result = random.randint(bottom, top)
        
        return result
    
    def _gen_boolean(self):
        result = bool(random.getrandbits(1))
        return result

    def _gen_float(self):
        result = random.getrandbits(32) + random.random()
        return result
    
    def _gen_datetime(self):
        max_ordinal = datetime.datetime.max.toordinal()
        ordinal_date = random.randint(1, max_ordinal)
        hour = random.randint(0,23)
        min = random.randint(0,59)
        sec = random.randint(0,59)

        date = datetime.datetime.fromordinal(ordinal_date)
        result = date.replace(hour=hour, minute=min,second=sec)

        return result
    
    def _gen_interval(self):
        seconds_in_day = 3600*24
        seconds = random.randint(0,seconds_in_day)
        days = random.randint(-999999999,999999999)

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

    def generate_fake(self, column):    
        return random.sample(self.column_data_pool[column.name],1)[0]