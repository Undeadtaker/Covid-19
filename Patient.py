import uuid

class Patient:
    def __init__(self, name, dob, l = None):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.location = l
        self.infected = False
        self.tested = False
        self.dead = False
        self.dispatched = False


    def showPatients(self):
        return \
            {
               'ID' : self.ID,
               'date of birth' : self.dob,
               'name' : self.name,
               'location' : self.location,
               'is infected' :  self.infected,
               'is dead' : self.dead
            }

    def getID(self):
        return {self.ID : self}



