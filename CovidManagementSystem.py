from Hospital import *


class CovidManagementSystem:
    def __init__(self):
        self.hospitals = [] # list of hospitals known to the system
        self.System = System()

    def getHospitals(self):
        return self.hospitals

    def getAllStaff(self):
        SysLi = [s.showStaff() for s in self.System.staff]
        HospitalsList = [h for h in self.hospitals]
        HosStaffLi= []
        QuaranLi = []

        for h in HospitalsList:
            for s in h.staff:
                HosStaffLi.append(s.showStaff())

        for h in HospitalsList:
            for q in h.quarantines:
                for s in q.staff:
                    QuaranLi.append(s.showStaff())

        return \
            {
                'Staff in the System' : SysLi,
                'Staff in the Hospitals' : HosStaffLi,
                'Staff in Quarantines' : QuaranLi
            }

    def getStaffMembers(self):
        SysLi = [s.getMember() for s in self.System.staff]
        HospLi = [h for h in self.hospitals]
        HospStaff = []
        QuaranLi = []

        for h in HospLi:
            for s in h.staff:
                HospStaff.append(s.getMember())

        for h in HospLi:
            for q in h.quarantines:
                for s in q.staff:
                    QuaranLi.append(s.getMember())

        final = SysLi + HospStaff + QuaranLi
        return final

    def MoveStaff(self, staff, location):
        print(staff)
        print(location)
        print(staff.location)

        if staff.location == location and staff.location == None:
            return print('Cannot assign the staff to where they already are')
        elif staff.location == None and location == 'system':
            return print('Cannot assign the staff to where they already are')


        if location == 'system':
            hosp = self.getHospitalById(staff.location)
            quaran = self.getQuarantineById(staff.location)
            staff.location = None
            self.System.staff.append(staff)
            if hosp == None:
                pass
            else:
                hosp.staff.remove(staff)
                return None
            if quaran == None:
                pass
            else:
                quaran.staff.remove(staff)
                return None


        for h in self.getHospitals():
            if h.ID == location:
                staffHosp = self.getHospitalById(staff.location)
                if staffHosp == None:
                    pass
                else:
                    staffHosp.staff.remove(staff)
                hosp = self.getHospitalById(location)
                if staff.location == None:
                    staff.location = location
                    hosp.staff.append(staff)
                    self.System.staff.remove(staff)
                    return None
                else:
                    pass
                if self.getHospitalById(staff.location) == None:
                    pass
                else:
                    old_location = self.getHospitalById(staff.location)
                    hosp.staff.append(staff)
                    staff.location = location

                    if old_location.staff == []:
                        pass
                    else:
                        old_location.staff.remove(staff)
                    return None
                if self.getQuarantineById(staff.location) == None:
                    pass
                else:
                    hosp.staff.append(staff)
                    self.getQuarantineById(staff.location).staff.remove(staff)
                    staff.location = location
                    return None
                return None
            else:
                pass

        for h in self.getHospitals():
            for q in h.quarantines:
                if q.ID == location:
                    staffQuaran = self.getQuarantineById(staff.location)
                    if staffQuaran == None:
                        pass
                    else:
                        staffQuaran.staff.remove(staff)
                quaran = self.getQuarantineById(location)

                if staff.location == None:
                    staff.location = location
                    quaran.staff.append(staff)
                    self.System.staff.remove(staff)
                    return None
                else:
                    pass
                if self.getHospitalById(staff.location) == None:
                    pass
                else:
                    self.getHospitalById(staff.location).staff.remove(staff)
                    staff.location = location
                    quaran.staff.append(staff)
                    return None
                if self.getQuarantineById(staff.location) == None:
                    pass
                else:
                    old_location = self.getQuarantineById(staff.location)
                    quaran.staff.append(staff)
                    staff.location = location
                    if old_location.staff == []:
                        pass
                    else:
                        old_location.staff.remove(staff)
                    return None
                return None
            else:
                pass

    def DelStaff(self, staff):

        if self.getQuarantineById(staff.location) == None:
            pass
        else:
            self.getQuarantineById(staff.location).staff.remove(staff)
            return None
        if self.getHospitalById(staff.location) == None:
            pass
        else:
            self.getHospitalById(staff.location).staff.remove(staff)
            return None
        if staff.location == None:
            self.System.staff.remove(staff)
            return None

    def addHospital(self, name, capacity):
        if int(capacity) < 0:
            return None
        elif int(capacity) > 5000:
            return None

        h = Hospital(name, capacity)
        self.hospitals.append(h)

    def addToSystem(self, name, dob):
        p = self.System
        p.addPatient(name, dob)

    def getHospitalById(self, id_):
        for h in self.hospitals:
            if (h.ID == id_):
                return h
        return None

    def getQuarantineById(self, id_):
        for h in self.hospitals:
            for q in h.quarantines:
                if (q.ID == id_):
                    return q
        return None

    def deleteQ(self, id_):
        for h in self.hospitals:
            for q in h.quarantines:
                if (q.ID == id_):
                    h.quarantines.remove(q)

    def deleteHospital(self, id_):
        h = self.getHospitalById(id_)
        if (h != None):
            self.hospitals.remove(h)
        return h != None

    def addStaff(self, name, dob, type, location):
        if type != 'doctor' and type != 'nurse':
            print('kek')
            return ('Staff type not doctor or nurse')
        s = self.System
        s.addStaff(name, dob, type, location)

    def ShowAllQ(self):
        Qlist = []
        for h in self.hospitals:
            for q in h.quarantines:
                Qlist.append(q)
        if Qlist == []:
            return 'No Quarantines found'
        else:
            return Qlist

    def MovePatient(self, Pat_ID, Facility_ID):
        li_System = [p.getID() for p in self.System.patients]  # returns a dict with key as Patient ID, and value Patient object
        li_Hospital = []
        li_Quaran = []
        for h in self.getHospitals():
            for p in h.patients:
                li_Hospital.append(p.getID())

        for h in self.getHospitals():
            for q in h.quarantines:
                for p in q.patients:
                    li_Quaran.append(p.getID())

        final_li = li_System + li_Hospital + li_Quaran

# For system

        if Facility_ID == 'system':
            for d in final_li:
                for key, value in d.items():
                    if str(key) == str(Pat_ID):
                        patientObject = value

                        if patientObject.dead == True or patientObject.dispatched == True:
                            return 'Cannot move dead or dispatched patients'

                        if patientObject.location == None:
                            return ['Patient alredy in this location']

                        if self.getHospitalById(patientObject.location) == None:
                            pass
                        else:
                            old_location = patientObject.location
                            self.System.patients.append(patientObject)
                            patientObject.location = None
                            self.getHospitalById(old_location).patients.remove(patientObject)
                            return print('Patient moved from hospital to system')

                        if self.getQuarantineById(patientObject.location) == None:
                            pass
                        else:
                            old_location = patientObject.location
                            self.System.patients.append(patientObject)
                            patientObject.location = None
                            self.getQuarantineById(old_location).patients.remove(patientObject)
                            return print('Patient moved from quarantine to system')
        else:
            pass

# For hospitals

        if self.getHospitalById(Facility_ID) == None:
            pass
        else:
            for d in final_li:
                for key, value in d.items():
                    if str(key) == str(Pat_ID):
                        patientObject = value

                        if patientObject.dead == True or patientObject.dispatched == True:
                            return print('Cannot move dead or dispatched patients')

                        if patientObject.location == None:
                            patientObject.location = Facility_ID
                            self.getHospitalById(Facility_ID).patients.append(patientObject)
                            self.System.patients.remove(patientObject)
                            return print('Moved the patient from the system to the hospital')

                        if self.getQuarantineById(Facility_ID) == None:
                            pass
                        else:
                            old_location = patientObject.location
                            patientObject.location = Facility_ID
                            if self.getQuarantineById(Facility_ID) == None:
                                pass
                            else:
                                self.getQuarantineById(Facility_ID).patients.append(patientObject)
                                self.getQuarantineById(old_location).patients.remove(patientObject)
                                return print('Moved the patient from a quarantine to a hospital')

                        if self.getHospitalById(patientObject.location) == Facility_ID:
                           return print('Patient is already in this hospital')
                        else:
                            old_location = patientObject.location
                            patientObject.location = Facility_ID
                            if self.getHospitalById(Facility_ID) == None:
                                pass
                            else:
                                self.getHospitalById(Facility_ID).patients.append(patientObject)
                                self.getQuarantineById(old_location).patients.remove(patientObject)
                                return print('Moved the patient from one hospital to another')

# For quarantines

        if self.getQuarantineById(Facility_ID) == None:
            pass
        else:
            for d in final_li:
                for key, value in d.items():
                    if str(key) == str(Pat_ID):
                        patientObject = value

                        if patientObject.dead == True or patientObject.dispatched == True:
                            return print('Cannot move dead or dispatched patients')

                        if patientObject.location == None:
                            patientObject.location = Facility_ID
                            self.getQuarantineById(Facility_ID).patients.append(patientObject)
                            self.System.patients.remove(patientObject)
                            return print('Moved the patient from the system to a quarantine')

                        if self.getHospitalById(patientObject.location) == None:
                            pass
                        else:
                            old_location = patientObject.location
                            patientObject.location = Facility_ID
                            if self.getHospitalById(old_location) == None:
                                pass
                            else:
                                print('good succ')
                                self.getQuarantineById(Facility_ID).patients.append(patientObject)
                                self.getHospitalById(old_location).patients.remove(patientObject)
                                return print('Moved the patient from one hospital to another')

                        if self.getQuarantineById(patientObject.location) == Facility_ID:
                            return print('Patient is already inside of that quarantine')
                        else:
                            old_location = patientObject.location
                            patientObject.location = Facility_ID
                            self.getQuarantineById(Facility_ID).patients.append(patientObject)
                            self.getQuarantineById(old_location).patients.remove(patientObject)
                            return print('Patient moved from one quarantine area to another')


