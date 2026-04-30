def send_email_alert(message, receiver):
    import smtplib

    sender = "riteshsingh.aie@gmail.com"
    password = "your_app_password"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    email_message = f"Subject: Toddle Churn Alert\n\n{message}"

    server.sendmail(sender, receiver, email_message)
    server.quit()