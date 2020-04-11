from flask import Flask, request, jsonify
from CovidManagementSystem import *
import random


app = Flask(__name__)

# Root object for the management system
ms = CovidManagementSystem()

#========================================= ADDING ==============================================#

# ADD a new hospital (parameters: name, capacity).
@app.route("/hospital", methods=["POST"])
def addHospital():
    ms.addHospital(request.args.get('name'), request.args.get('capacity'))
    if int(request.args.get('capacity')) < 1:
        return jsonify(important_note = 'Hospital capacity cannot be negative')
    if int(request.args.get('capacity')) > 5000:
        return jsonify(important_note = 'Hospital capacity cannot be more than 5000')

    return jsonify(
        f"Added a new hospital called {request.args.get('name')} with capacity {request.args.get('capacity')}")

# ADD a new quarantine area to a specific hospital
@app.route("/hospital/<hospital_id>/quarantine", methods = ["POST"])
def addQuarantine(hospital_id):
    h = ms.getHospitalById(hospital_id)
    h.addQuarantine(request.args.get('name'), request.args.get('capacity'), hospital_id)

    if int(request.args.get('capacity')) <= 0:
        return jsonify(important_note = 'Cannot add quarantines with negative capacity')
    elif int(request.args.get('capacity')) >5000:
        return jsonify(important_note = 'Cannot add quarantines with capacity greater than 5000')

    return jsonify\
            (
                f"Added a new quarantine called {request.args.get('name')} with capacity {request.args.get('capacity')}"
            )

# ADD a new patient to the system
@app.route("/patient", methods = ["POST"])
def addPatient():
    ms.addToSystem(request.args.get('name'), request.args.get('dob'))
    if request.args.get('name') == None or request.args.get('dob') == None:
        return jsonify(imporant_note='One or two parameters for patient were not given (name, dob)')

    name = re.findall(r'([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)', request.args.get('name').title())
    if name == []:
        return jsonify(important_note='Name must be provided in format <name surname>')

    date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', request.args.get('dob'))
    if date_of_birth == []:
        return jsonify(important_note='Unexpected characters found or date format not correct <year.month.day>')
    elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
        return jsonify('Year of birth not compatible')
    elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
        return jsonify('Month of birth not compatible')
    elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
        return jsonify('Day of birth not compatible')

    return jsonify\
            (
                f"Added a new Patient to the system with name {name[0]}"
            )

# ADD a new patient to a specific hospital, the name is in format <name surname> and the date is in format <year.month.day>
# Patient can only be added if the capacity of the hospital is more than 0
@app.route("/hospital/<hospital_id>/patient", methods=["POST"])
def admitPatient(hospital_id):
    h = ms.getHospitalById(hospital_id)
    if (h != None):
        h.admission(request.args.get('name'), request.args.get('dob'), hospital_id)
        if request.args.get('name') == None or request.args.get('dob') == None:
            return jsonify(imporant_note = 'One or two parameters for patient were not given (name, dob)')
        elif h.capacity - len(h.patients) < 0:
            return jsonify(important_note = 'Hospital is full, cannot add more patients')

        name = re.findall(r'([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)', request.args.get('name').title())
        if name == []:
            return jsonify(important_note = 'Name must be provided in format <name surname>')
        date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', request.args.get('dob'))
        if date_of_birth == []:
            return jsonify(important_note='Unexpected characters found or date format not correct <year.month.day>')
        elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
            return jsonify('Year of birth not compatible')
        elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
            return jsonify('Month of birth not compatible')
        elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
            return jsonify('Day of birth not compatible')

    else:
        return jsonify(imporatnt_note = f'Hospital with ID {hospital_id} was not found')
    return jsonify(message = f'patient named {name[0]} was added to hospital {ms.getHospitalById(hospital_id).name}')

# ADD a new patient to a specific quarantine from the system, or from the same hospital, cannot add patients from other hospitals, for that use
# the move function. Can also only be done if the patient is infected.
@app.route("/quarantine/<qu_id>/<pat_id>", methods = ["POST"])
def admitPatientToQarea(qu_id, pat_id):

    hosp = [h for h in ms.getHospitals()]
    if hosp == []:
        return jsonify(message=f'No hospitals were found in the system')

    quarantine = ms.getQuarantineById(qu_id) # we get the quarantine from the hospital

    if quarantine == None:
        return jsonify(message = f'Quarantine area with ID {qu_id} was not found in any hospital')
    elif quarantine.capacity - len(quarantine.patients) <= 0:
        return jsonify(important_note = 'Quarantine full, cannot add more patients')


    sysLi = [p for p in ms.System.patients] # patients from the system
    hosp = ms.getHospitalById(quarantine.location) # the hospital where the quarantine is located
    QLi = hosp.patients # patients from the specific hospital

    for p in sysLi:
        for key, value in p.getID().items():
            if key == pat_id:
                if value.dead == True or value.dispatched == True:
                    return print('Cannot move dead or dispatched patients')
                if value.infected == False:
                    return jsonify('Cannot admit the patient to the quarantine area, patient is not infected')
                quarantine.patients.append(value)
                value.location = quarantine.ID
                ms.System.patients.remove(value)
                return jsonify(message = f'Added patient {p.name} from the system to quarantine named {quarantine.name}')

    for p in hosp.patients:
        for key, value in p.getID().items():
            if key == pat_id:
                if value.dead == True or value.dispatched == True:
                    return print('Cannot move dead or dispatched patients')
                if value.infected == False:
                    return jsonify('Cannot admit the patient to the quarantine area, patient is not infected')
                quarantine.patients.append(value)
                value.location = quarantine.ID
                QLi.remove(value)
                return jsonify(message = f'Added patent {p.name} from the hospital {hosp.name} to quarantine named {quarantine.name}')

    return jsonify(message = f'Patient with ID {pat_id} was not found in the system or in the hospital where the quarantine is situated')

# ADD a new staff to the system
@app.route("/staff", methods = ['POST'])
def addStaff():
        ms.addStaff(request.args.get('name'), request.args.get('dob'), request.args.get('type'), None)
        name = re.findall(r'([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)', request.args.get('name').title())
        if name == []:
            return jsonify(important_note='Name must be provided in format <name surname>')

        date_of_birth = re.findall(r'(\d+)\.(\d+)\.(\d+)', request.args.get('dob'))
        if date_of_birth == []:
            return jsonify(important_note='Unexpected characters found or date format not correct <year.month.day>')
        elif int(date_of_birth[0][0]) > 2100 or int(date_of_birth[0][0]) < 1900:
            return jsonify('Year of birth not compatible')
        elif int(date_of_birth[0][1]) > 12 or int(date_of_birth[0][1]) < 1:
            return jsonify('Month of birth not compatible')
        elif int(date_of_birth[0][2]) > 31 or int(date_of_birth[0][2]) < 1:
            return jsonify('Day of birth not compatible')
        elif request.args.get('type') != 'doctor' and request.args.get('type') != 'nurse':
            return jsonify('Staff could not be added because type is not doctor or nurse')
        else:
            return jsonify(message = 'Added a new staff memeber to the system')


#================================================= DELETING =============================================#


# Delete a certain hospital from the system
@app.route("/hospital/<hospital_id>", methods=['DELETE'])
def deleteHospital(hospital_id):
    result = ms.deleteHospital(hospital_id)
    if (result):
        message = f"Hospital with id{hospital_id} was deleted"
    else:
        message = "Hospital not found"
    return jsonify(success=result)

# Delete a certain quarantine from the hospital, if it's not empty, moved all patients to the system
@app.route("/quarantine/<qu_id>", methods = ['DELETE'])
def delQ(qu_id):
    q = ms.getQuarantineById(qu_id)
    hosp = ms.getHospitalById(q.location)
    sum_of_space = 0

    if q == None:
        return jsonify(message=f'Quarantine with ID {qu_id} has not been found')

    hospital = ms.getHospitalById(q.location)
    all_quarantines = [q for q in hospital.quarantines] # all quarantines in the hospital where the first one is

    for quaran in all_quarantines:
        space = quaran.capacity - len(quaran.patients)
        sum_of_space += space

    if len(q.patients) == 0:
        hosp.quarantines.remove(q)
        return jsonify(message = 'Quarantine area removed')

    if len(q.patients) > sum_of_space:
        return jsonify(message = f'There is not enough space in other quarantine areas to move the patients from this one {sum_of_space - len(q.patients)}')

    else:
        for p in q.patients:
            p.location = qu_id
            ms.System.patients.append(p)
        hosp.quarantines.remove(q)

    return jsonify(message = 'Patients moved to the system, please move them to other quarantines')



# Delete a staff memeber from the hospital
@app.route("/staff/<staff_id>", methods = ['DELETE'])
def delStaff(staff_id):

    chosen_staff = None
    a = ms.getStaffMembers()
    for dict in a:
        for key, value in dict.items():
            if key == staff_id:
                chosen_staff = value
    if chosen_staff == None:
        return jsonify(important_note = f'Staff member with ID {staff_id} was not found.')
    else:
        ms.DelStaff(chosen_staff)
        return jsonify(message = 'Staff memeber deleted')

                    
#================================================= SHOWING ALL =============================================#

#Show all staff members in the system, in hospitals and quarantine areas
@app.route("/staff", methods = ['GET'])
def getStaff():
    return jsonify(ms.getAllStaff())

# Show all patients in a given hospital
@app.route("/hospital/<hospital_id>/patients", methods=["GET"])
def getPatients(hospital_id):
    h = ms.getHospitalById(hospital_id)
    if (h != None):
        return jsonify(patients = [p.showPatients() for p in h.patients])
    else:
        return jsonify(important_note = f'Hospital with ID {hospital_id} not found')

# Show all the details of a hospital of the given hospital_id.
@app.route("/hospital/<hospital_id>", methods=["GET"])
def hospitalInfo(hospital_id):
    h = ms.getHospitalById(hospital_id)
    if (h != None):
        return jsonify(h.serialize())
    return jsonify(
        success=False,
        message="Hospital not found")

# Show all patients in the system
@app.route("/system", methods=["GET"])
def getPatientsFromSystem():
        return jsonify (Patients_in_the_system = [p.showPatients() for p in ms.System.patients],
                        Staff_in_the_system = [s.showStaff() for s in ms.System.staff])

#Show all details of a quarantine
@app.route("/quarantine/<qu_id>", methods = ["GET"])
def getQuaratine(qu_id):
    q = ms.getQuarantineById(qu_id)
    if q == None:
        return jsonify(important_note = f'Quarantine area with ID {qu_id} was not found.')
    return jsonify(message = q.returnQ())

# Show all hospitals in the system
@app.route("/hospitals", methods=["GET"])
def allHospitals():
    return jsonify(hospitals = [h.serialize() for h in ms.getHospitals()])

# Show all quarantine areas in a certain hospital
@app.route("/hospital/<hospital_id>/quarantines")
def getQuarantines(hospital_id):
    h = ms.getHospitalById(hospital_id)
    if (h != None):
        return jsonify(quarantines = [q.showQuarantines() for q in h.quarantines])

# Show all quarantine areas in every hospital
@app.route("/quarantines", methods = ['GET'])
def showAllQAreas():
    return jsonify([q.showQuarantines() for q in ms.ShowAllQ()])
        

# Show all the stats
@app.route("/stats", methods = ['GET'])
def stats():
    Li_sys = []
    Li_hosp = []
    Li_q = []

    for p in ms.System.patients:
        Li_sys.append(p)
    for h in ms.getHospitals():
        for p in h.patients:
            Li_hosp.append(p)
    for h in ms.getHospitals():
        for q in h.quarantines:
            for p in q.patients:
                Li_q.append(p)

    final = Li_sys + Li_hosp + Li_q
    counter = 0
    for p in final:
        if p.infected == True:
            counter+=1

    if final == []:
        return jsonify(important_note = 'No patients were found in the system')

    infected = (counter/len(final)) * 100

    final1 = Li_q + Li_hosp

    occup_hosp = 0
    occup_quaran = 0
    for h in ms.getHospitals():
        occup_hosp+=h.occupancy()
    for h in ms.getHospitals():
        for q in h.quarantines:
            occup_quaran+=q.occupancy()

    final_ocuppancy = occup_hosp + occup_quaran

    if final1 == []:
        occupancy = 0
    else:
        occupancy = final_ocuppancy / len(final1)



    in_isolation = len(Li_q)
    status_dead = 0
    status_dispatched = 0

    for p in Li_sys:
        if p.dead == True:
            status_dead+=1
        elif p.dispatched == True:
            status_dispatched += 1




    return jsonify({'Percentage of all infected patients' : infected,
                   'Percentage of occupancy in all the facilities' : occupancy,
                   'Percentage of patients in isolation(quarantine)' : in_isolation/len(final),
                   'Percentage of discharged patients' : (status_dispatched/len(final)) * 100,
                   'Percentage of dead patients' : (status_dead/len(final)) * 100})


#========================================== MOVING ==============================================#

# Move patient found from any ID to a facility
@app.route("/patient/<pat_id>/move/<facility_id>", methods=['PUT'])
def admit(pat_id, facility_id):
    pat = None
    for h in ms.getHospitals():
        for p in h.patients:
            if pat_id == p.ID:
                pat = p
    for p in ms.System.patients:
        if pat_id == p.ID:
            pat = p
    for h in ms.getHospitals():
        for q in h.quarantines:
            for p in q.patients:
                if pat_id == p.ID:
                    pat = p

    if pat.location == facility_id:
        return jsonify(important_note = 'Patient is already located in this facility')
    elif pat.location == None and facility_id == 'system':
        return jsonify(important_note='Patient is already located in this facility')



    a = ms.MovePatient(pat_id, facility_id)
    return jsonify(message = 'successfully moved patient')

# Move staff with ID to a hospital or a quarantine area
@app.route("/staff/<staff_id>", methods = ['PUT'])
def moveStaff(staff_id):
    chosen_staff = None
    a = ms.getStaffMembers()
    for dict in a:
        for key, value in dict.items():
            if key == staff_id:
                chosen_staff = value

    if chosen_staff == None:
        return jsonify(important_note = f'Staff member with ID {staff_id} was not found')

    chosen_staff_old_location = chosen_staff.location
    ms.MoveStaff(chosen_staff, request.args.get('location'))

    if chosen_staff_old_location == request.args.get('location'):
        return jsonify(message = 'Staff could not be moved to the position they are already in')
    if chosen_staff_old_location == None and chosen_staff.location == 'system':
        return jsonify(message = 'Staff could not be moved to the position they are already in')
    else:
        return jsonify(message = 'succ cess')


#======================================== DIAGNOSIS ==============================================#

#Simulating a diagnosis test, only possible if the patient is in the hospital and there is a doctor inside
@app.route('/patient/<pat_id>/diagnosis', methods = ['POST'])
def SimulateTest(pat_id):

    specific_patient = None # The patient
    staff_li = []
    patient_li = []
    doctors = []
    doctors_list = [] # List of all doctors

    for h in ms.getHospitals():
        for p in h.patients:
            patient_li.append(p.getID())

    for h in ms.getHospitals():
        for s in h.staff:
            staff_li.append(s.getMember())


    for dict in patient_li:
        for key, value in dict.items():
            if pat_id == key:
                specific_patient = value
            else:
                return jsonify(message = f'No patient of ID {pat_id} was found in any hospital')

    if specific_patient.tested == True:
        return jsonify(message = 'This patient has already been tested')

    for dict in staff_li:
        for key, value in dict.items():
            doctors.append(value)


    for doctor in doctors:
        if doctor.type == 'doctor':
            doctors_list.append(doctor)
        else:
            pass


    if patient_li == []:
        return jsonify(message = 'There are no patients found in any hospitals')

    if doctors_list == []:
        return jsonify(message = 'There are no doctors found anywhere, diagnosis cannot be performed')


    if ms.getHospitalById(specific_patient.location) == None:
        return jsonify(message = 'The patient is not located inside of a hospital')

    doc = [] # the doctors that are in the hospital the patient is located as well


    for doctor in doctors_list:
        if specific_patient.location == doctor.location:
            doc.append(doctor)
        elif specific_patient.location != doctor.location:
            return jsonify(message = 'There are no doctors in the hospital the patient is located in, diagnosis cannot be performed')


    if doc == []:
        return jsonify(message = 'No doctors found in the hospital the patient is located in')

    random_doctor = random.choice(doc)
    chance_to_get_diagnozed = random.randint(0,100)

    if chance_to_get_diagnozed >=10:
        specific_patient.tested = True
        return jsonify(message = f'Doctor named {random_doctor.name} performed the diagnosis on the patient named {specific_patient.name}, the patient does not have Covid-19')
    elif chance_to_get_diagnozed <10:
        specific_patient.tested = True
        specific_patient.infected = True
        return jsonify(message = f'Doctor named {random_doctor.name} performed the diagnosis on the patient named {specific_patient.name}, the patient tested Covid-19 positive, and needs to be moved to a quarantine.')

#Simulating a cure for patient, only possible if the patient is inside a quarantine
@app.route('/patient/<pat_id>/cure', methods = ['POST'])
def CurePatient(pat_id):
    patient = None
    patient_li = []

    for h in ms.getHospitals():
        for q in h.quarantines:
            for p in q.patients:
                patient_li.append(p.getID())

    if patient_li == []:
        return jsonify(important_note = 'No patients were found')


    for dict in patient_li:
        for key, value in dict.items():
            if key == pat_id:
                patient = value

    if patient == None:
        return jsonify(message = f'Patient with ID {pat_id} not found in any hospital or quarantines')

    if patient.infected == True and patient.tested == True:
        cured = random.randint(0,100)
        if cured < 3:
            patient.dead = True
            admit(patient.ID, 'system')
            return jsonify(message = 'Curing the patient was not successful, the patient has died.')
        if cured >=3:
            patient.dispatched = True
            admit(patient.ID, 'system')
            return jsonify(message = 'Patient has successfully been cured, dispatching patient')


    else:
        return jsonify('Error has occured')

#========================================== SERVER SIDE ==========================================#
# The index of the system
@app.route("/")
def index():
    return jsonify(
        success=True,
        message="Your server is running! Welcome to the Covid API.")

# Custom headers
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE"
    return response

# The port number
if __name__ == "__main__":
    app.run(debug=False, port=8888)
