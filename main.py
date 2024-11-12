from flask import Flask, request, send_file
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Cấu hình Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("test-ranpak-0867b6a29f23.json", scope)
client = gspread.authorize(creds)

# Mở Google Sheet (thay bằng ID của sheet của bạn)
sheet = client.open_by_key("1DHT8q0Pou3yquMYQnud32ydwOygJ1X0dz1v1kHqlht0").worksheet("Report")

# Hàm ghi dữ liệu vào Google Sheets
def update_google_sheet(email, campaign_id, event_type):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([email, campaign_id, event_type, timestamp])

# Endpoint cho việc theo dõi mở email
@app.route('/track_open')
def track_open():
    email = request.args.get('email')
    campaign_id = request.args.get('campaign_id')
    if email and campaign_id:
        with sqlite3.connect('email_tracking.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO email_events (email, campaign_id, event_type) VALUES (?, ?, ?)",
                           (email, campaign_id, 'open'))
            conn.commit()
        # Cập nhật Google Sheets
        update_google_sheet(email, campaign_id, 'open')
    return send_file('1x1_pixel.png', mimetype='image/png')

# Endpoint cho việc theo dõi click
@app.route('/track_click')
def track_click():
    email = request.args.get('email')
    campaign_id = request.args.get('campaign_id')
    if email and campaign_id:
        with sqlite3.connect('email_tracking.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO email_events (email, campaign_id, event_type) VALUES (?, ?, ?)",
                           (email, campaign_id, 'click'))
            conn.commit()
        # Cập nhật Google Sheets
        update_google_sheet(email, campaign_id, 'click')
    return "Click tracked successfully"

# Khởi động server
if __name__ == '__main__':
    app.run(debug=True)
