import smtplib, os, json
from email.message import EmailMessage

def notification(body):
    # Send an email notification
    try:
        '''Since google has stoped unsafe app to use the google account I am only sending the token back'''
        msg = json.loads(body) # Convert the JSON object to a Python dictionary
        mp3_file_id = msg["mp3_file_id"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        recever_address = msg["username"]

        msg = EmailMessage()
        msg.set_content(f"Your MP3 file is ready for download. \nFile ID: {mp3_file_id}")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = recever_address

        try:
            session = smtplib.SMTP("smtp.gmail.com", 587)
        except:
            raise "Error: unable to send email"
        session.starttls() # enable security
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, recever_address)
        session.quit()

        print("Email sent successfully")
    except Exception as e:
        print(e)
        return str(e)
    return None
