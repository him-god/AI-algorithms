from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from model.Appointment import Appointment
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None

def strong_pw_checker(pw):
    if len(pw) < 8:
        return False
    if pw.islower() or pw.upper() == pw:
        return False
    if pw.isdigit():
        return False
    if pw.find("!") == -1 and pw.find("@") == -1 and pw.find("#") == -1 and pw.find("?") == -1:
        return False
    return True

def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        print("Please input 'create_patient <username> <password>' to create user")
        return
    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # check 3: check if the password is strong
    if not strong_pw_checker(password):
        print("Please use a strong password")
        print("Strong password guidelines: ")
        print("1. At least 8 characters.")
        print("2. A mixture of both uppercase and lowercase letters.")
        print("3. A mixture of letters and numbers.")
        print("4. Inclusion of at least one special character, from '!', '@', '#', '?'.")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)



def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
    except Exception as e:
        print("Error occurred when checking username")
        print(e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        print("Please input 'create_caregiver <username> <password>' to create user")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return
    
    # check 3: check if the password is strong
    if not strong_pw_checker(password):
        print("Please use a strong password")
        print("Strong password guidelines: ")
        print("1. At least 8 characters.")
        print("2. A mixture of both uppercase and lowercase letters.")
        print("3. A mixture of letters and numbers.")
        print("4. Inclusion of at least one special character, from '!', '@', '#', '?'.")

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        print("Please input 'login_patient <username> <password>' to log in")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        print("Please input 'login_caregiver <username> <password>' to log in")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # search_caregiver_schedule <date>
    # check 1: user needs to login first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        print("Please input 'search_caregiver_schedule <date>' to search caregiver schedule")
        return
    
    date = tokens[1]
    
    # check 3: input date should be hyphenated in the format mm-dd-yyyy
    try:
        date_tokens = date.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
    except IndexError:
        print("Please input date as 'mm-dd-yyyy'.")
        return
    except ValueError:
        print("Please input date as 'mm-dd-yyyy'.")
        return
        
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()

    get_appointment = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username"
    get_vaccine = "SELECT Name, Doses FROM Vaccines"
    caregiverList = []
    vaccineList = {}
    try:
        d = datetime.datetime(year, month, day)
        cursor.execute(get_appointment, d)
        for row in cursor:
            caregiverList.append(str(row))
        cursor.execute(get_vaccine)
        for row in cursor:
            vaccineList[str(row[0])] = int(row[1])
        print('Available caregivers: ')
        for caregiver in caregiverList:
            print(caregiver + '; ')
        print('Number of doses for each vaccine:')
        for vaccine in vaccineList.keys():
            print(vaccine + ': ' + str(vaccineList[vaccine]) + ' remaining; ')
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        return
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()

def reserve(tokens):
    # reserve <date> <vaccine>
    # check 1: user needs to login as a patient first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    elif current_patient is None:
        print("Please login as a patient!")
        return
    
    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        print("Please input 'reserve <date> <vaccine>' to reserve appointment")
        return
    
    date = tokens[1]
    vaccine = tokens[2]
    
    # check 3: input date should be hyphenated in the format mm-dd-yyyy
    try:
        date_tokens = date.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
    except IndexError:
        print("Please input date as 'mm-dd-yyyy'.")
        return
    except ValueError:
        print("Please input date as 'mm-dd-yyyy'.")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    get_available_caregiver = "SELECT TOP 1 Username FROM Availabilities WHERE Time = %s AND \
                            Username NOT IN (SELECT Caregiver FROM Appointment WHERE Time \
                            = %s AND Cancel = 0) ORDER BY Username"
    try:
        d = datetime.datetime(year, month, day)
        cursor.execute(get_available_caregiver, (d, d))
        for row in cursor:
            caregiver = row['Username']
            if caregiver is None:
                print("No Caregiver is available!")
                return
            else:
                break
        current_vaccine = Vaccine(vaccine, 1).get()
        if current_vaccine == None:
            print("Not enough available doses!")
            return        
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        return
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()

    # create the appointment
    appointment = Appointment(d, caregiver, current_patient.get_username(), vaccine)

    try:
        aid = appointment.save_to_db()
        current_vaccine.decrease_available_doses(1)
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    print("Successfully reserve %s's appointment at %s" %(caregiver, date))
    print('Appointment ID: ' + str(aid))
    

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        print("Please input 'upload_availability <date>' to upload availability")
        return

    date = tokens[1]

    # check 3: input date should be hyphenated in the format mm-dd-yyyy
    try:
        date_tokens = date.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
    except IndexError:
        print("Please input date as 'mm-dd-yyyy'.")
        return
    except ValueError:
        print("Please input date as 'mm-dd-yyyy'.")
        return

    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        return
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    # cancel <appointment_id>
    # check 1: user needs to login first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    elif current_caregiver is not None:
        user = 'Caregiver'
        username = current_caregiver.get_username()
    elif current_patient is not None:
        user = 'Patient'
        username = current_patient.get_username()
    
    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        print("Please input 'cancel <appointment_id>' to cancel appointment")
        return
    
    # check 3: the appointment id needs to be an integer
    try:
        id = int(tokens[1])
    except ValueError:
        print('Please input a valid appointment id')

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    cancel_appointment = "UPDATE Appointment SET Cancel = 1 WHERE aid = %d AND " + user + " = %s"

    try:
        # check 4: users can't cancel other's appointment
        cursor.execute(cancel_appointment, (id, username))
        if cursor.rowcount == 1:
            print("Successfully cancel the appointment: %d" %id)
        conn.commit()
    except pymssql.Error as e:
        print("Cancel Appointment Failed")
        print("Db-Error:", e)
        return
    finally:
        cm.close_connection() 
    


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        print("Please input 'add_doses <vaccine> <number>' to add doses")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    # show_appointments
    # check 1: user needs to login first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    elif current_caregiver is not None:
        user = 'Caregiver'
        username = current_caregiver.get_username()
    elif current_patient is not None:
        user = 'Patient'
        username = current_patient.get_username()
    
    # check 2: the length for tokens need to be exactly 1 to include all information (with the operation name)
    if len(tokens) != 1:
        print("Please try again!")
        print("Please input 'show_appointments' to access user's appointment")
        return
    try:
        appointment = get_schedule(user, username)
        for ln in appointment:
            print(ln)
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return

def get_schedule(user, username):
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    get_appointment_details = "SELECT * FROM Appointment WHERE " + user + " = %s AND Cancel = 0 ORDER BY aid"
    result = []
    try:
        cursor.execute(get_appointment_details, username)
        # return all appointments
        for row in cursor:
            result.append('aid: ' + str(row['aid']) + ', ' + 'vaccine: ' + str(row['Vaccine']) + ', ' 
            + 'date: ' + str(row['Time']) + ', ' + user + ': ' + str(row[user]))
        return result
    except pymssql.Error as e:
        raise e
    finally:
        cm.close_connection()

def logout(tokens):
    # logout
    # check 1: user needs to have already logged in
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: the length for tokens need to be exactly 1 to include all information (with the operation name)
    if len(tokens) != 1:
        print("Please try again!")
        print("Please input 'logout' to log out")
        
    current_caregiver = None
    current_patient = None
    print('Log out successfully')


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == 'cancel':
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
