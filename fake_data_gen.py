import random
import string

from structures import Table, Column, Context
import type_compatible

class Faker:
    def __init__(self, table):
        self.column_data_pool = {}
        for column in table.columns:
            self.column_data_pool[column.name] = self._generate_data_pool(column, table.fake_data_size)
    
    def _generate_data_pool(self, column, size):
        pool = set()
        if (column.fake_type == 'default'):
            # while (len(pool)!= size):
            for _ in range(size):
                pool.add(self._generate_default_fake(column.ctype))
        return pool

    
    def _generate_default_fake(self, ctype):
        if (type_compatible.is_string(ctype)):
            fake = self._gen_string()
            formatted_fake = self._format_string_fake(fake)
            return formatted_fake
            
    
    def _gen_string(self):
        STRING_LEN = 10
        result = ""
        for _ in range(STRING_LEN):
            result += random.choice(string.ascii_letters)
        return result
    
    
    def _format_string_fake(self, fake):
        envelope_particle = "\'"
        formatted_result = envelope_particle + fake + envelope_particle
        return formatted_result  
    
    def generate_fake(self, column):    
        return random.sample(self.column_data_pool[column.name],1)[0]