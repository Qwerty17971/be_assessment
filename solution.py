import uuid
import sqlite3
import json

input=json.load(open("db.json")) #fetch our input json payload

id=uuid.uuid4() #generates a universally unique identifier
global netfee
netfee=0

scrub=[] #some variables and a "json to tuple converter"
plc=()
for i in input:
    for x in i.keys():
        plc=plc + (i[x],)
    plc=plc + (str(id),)
    scrub.append(plc)
    plc=()

conn=sqlite3.connect("database.db")
cursor=conn.cursor()
cursor.execute("create table info (service_date datetime not null, submitted_procedure text not null, quadrant text, plan_group_num text not null, subcriber_num integer not null, provider_npi bigint(10) not null, provider_fees integer not null, allowed_fees integer not null, member_coinsurance integer not null, member_copay integer not null, claim_id text not null)") #this line is to generate the database, not for use in the final version
cursor.executemany("insert into info values (?,?,?,?,?,?,?,?,?,?,?)", scrub)

conn.close()

def payments(x):
    print(x)

for i in input:
    for j in i.keys():
        print(j)
        if str(j).lower()=="service date" or "submitted procedure":
            continue
        elif str(j).lower()=="allowed fees":
            netfee-=int(i[j])
        if str(j).lower()=="provider fees" or "member coinsurance" or "member copay":
            netfee+=int(i[j])
    payments(netfee) #perhaps this would be a simple and robust way to pass it along?

