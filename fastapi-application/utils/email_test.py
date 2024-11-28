import smtplib

server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
server.login("mail@mail.com", "password")
server.sendmail(
    "mail@mail.com",
    "reciever@mail.com",
    "Subject: Test Email\n\nThis is a test email."
)
server.quit()
