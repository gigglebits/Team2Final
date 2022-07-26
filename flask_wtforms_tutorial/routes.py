from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash
from .forms import *
import numpy


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    #check if the request method is POST. POST method means that form data was submitted
    #So, if method is POST we can get the form data 
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            #if form option is "1" go to the admin page
            return redirect('/admin')
        else:
            #if form option is "2" go to the reservations page
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = AdminLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        f = open('passcodes.txt')
        passcodestxt = f.readlines()
        credentials = {}

        for x in passcodestxt:
            line = x.split(',')
            print(f"Username:{line[0].strip()} Password:{line[1].strip()}")
            user = line[0].strip()
            userpass = line[1].strip()
            credentials[user] = userpass
        
        if username in credentials.keys():
            if password == credentials.get(username):
                print("match")
                extra = extraFunctionality()
                matrix = extra.get_matrix()
                total = extra.calculate_cost()
                return render_template("admin.html", form=form, template="form-template", matrix=matrix, total=total)
                #form = UserOptionForm()
                #return render_template("admin.html", form=form, template="form-template")
            else:
                my_error = "Username or Password not incorrect."
                return render_template("admin.html", form=form, template="form-template", my_error=my_error)
        else:
            my_error = "Username or Password not found."
            return render_template("admin.html", form=form, template="form-template", my_error=my_error)
                
    else:
        pass
    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    submitted = False
    extra = extraFunctionality()
    current_matrix = extra.get_matrix()

    if request.method == 'POST' and form.validate_on_submit():
        row = int(request.form['row'])
        col = int(request.form['seat'])
        if extra.check_availability(row, col):
            submitted = True
            fname = request.form['first_name']
            confirmation = extra.make_confirmation(fname)
            thingToWrite= f"{fname}, {row -1}, {col -1}, {confirmation}\n"
            extra.write_to_reservations(thingToWrite)
            updated_matrix = extra.get_matrix()
            return render_template("reservations.html", form=form, template="form-template", matrix=updated_matrix, submitted=submitted, row=row, col=col, confirmation=confirmation)

        else:
            message = "Oops, Looks like that seat's taken. Please try again."
            return render_template("reservations.html", form=form, template="form-template", matrix=current_matrix, submitted=submitted, message=message)
    return render_template("reservations.html", form=form, template="form-template", matrix=current_matrix, submitted=submitted)