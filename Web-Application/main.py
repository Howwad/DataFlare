from flask import Flask, redirect, url_for, render_template, request, jsonify
import mysql.connector
import mysql

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mo.awwad21",
  database="robot"
)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/warranty')
def listWarranty():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM robot.warranty")
    data = cursor.fetchall()
    return render_template('list-warranty.html', data=data)

@app.route('/warranty/insert', methods=['GET', 'POST'])
def addWarranty():
    if request.method == 'POST':
        id = request.form['w_id']
        desc = request.form['w_desc']
        start_date = request.form['start_date']
        status = request.form['sw_status']
        end_date = request.form['end_date']
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO robot.warranty (w_id, w_desc, start_date, sw_status, end_date) VALUES (%s, %s,%s, %s,%s)", (id, desc, start_date, status, end_date))
        mydb.commit()
        return redirect(url_for('listWarranty'))
    else:
        return render_template('add-warranty.html')

@app.route('/delete_row_warranty/<int:id>')
def delete_row_warranty(id):
    cursor = mydb.cursor()

    # Construct the SQL query to delete the row
    query = "DELETE FROM robot.warranty WHERE w_id = %s"
    values = (id,)
    cursor.execute(query, values)
       
    # Commit the changes to the database
    mydb.commit()

    # Return a JSON response indicating success
    response = {'success': True}
    return jsonify(response)

#error
@app.route('/error')
def listError():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM robot.error")
    data = cursor.fetchall()
    return render_template('list-error.html', data=data)

@app.route('/error/insert', methods=['GET', 'POST'])
def addError():
    if request.method == 'POST':
        id = request.form['error_id']
        desc = request.form['error_desc']
        severity = request.form['error_severity']
        type = request.form['component_type']
        status = request.form['status']
        error_creation_date = request.form['error_creation_date']
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO robot.error (error_id, error_desc, error_severity, component_type, status, error_creation_date) VALUES (%s, %s,%s, %s,%s, %s)", (id, desc, severity, type, status, error_creation_date ))
        mydb.commit()
        return redirect(url_for('listError'))
    else:
        return render_template('add-error.html')

@app.route('/delete_row_error/<int:id>')
def delete_row_error(id):
    cursor = mydb.cursor()

    # Construct the SQL query to delete the row
    query = "DELETE FROM robot.error WHERE error_id = %s"
    values = (id,)
    cursor.execute(query, values)
       
    # Commit the changes to the database
    mydb.commit()

    # Return a JSON response indicating success
    response = {'success': True}
    return jsonify(response)

#supervisor
@app.route('/supervisor')
def listSupervisor():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM robot.supervisor")
    data = cursor.fetchall()
    return render_template('list-supervisor.html', data=data)

@app.route('/supervisor/insert', methods=['GET', 'POST'])
def addSupervisor():
    if request.method == 'POST':
        id = request.form['supervisor_id']
        role = request.form['role']
        name = request.form['name']
        contact_information = request.form['contact_information']
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO robot.supervisor (supervisor_id, role, name, contact_information) VALUES (%s, %s,%s, %s)", (id, role, name,contact_information))
        mydb.commit()
        return redirect(url_for('listSupervisor'))
    else:
        return render_template('add-supervisor.html')

@app.route('/delete_row_supervisor/<int:id>')
def delete_row_supervisor(id):
    cursor = mydb.cursor()

    # Construct the SQL query to delete the row
    query = "DELETE FROM robot.supervisor WHERE supervisor_id = %s"
    values = (id,)
    cursor.execute(query, values)
       
    # Commit the changes to the database
    mydb.commit()

    # Return a JSON response indicating success
    response = {'success': True}
    return jsonify(response)


#user
@app.route('/robot')
def listRobot():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM robot.robot_component")
    data = cursor.fetchall()
    return render_template('list-robot-component.html', data=data)

@app.route('/robot/insert', methods=['GET', 'POST'])
def addRobot():
    if request.method == 'POST':
        id = request.form['rc_id']
        serialNumber = request.form['serial_number']
        modelNumber = request.form['model_number']
        type = request.form['type']
        manufacturer = request.form['manufacturer']
        rc_description = request.form['rc_description']
        robot_id = request.form['robot_id']
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO robot.robot_component (rc_id, serial_number, model_number, type, manufacturer, rc_description, robot_id) VALUES (%s, %s,%s, %s,%s, %s, %s)", (id, serialNumber, modelNumber,type, manufacturer, rc_description, robot_id))
        mydb.commit()
        return redirect(url_for('listRobot'))
    else:
        return render_template('add-robot-component.html')

@app.route('/delete_row_robot/<int:id>')
def delete_row_robot(id):
    cursor = mydb.cursor()

    # Construct the SQL query to delete the row
    query = "DELETE FROM robot.robot_component WHERE rc_id = %s"
    values = (id,)
    cursor.execute(query, values)
       
    # Commit the changes to the database
    mydb.commit()

    # Return a JSON response indicating success
    response = {'success': True}
    return jsonify(response)

#user
@app.route('/robot/warranty')
def listRobotWarranty():
    cursor = mydb.cursor()
    cursor.execute("SELECT rc.serial_number, rc.model_number, rc.manufacturer, rc.rc_description, rc.robot_id, r.w_id, w.w_desc, w.start_date, w.sw_status FROM robot_component rc LEFT OUTER JOIN robot r ON rc.robot_id = r.robot_id INNER JOIN warranty w ON r.w_id = w.w_id GROUP BY rc.serial_number, rc.model_number, rc.manufacturer, rc.rc_description, rc.robot_id, r.w_id, w.w_desc, w.start_date, w.sw_status ORDER BY rc.serial_number ASC;")
    data = cursor.fetchall()
    return render_template('list-robot-comp-warranty.html', data=data)

@app.route('/robot/machine')
def listRobotMachine():
    cursor = mydb.cursor()
    cursor.execute("SELECT rc.serial_number, rc.model_number, rc.manufacturer, rc.rc_description, rc.robot_id, r.machine_model_number, m.location, m.name, m.manufacturer FROM robot_component rc INNER JOIN robot r ON rc.robot_id = r.robot_id LEFT OUTER JOIN machine m ON r.machine_model_number = m.model_number;")
    data = cursor.fetchall()
    return render_template('list-robot-comp-machine.html', data=data)

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8080, debug=True)