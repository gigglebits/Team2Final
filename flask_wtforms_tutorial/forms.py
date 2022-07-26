"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
)
#from datetime import date
#from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class UserOptionForm(FlaskForm):
    """User option form."""
    #When the user submits the user option form if the choose Admin option = "1"
    #if they choose Reserve a seat, option = "2"
    option = SelectField("Choose an Option",[DataRequired()],
        choices=[
            ("", "Choose an option"),
            ("1", "Admin Login"),
            ("2", "Reserve a seat"),
        ],
    )

    submit = SubmitField("Submit")


class ReservationForm(FlaskForm):
    """Reservation Form"""
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    row = SelectField("Choose Row", [DataRequired()],
        choices=[
            ("", "Choose a Row"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
    )
    seat = SelectField("Choose Seat", [DataRequired()],
        choices=[
            ("", "Choose a Seat"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
        ],
    )

    reserve = SubmitField("Reserve a Seat")

class AdminLoginForm(FlaskForm):
    """Admin login form"""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    username = StringField('Username', [DataRequired()])
    password = StringField('Password', [DataRequired()])

    login = SubmitField("Login")


class extraFunctionality():
    #reads all of the reservations in reservations.txt
    def read_reservations(self):
        f = open('reservations.txt')
        lines = f.readlines()
        records = []
        for line in lines:
            record = {}
            components = line.split(',')
            record['fname'] = components[0].strip()
            #print(f"fName: {record.get('fname')}")
            record['row'] = components[1].strip()
            #print(f"Row: {record.get('row')}")
            record['seat'] = components[2].strip()
            #print(f"Seat: {record.get('seat')}")
            record['confirmation'] = components[3].strip()
            #print(f"Confirmation: {record.get('confirmation')}")
            records.append(record)
        f.close()
        #returns a list of dicts for each reservation
        return records
    
    #Takes a string and appends it to the reservations.txt
    def write_to_reservations(self, thingToWrite):
        f = open('reservations.txt', 'a')
        f.write(thingToWrite)
        f.close

    #Creates a new array filled with O's then reads the reservations and finally replaces reserved seats with X's
    def get_matrix(self):
        records = self.read_reservations()
        matrix = [['O', 'O', 'O', 'O'] for row in range(12)]
        for x in records:
            row = int(x.get('row'))
            col = int(x.get('seat'))
            matrix[row][col] = 'X'
        #Returns the current array. 
        return matrix

    #Reads the reservations, then gets the cost matrix and adds together the prices of the reserved seats. Returns the total.
    def calculate_cost(self):
        records = self.read_reservations()
        matrix = self.get_cost_matrix()
        total = 0
        for x in records:
            row = int(x.get('row'))
            col = int(x.get('seat'))
            total += matrix[row][col]
        return total

    def get_cost_matrix(self):
        cost_matrix = [[100, 75, 50, 100] for row in range(12)]

        #returns a cost matrix as a list of lists. 
        return cost_matrix
    
    #Checks Seat Availability and returns true if it's available and false if it isn't. 
    def check_availability(self, row, col):
        current = self.get_matrix()
        row = row-1
        col = col-1
        if current[row][col] == 'X':
            return False
        else:
            return True
    
    def make_confirmation(self, fname):
        salt = "ITFOTC4320"
        confirmation = ''.join(map(''.join, zip(fname, salt)))
        return confirmation

#def test():
#    extra = extraFunctionality()
#    matrix = extra.get_matrix()
#    for x in matrix:
#        print(x)

#test()