import smtplib

server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
server.login("whychain@vk.com", "Fp2frTdepGJpR3eM0Syk")
server.sendmail(
    "whychain@vk.com",
    "a_mir_m@mail.ru",
    "Subject: Test Email\n\nThis is a test email!"
)
server.quit()