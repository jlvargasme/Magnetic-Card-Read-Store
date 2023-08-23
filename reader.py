# Logic to read input from magnetic card reader and upload user
# to database

import json
import requests

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

def add_to_list():

    
    return


def process_data(str_in):
    [um_id, first, last, uniqname] = process_string(str_in)
    [fullname, email] = get_full_name(uniqname)
    data = [uniqname, fullname, first, last, um_id, email]
    write_data(data)

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

    while True:
        str_in = input("")
        process_data(str_in)
    