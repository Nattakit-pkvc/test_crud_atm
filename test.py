@app.route("/check_balance", methods=["GET", "POST"])
def check_balance():
    if request.method == "POST":
        username = request.form.get('username')
        print("Input:",username)
        
        # Connect to database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        my_cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM atm_member_b WHERE username = %s"
        my_cursor.execute(sql, (username,))
        result = my_cursor.fetchone()  # Fetch one row
        

        if result:
            session['alert_status'] = "success"
            session['alert_message'] = "Already Check!"
            return render_template("check_balance.html", result=result)  # Send a single result
        else:
            session['alert_status'] = "fail"
            session['alert_message'] = "Something went wrong!"
            return redirect(url_for('index'))  # Redirect to main page if no user found
         # Show Messages


    return render_template("check_balance.html", result=result)  # Display form for GET request
