import time
from email.message import EmailMessage
import ssl
import smtplib
from connect_database import mycursor, db

email_sender='kavincdsrough@gmail.com'
email_password='ucvqcmtbwxgzczvg'


def pdf_conversion_mail_send(case_id):
    subject = 'PDF CONVERSION update mail'

    body = """
    Hai, This is python generated mail, The PDF conversion will be started now
    """
    mycursor.execute("SELECT client_mail from tbl_workflow_mail where case_id=%s",[case_id])
    res=mycursor.fetchall()
    for i in res:
        email_receiver=i[0]
        em = EmailMessage()
        em['FROM'] = email_sender
        em['TO'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            mycursor.execute("update tbl_workflow_mail set pdf_conversion=1  where case_id = %s ", [case_id])
            db.commit()
            print("Mail send succesfully for PDF conversion")

while True:
    print("  ")
    time.sleep(5)
    result=0

    mycursor.execute("select * from tbl_workflow_mail")
    result = mycursor.fetchall()
    if result:
        for i in result:
            case_id=i[0]
            pdf_convertion=i[3]
            if pdf_convertion==0:
               print(case_id," case id..")
               pdf_conversion_mail_send(case_id)

    else:
        print("No more case for PDF conversion mail")
        time.sleep(20)

