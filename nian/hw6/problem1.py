"""
>>> p = Person(birthday='1985-05-25')
>>> p.age
34
>>> p.age = 33  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
AttributeError:
>>> p.birthday = '2015-08-15'
>>> p.age
4
>>> p = Person('Aug 15, 2015') # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
ValueError:
>>> p.birthday = 'Aug 15, 2015' # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
ValueError:
"""
import datetime
from datetime import date
import math

class Person:

    def __init__(self,birthday):
        self.birthday = birthday
    #should raise a ValueError if birthday is not in the correct format.

    
    @property
    def birthday(self):
        result = self.__birthday
        return result


    @birthday.setter
    def birthday(self,birthday):
    	## the strptime already raise the correct error
    	## and Ron said that we do not raise it explicitly
        self.__birthday = datetime.datetime.strptime(birthday,'%Y-%m-%d').date()


    @property
    def age(self):
    # returns the person’s age (based on the current date) as an int. 
        today = datetime.date.today()
        age = abs(self.birthday - today).days
        age = math.floor(age/365)
        return age



p = Person(birthday='1985-05-25')
print(p.age)