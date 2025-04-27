import os
import shutil
import smtplib
import schedule
import time
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  

load_dotenv()


SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
DB_FILE = os.getenv('DB_FILE')       
BACKUP_DIR = os.getenv('BACKUP_DIR') 

def backup_and_send_email():
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        if not os.path.exists(DB_FILE):
            raise Exception(f"Không tìm thấy file database: {DB_FILE}")

        file = os.path.basename(DB_FILE)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_filename = f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}"
        dst = os.path.join(BACKUP_DIR, dst_filename)

       
        shutil.copy2(DB_FILE, dst)

        #backup thành công 
        send_email(
            subject="Backup Database Thành Công",
            body=f"Đã backup file '{file}' lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} thành '{dst_filename}'."
        )

        print("Backup và gửi email thành công lúc:", time.strftime("%H:%M:%S"))

    except Exception as e:
        #backup thất bại
        send_email(
            subject="Backup Database Thất Bại",
            body=f"Lỗi khi backup: {str(e)}"
        )
        print(" Backup thất bại:", e)

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

    except Exception as e:
        print(" Lỗi khi gửi email:", e)

# Đặt lịch backup mỗi ngày lúc 00:00
schedule.every().day.at("00:00").do(backup_and_send_email)


print(" Chương trình backup database đang chạy...")

while True:
    schedule.run_pending()
    time.sleep(1)
