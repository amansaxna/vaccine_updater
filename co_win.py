import requests
import pprint
import json
from datetime import date
import time

mail_content = ""

#slots = dict()
# api-endpoint gives appointment avail. of 1 week
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"  
# location given here
location = "199" #199 - faridabad #353 - katni

#GET data 
def get_data(mail_content):

    #create a range of dates form tommorow to 15 days w/ interval of 7 days
    today = date.today()
    day = today.day
    #d1 = today.strftime("%d")
    count = day
    while (day < count+28):
        #print(day)

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'district_id':location,'date' : day }
        
        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)
        print(r)
        # extracting data in json format
        data = r.json()
        
        # extracting data
        # of the first matching location
        if data["centers"] == [] :
            print("is empty")

        data = data["centers"]

        for centers in data :
            for sessions in centers['sessions'] :
                if sessions['available_capacity'] > 0 : 
                    pprint.pprint(centers['name'] )
                    mail_content += "<html><body><table>"
                    mail_content += "<tr><td>"+ str(sessions['date']) + "</td><td>  =>>  " +str(sessions['available_capacity']) +"</td><td> =></td><td>"+centers['name'] + "</td></tr>\n"
                    
        day = day + 7
    
    return mail_content

#sending mail update        
def send_mail(mail_content) :
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    # mail_content = "Hello,This is a simple mail. There is only text, The mail is sent using Python SMTP library.Thank You"

    #The mail addresses and password
    sender_address = 'aman0saxena@gmail.com'
    sender_pass = 'Gardner01'
    receiver_address = 'saxena2aman@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Vaccine slots available book it '   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    #session.sendmail(sender_address, 'sunny0rajat@gmail.com', text)
    #session.sendmail(sender_address, 'rajeev.saxena862@gmail.com', text)
  
    session.quit()
    print('Mail Sent')

#clock 
start_time = time.time()
seconds = 3 # 5min = 60sec *5 = 300 sec
iteration_no =1

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time > seconds:
        print("iterating AT: " + str(int(iteration_no))  + " Attempt")
        iteration_no +=1
        
        #Get Data
        mail_content = get_data(mail_content)
        
        #send mail
        if mail_content != "":
            mail_content = "Vaccine Slots Availble "+" AT "+ str(location) +"\n" + mail_content
            #pprint.pprint(mail_content)
            send_mail(mail_content +"</table></body></html>"+ str("https://www.cowin.gov.in/home") )
        else :
            print("NO NEW APPOINTMENS YET")

        start_time = time.time()
        continue

# printing the output
#pprint.pprint("Vaccine Slots Availble \n"+mail_content)
#print("Vaccine Slots Availble  at : \n"+mail_content)

