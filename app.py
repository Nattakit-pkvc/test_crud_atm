from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector

app = Flask(__name__)

# For Database
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'atm_67_b'

# For Session
app.config['SECRET_KEY'] = 'your-secret-key'

# route for main page
@app.route("/")
def index():
    my_db = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASS,
            db = DB_NAME,
        )
    my_cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM atm_member_b"
    my_cursor.execute(sql)
    results = my_cursor.fetchall()
    
    # Show Messages
    if "alert_status" in session and "alert_message" in session:
        alert_message = {
            'status': session["alert_status"],
            'message': session["alert_message"],
        }
        del session["alert_status"]
        del session["alert_message"]
    
    else:
        alert_message = {
            'status': None,
            'message': None,
        }
    return render_template("index.html",alert_message = alert_message, results=results)

# route for Create Account Page
@app.route('/create_accout')
def create_accout():
    
    return render_template('create_accout.html')
    
# route for Create Account Process
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        account_number = request.form['account_number']
        username = request.form['username']
        balance = request.form['balance']
        print("Input:", account_number, username, balance)

        # connect to database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        my_cursor = my_db.cursor(dictionary=True)
        
        # Check if the account_number already exists
        my_cursor.execute("SELECT * FROM atm_member_b WHERE account_number = %s OR username = %s", (account_number, username))
        result = my_cursor.fetchone()
        if result:
            # Account number already exists
            session['alert_status'] = "fail"
            session['alert_message'] = "The username or account number has already been used.!"
            return redirect("/")
        
        # If account number does not exist, insert the new record
        
        sql = "INSERT INTO atm_member_b (account_number, username, balance) VALUES (%s, %s, %s)"
        val = (account_number, username, balance)
        my_cursor.execute(sql, val)
        my_db.commit()
        
        session['alert_status'] = "success"
        session['alert_message'] = "Already Created!"
        return redirect("/")

# route for Checking Balance
@app.route("/check_balance", methods=['GET', 'POST'])
def check_balance():
    if request.method == "POST":
        username = request.form['username']
        print("Input:", username)
        
        # Connect to Database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        
        my_cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM atm_member_b WHERE username = %s"
        val = (username,)
        my_cursor.execute(sql, val)
        results = my_cursor.fetchall()
        
        # เก็บ session username
        if results:
            session['username'] = username
            session['alert_status'] = "success"
            session['alert_message'] = "Login successful!"
        else:
            session['username'] = ""
            session['alert_status'] = "fail"
            session['alert_message'] = "Something went wrong!"
            return redirect("/")
        
        # Use redirect to avoid form re-submission on refresh
        return redirect("/check_balance")

    # Handle GET request
    else:
        username = session.get('username')
        # Connect to Database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        
        my_cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM atm_member_b WHERE username = %s"
        val = (username,)
        my_cursor.execute(sql, val)
        results = my_cursor.fetchall()
        
        # Show Messages
        if "alert_status" in session and "alert_message" in session:
            alert_message = {
                'status': session["alert_status"],
                'message': session["alert_message"],
            }
            del session["alert_status"]
            del session["alert_message"]
        else:
            alert_message = {
                'status': None,
                'message': None,
            }
            
        return render_template("check_balance.html", alert_message=alert_message, results=results, username=username)


# route for Logout
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('index'))  # Redirect to main page after logout

# Run server
if __name__ == '__main__':
    app.run(debug=True)