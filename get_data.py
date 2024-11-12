import sqlite3

# Kết nối tới database
conn = sqlite3.connect('email_tracking.db')
cursor = conn.cursor()

# Truy vấn tất cả các sự kiện mở email
cursor.execute("SELECT email, campaign_id, event_type, timestamp FROM email_events")
events = cursor.fetchall()

# Hiển thị tất cả các sự kiện trong database
print("Danh sách các sự kiện trong database:")
for event in events:
    email, campaign_id, event_type, timestamp = event
    print(f"Email: {email}, Campaign ID: {campaign_id}, Event: {event_type}, Timestamp: {timestamp}")

# Đóng kết nối
conn.close()