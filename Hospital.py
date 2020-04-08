from Patient import *
import uuid
import re
import datetime

class Quarantines:
    def __init__(self, name, capacity, l = None):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []
        self.location = l
        self.staff = []


    def showQuarantines(self):
            return \
                {
                    'Name of Quarantine Area ' : self.name,
                    'Capacity of Quarantine Area' : self.capacity,
                    'Quarantine located in Hospital' : self.location,
                    'Quarantine ID' : self.ID
                }

    def addPatient(self, patient):
        self.patients.append(patient)

    def occupancy(self):
        return 100 * len(self.patients) / self.capacity

    def returnQ(self):
        return \
            {
            'name': self.name,
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
            'patients': [p.showPatients() for p in self.patients]
            }

class Staff:
    def __init__(self, name, dob, type, location = None):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.type = type
        self.location = location

    def showStaff(self):
        return \
            {
                'name' : self.name,
                'ID' : self.ID,
                'Date of birth' : self.dob,
                'Type' : self.type,
                'Location' : self.location
            }

    def getMember(self):
        return \
            {
                self.ID : self
            }

class System:
    def __init__(self):
        self.patients = []
        self.staff = []

    def addPatient(self, name, dob):
        if name == None or dob == None:
            return None
        str = re.findall(r'([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)', name.title())
        if str == []:
            return print('1')

        date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', dob)
        if date_of_birth == []:
            return print('2')
        elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
            return print('3')
        elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
            return print('4')
        elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
            return print('5')
        dob = datetime.date(int(date_of_birth[0][0]), int(date_of_birth[0][1]), int(date_of_birth[0][2]))
        print(dob)
        p = Patient(name.title(), dob)
        self.patients.append(p)

    def addStaff(self, name, dob, type, location):

        date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', dob)
        if date_of_birth == []:
            return print('2')
        elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
            return print('3')
        elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
            return print('4')
        elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
            return print('5')
        dob = datetime.date(int(date_of_birth[0][0]), int(date_of_birth[0][1]), int(date_of_birth[0][2]))

        S = Staff(name, dob, type, location)
        self.staff.append(S)

    def getPatientID(self):
        for p in self.patients:
            return[p.ID]

    def getStaff(self):
        for s in self.staff:
            return[s.getStaff]

    def getSelf(self):
        for p in self.patients:
            return p.getID

class Hospital:

    def __init__(self, name, capacity):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []  # List of patients admitted to the hospital
        self.staff = []  # List of doctors and nurses working in the hospital
        self.quarantines = [] # List of quarantine areas in the hospital
        self.staff = [] # List of all staff members


    # return the percentage of occupancy of this hospital
    def occupancy(self):
        return 100 * len(self.patients) / self.capacity

    # admit a patient to the hospital of given name and date of birth
    def admission(self, name, dob, l):
        if self.capacity - len(self.patients) <= 0:
            return None
        if name == None or dob == None:
            return None
        str = re.findall(r'([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)', name.title())
        if str == []:
            return print('1')
        date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', dob)
        if date_of_birth == []:
            return print('2')
        elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
            return print('3')
        elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
            return print('4')
        elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
            return print('5')
        dob = datetime.date(int(date_of_birth[0][0]), int(date_of_birth[0][1]), int(date_of_birth[0][2]))
        print(dob)
        p = Patient(name.title(), dob, l)
        self.patients.append(p)

    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'capacity': self.capacity,
            'occupancy': self.occupancy()
        }

    def addQuarantine(self, name, capacity, l):
        if int(capacity) <= 0:
            return None
        elif int(capacity) > 5000:
            return None
        q = Quarantines(name, capacity, l)
        self.quarantines.append(q)

    def getID(self):
        li = [p.getID() for p in self.patients]
        return (li)

