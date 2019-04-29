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
            fake = self._gen_float()
            formatted_fake = str(fake)
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

    def _format_string_fake(self, fake):
        envelope_particle = "\'"
        formatted_result = envelope_particle + fake + envelope_particle
        return formatted_result  
    
    def generate_fake(self, column):    
        return random.sample(self.column_data_pool[column.name],1)[0]