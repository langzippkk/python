"""
>>> cps = CPS('schools.csv')
>>> cps.schools[:5]
[GLOBAL CITIZENSHIP, ACE TECH HS, LOCKE A, ASPIRA - EARLY COLLEGE HS, ASPIRA - HAUGAN]
>>> [s for s in cps.schools if s.name.startswith('OR')]
[ORTIZ DE DOMINGUEZ, ORIOLE PARK, OROZCO, ORR HS]
>>> ace_tech = cps.schools[1]
>>> print('{:0.3f} {:0.3f}'.format(*ace_tech.location.as_degrees()))
41.796 -87.626
>>> print(ace_tech.full_address())
5410 S STATE ST
Chicago, IL 60609
>>> the_bean = Coordinate.fromdegrees(41.8821512, -87.6246838)
>>> cps.nearby_schools(the_bean, radius=0.5)
[NOBLE - MUCHIN HS, YCCS - INNOVATIONS]
>>> cps.get_schools_by_grade('PK', '12')
[FARRAGUT HS]
>>> cps.get_schools_by_network('Contract')
[CHIARTS HS, HOPE INSTITUTE, PLATO, CHICAGO TECH HS]
"""

import webbrowser
import math
import csv

class School:

    # !!! Don't change the __repr__ method.  It gives a simple string
    # representation of a School.  It's needed in the doctests and will help you
    # as you're developing and debugging the code.
    def __repr__(self):
        return self.name

    def __init__(self, id, name, network, address, zip, phone, grade, location):
        self.id = id
        self.name = name
        self.network = network
        self.address = address
        self.zip = zip
        self.phone = phone
        self.grades = grade
        self.location = location

    def open_website(self):
        return webbrowser.open_new_tab(f'http://schoolinfo.cps.edu/schoolprofile/SchoolDetails.aspx?SchoolId={self.id}')

    def distance(self, coord):
        latitude1 = (math.sin((self.location.latitude - coord.latitude)/2))**2
        longitude1 = (math.sin((self.location.longitude - coord.longitude)/2))**2
        longitude1 = math.cos(self.location.latitude) * math.cos(coord.latitude)*longitude1
        result = 2*3961*math.asin(math.sqrt(latitude1+longitude1))
        return result

    def full_address(self):
        return f'{self.address}\nChicago, IL {self.zip}'


class Coordinate:
    def __init__(self, latitude, longitude):

        self.latitude = float(latitude)*math.pi/180
        self.longitude = float(longitude)*math.pi/180
    
    ## A class method is a method that is bound to a class rather than its object.
    @classmethod
    def fromdegrees(cls, latitude, longitude):
        return Coordinate(latitude, longitude)

    def as_degrees(self):
        latitude2 = self.latitude*180/math.pi
        longtitude2 = self.longitude*180/math.pi
        return (latitude2,longtitude2)

    def distance(self, coord):
        latitude1 = (math.sin((self.location.latitude - coord.latitude)/2.0))**2
        longitude1 = (math.sin((self.location.longitude - coord.longitude)/2.0))**2
        longitude1 = math.cos(self.latitude) * math.cos(coord.latitude)*longitude1
        result = 2*3961*math.asin(math.sqrt(latitude1+longitude1))
        return result

    def show_map(self):
        latdegree = self.latitude*180/math.pi
        longtidegree = self.longitude*180/math.pi
        return webbrowser.open_new_tab(f'http://maps.google.com/maps?q={latdegree},{longtidegree}')


class CPS:
    def __init__(self, filename):
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            self.schools = []
            for row in reader:
                stripped_dict = {k.strip() : v.strip() for k, v in row.items()}
                self.schools.append(School(stripped_dict['School_ID'],stripped_dict['Short_Name'],stripped_dict['Network'],stripped_dict['Address'],
                stripped_dict['Zip'], stripped_dict['Phone'],stripped_dict['Grades'].split(", "),Coordinate(stripped_dict['Lat'],stripped_dict['Long'])))
         

    def nearby_schools(self, coord, radius=1.0):
        res = []
        for school in self.schools:
            if school.distance(coord) < radius:
                res.append(school)
        return res
        

    def get_schools_by_grade(self, *grades):
        res = []
        for school in self.schools:
            flag = True
            for grade in grades:
                if grade in school.grades:
                    continue
                else:
                    flag = False
            if flag == True:
                res.append(school)
        return res

    def get_schools_by_network(self, network):
        res = []
        for school in self.schools:
            if school.network == network:
                res.append(school)
        return res
