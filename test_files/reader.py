# Logic to read input from magnetic card reader and write to csv
import os

filename = "students.csv"

def process_string(str_in):
    inputs = str_in.split("^")
    um_id = inputs[0][8:16]
    
    name = inputs[1]
    last, first = name.split("/")

    uniqname = inputs[2].split("?")[0]
    uniqname = ''.join([i for i in uniqname if not i.isdigit()]).lower()

    return [um_id, first, last, uniqname]

def write_data(data):
    file = open(filename, "a")

    for i in range(0, len(data)-1):
        file.write(data[i]+", ")
    file.write(data[-1]+"\n")

    file.close()
    return

def process_data(str_in):
    [um_id, first, last, uniqname] = process_string(str_in)
    email = uniqname + "@umich.edu"
    data = [uniqname, first, last, um_id, email]
    write_data(data)

    return 

if __name__ == "__main__":

    file = open(filename, "a+") 

    if (os.stat("./students.csv").st_size == 0):
        # Add header column for new file
        file.close() # close file, will be opened in write_data
        write_data(["uniqname", "first", "last", "UMID", "email"])

    while True:
        str_in = input("")
        process_data(str_in)
    