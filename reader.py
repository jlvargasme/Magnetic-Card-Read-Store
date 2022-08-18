# Logic to read input from magnetic card reader and upload user
# to database

import json
import requests
import smtplib, ssl
import getpass

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "joselvdm@umich.edu"
#password = getpass.getpass("Email password: ")

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
  "api_key": "40cec2ec47605eb09286969b84f5eaeb-us11",
  "server": "us11"
})

list_id = "4abc78d557"

filename = "students.csv"

def process_string(str_in):
    inputs = str_in.split("&")
    um_id = inputs[0][8:16]
    
    name = inputs[1]
    last, first = name.split("/")

    uniqname = inputs[2].split("?")[0]
    uniqname = ''.join([i for i in uniqname if not i.isdigit()]).lower()

    return [um_id, first, last, uniqname]

def get_full_name(uniqname):

    url = "https://mcommunity.umich.edu/mcPeopleService/people/" + uniqname
    header = {
        "Content-Type": "application/json"
    }
    profile = requests.get(url, headers=header).text
    profile_json = json.loads(profile)
    fullname = profile_json["person"]["displayName"]
    email = profile_json["person"]["email"]

    return [fullname, email]

def write_data(data):
    file = open(filename, "a")

    for i in range(0, len(data)-1):
        file.write(data[i]+", ")
    file.write(data[-1]+"\n")

    file.close()
    return

# def send_email(data):
#     receiver_email = data[5]
#     context = ssl.create_default_context()
#     try:
#         server = smtplib.SMTP(smtp_server, port)
#         server.starttls(context=context)
#         server.login(sender_email, password)
#         message = """\
#         Subject: Test email

#         This message was sent from Python."""

#         server.sendmail(sender_email, receiver_email, message)
#     except Exception as e:
#         print(e)
#     finally:
#         server.quit()
#     return 

def add_to_list(member_info):
    try:
        #to add a new member
        response = mailchimp.lists.add_list_member(list_id, member_info)

        # to update or insert a member
        # response = mailchimp.lists.set_list_member(list_id, member_info["email_address"], member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

def process_data(str_in):
    [um_id, first, last, uniqname] = process_string(str_in)
    [fullname, email] = get_full_name(uniqname)
    data = [uniqname, fullname, first, last, um_id, email]
    write_data(data)
    #send_email(data)

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": fullname.split(" ")[0],
            "LNAME": last.title()
        }
    }
    add_to_list(member_info)

    return 



if __name__ == "__main__":

    response = mailchimp.ping.get()
    print(response)

    while True:
        str_in = input("")
        process_data(str_in)
    