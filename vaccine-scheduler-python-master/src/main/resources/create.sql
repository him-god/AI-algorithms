CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointment (
    aid INT PRIMARY KEY,
    Time date, 
    Caregiver varchar(255),
    Patient varchar(255) REFERENCES Patients,
    Vaccine varchar(255) REFERENCES Vaccines,
    Cancel INT
    UNIQUE(Time, Caregiver),
    UNIQUE(Time, Patient),
    FOREIGN KEY(Time, Caregiver) REFERENCES Availabilities,
    CHECK (Cancel = 0 OR Cancel = 1)
)   