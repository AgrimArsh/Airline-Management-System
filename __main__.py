#ISSUES AND COMMENTS
'''
2. Syntax Error in : ALTER TABLE j122101
                     ALTER COLUMN Seat_no varchar(6) not null;

3. Infinite Loop during booking of seats when no of seats exceeds those available

4. Line 156

5. Line 187

6. Line 268. Both functions (this and line 253 one) contain the same fundamental structure so both are having the same error.

NOTE THAT CUSTID IS STORED IN THE VARIABLE CALLED `session_key`.
'''

#importing the modules
import os
import re
import mysql.connector as m
import datetime

con1=m.connect(host='localhost', user='root', passwd='root', database='amd')
if con1.is_connected():
    print('Successfully connected to database!')
cur1=con1.cursor()

#defining the functions
Lof=[]
cur1.execute('select flightNo from flights')
Rec=cur1.fetchall()
for row in Rec:
    Lof.append(row[0])
print(Lof)

def route_data():
    print ('''

                ROUTES MENU
                -----------
        Choose what you want to do:
            1. View all routes
            2. Add new route
    
    ''')
    rd_choice=int(input('Enter your choice: '))
    if rd_choice==1:
        view_routes()
    elif rd_choice==2:
        add_route()
    return 

def view_routes():
    #not working------- check
    cur1.execute('select * from flights')
    rec=cur1.fetchall()
    print('FL. NO.      ARR       DEP   SEAT. CAP.     PLANE        DATE')
    for row in rec:
        print(row[0], '     ',row[1], '     ',row[2], '     ',row[3], '     ',row[4], '     ',row[5])

def add_route():
    try:
        fn=int(input('Enter Flight No: '))
        poa=input('Enter Place of Arrival: ')
        pod=input('Enter Place of Departure: ')
        sc=int(input('Enter Seating Capacity: '))
        pl=input("Enter Plane's Manufacturer: ")
        dat=input('Enter a date formatted as YYYY-MM-DD: ').split('-')
        y,mo,da=dat
        dt = datetime.date(int(y),int(mo),int(da))
        cur1.execute("insert into Flights values({},'{}','{}',{},'{}','{}')".format(fn,poa,pod,sc,pl,dt))
        con1.commit()
    except m.Error as e:
        print(e)

def flight_data():
    print ('''
    
                FLIGHTS MENU
                -----------
        Choose what you want to do:
            1. View flights
            2. Add new flight
      

    ''')
    rd_choice=int(input('Enter your choice: '))
    if rd_choice==1:
        view_flights()
    elif rd_choice==2:
        add_flight()
    return 

def view_flights():
    fl_no=int(input("Enter the flight No: "))

    tog=0
    boo=False
    for x in range(len(Lof)):
        if str(fl_no) in str(Lof[x]):
            tog+=1
        if tog==True:
            boo=True
        else:
            boo=False
    if boo:
        cur1.execute('select * from {fl_name}'.format(fl_name='j'+str(fl_no)))
        fl_data=cur1.fetchall()
        print('Seat No      Class       Vacancy         Price           Occupant ID')
        for row in fl_data:
            print(row[0], '         ', row[1], '            ', row[2], '            ', row[3], '            ', row[4])
    else:
        print('Flight Not Found')    

def add_flight():
    n=int(input("Enter Flight No.: "))
    tog=0
    for x in range(len(Lof)):
        if str(n) not in str(Lof[x]):
            tog+=1
    if tog==len(Lof):
        boo=True
    else:
        boo=False
    if boo:
        cur1.execute("create table {name} (seat_no numeric(6) primary key, class varchar(1) not null, vacancy varchar(1) not null, price numeric(5) not null, occupant_id numeric(6) );".format(name='J'+str(n)))
        con1.commit()
        nm=int(input("Enter No.of Seats: "))
        ep=int(input('Enter Economy Class Price'))
        bp=int(input('Enter Business Class Price'))
        fp=int(input('Enter First Class Price'))
        d={'E':ep,'B':bp,'F':fp}
        l=[]
        while nm>0:
            sn=int(input('Seat no.: '))
            if sn not in l:
                cs=input('Enter E/B/F: ')
                cur1.execute("insert into {} values({},'{}','N',{},null)".format('J'+str(n),sn,cs,d[cs]))
                con1.commit()
                nm-=1
            else:
                print('Seat Already There')
    else:
        print('Flight Already There')
    return

def customer_data():
    flight_no=input("Enter flight no. for which customer data is to be viewed: ")
    cur1.execute('select occupant_id from {}'.format('J'+flight_no))
    occ=[]
    print('|    ', end='')
    for x in cur1.fetchall():
        occ.append(x[0])
        print (x[0], end='  |   ')

#Leaving just this one functionality to you buddy, finish this up on 3rd October 😉.
def history():
    return 

def book():
    global arr
    arr=arrival()
    global dep
    dep=departure()
    global booked_seats
    booked_seats=seats()
    bills=bill()
    print (' ') 
    ## Take DEP place and DATE from the `flights` table (executed above) and add it down to the ticket.
    print('''
          
                ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ 
                  ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶
        CUSTID: '''+int(session_key)+'''
        FLIGHTN: '''+str(dep)+  '''
          
        DEP:               ARR: '''+str(arr)+ '''
        DATE:
        
        BILL PAYED: '''+str(bills)+'''

                ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ 
              ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶ ◀▶
          
''')

#Some Syntax Error is coming in this function. Ask Ma'am regarding the same.
def indat():
    for x in booked_seats:
        cur1.execute('update {name} set vacancy="N",occupant_id={occ_id} where Seat_NO= {stn}'.format(name=('J'+str(dep)), occ_id=int(session_key), stn=x))
        con1.commit()

def arrival():
    try:
        cur1.execute('select distinct(Place_of_Arrival) from Flights')
        #make table schedule_flights with coln arrival
        rec=cur1.fetchall()
        d=[]
        print ('''
        
                FLIGHTS AVAILABLE TO
                --------------------

        ''')
        for x in rec:
            print('                       ', x[0])
            d.append(x[0].upper())
        print('')

        arr=input('Enter your arrival location: ')
        while arr.upper() not in d:
            arr=input("Sorry, no flights to this location yet. Please enter another location: ")
        return arr.upper()

    except m.Error as e:
        print(e)

def departure():
    try:
        cur1.execute(('select flightNo,Place_of_Departure,ddate from Flights where Place_of_Arrival= "{}"').format(arr))
        rec=cur1.fetchall()
        d=[]
        for x in rec:
            print('Flight No',x[0] ,'\tPlace of Departure : ',x[1],'\tDate : ',x[2])
            d.append(x[0])
        dep=int(input("Enter Your Desired Flight's No: "))
        while dep not in d:
            dep=int(input("Invalid Flight No. Please choose one from the list above. "))
        return dep
    except m.Error as e:
        print(e)

def seats():
    try:
        cur1.execute('select Seat_NO,class from {} where Vacancy="Y"'.format('j'+str(dep)))
        rec=cur1.fetchall()
        print('Available Seats: ')
        l1=[]
        for x in rec:
            print(x[0],'\t',x[1])
            l1.append(int(x[0]))
        ns=int(input('No. of Seats You Would Like to Book: '))
        global l2
        l2=[]
        while ns>0:
            a=int(input('Enter Seat No.: '))
            if a in l1:
                l2.append(int(a))
                ns-=1
            else:
                print('Enter Valid Seat No.')
        return l2
    except m.Error as e:
        print(e)

def bill():
    try:
        cost=0
        for x in l2:
            cur1.execute(('select price from {} where Seat_NO="{}"').format(dep, x))
            rec=(cur1.fetchone())[0]
            cost+=int(rec)
        print('Your Total Cost = ',cost)
        return cost
    except m.Error as e:
        print(e)

#Same Syntax Error is coming in this function. Ask Ma'am regarding the same.
#Also, add cancellation charges based on some parameter. It is static at 2000. If not fine, then pls do the needful.
def cancel():
    fl_cancel=input("Enter flight no. to be cancelled: ")
    cur1.execute('select occupant_id from {}'.format('J'+fl_cancel))
    occ=[]
    for x in cur1.fetchall():
        occ.append(x[0])
    tgl=False
    for x in occ:
        if session_key==x:
            tgl=True
            cur1.execute('update {name} set vacancy="Y",occupant_id=NULL where occupant_id= {occ_id}'.format(name=('J'+str(dep)), occ_id=int(session_key) ))
            print('Cancellation Charges: 2000')
        else: 
            continue
    if tgl==False:
        print('You have not booked this flight.')

#defining menu messages
user_choice_menu='''
------------------------------------------------------------------------------------------------

                    ▯▯    ▯▯    ▯▯    ▯▯    ▯▯    ▯▯    ▯▯
                        ▯▯    ▯▯    ▯▯    ▯▯    ▯▯    ▯▯   

                    WELCOME TO LTC AIRLINE CONTROLLER MANAGEMENT SYSTEM         
                
                LOGIN AS:  1. Admin
                           2. Customer
                           3. Quit
                    
'''

admin_menu='''
                    ADMIN MENU

                Choose what you want to do:

                1. Route Data
                2. Flight Data
                3. Customer Data
                4. Go Back

'''

customer_menu='''
                    CUSTOMER MENU

                Choose what you want to do:

                1. Flight History
                2. Book a New Flight
                3. Cancel a Flight
                4. Go Back
'''

# __main__
while True:
    print(user_choice_menu)
    user_choice=input('Choose the respective numeric choice: ')


    if user_choice=='1':
        print('''ENTER THE CREDENTIALS
                ----------------------
              ''')
        username=input('Username: ')
        password=input('Password: ')
        if (username=='admin') and (password=='admin'):
            print(admin_menu)
            admin_choice=input('Choose the respective numeric choice: ')

            if admin_choice=='1':
                route_data()

            elif admin_choice=='2':
                flight_data()

            elif admin_choice=='3':
                customer_data()
            
            elif admin_choice=='4':
                continue
        else:
            print("Unauthorized access")


    elif user_choice=='2':
        print('''
              
ENTER THE CREDENTIALS
----------------------
              ''')
        

        cur1.execute('SELECT * FROM allcusts')
        all_users_data=[]
        for x in cur1.fetchall():
            all_users_data.append({'session_key':str(x[0]), 'passkey':x[1]})
        
        
        session_key=input('Username: ')
        password=input('Password: ')
        toggle=False
        for x in all_users_data:
            if (session_key==x['session_key']) and (password==x['passkey']):
                toggle=True
                print(customer_menu)
                customer_choice=input('Hello Customer! Choose the respective numeric choice: ')

                if customer_choice=='1':
                    history()

                elif customer_choice=='2':
                    book()

                elif customer_choice=='3':
                    cancel()

                elif customer_choice=='4':
                    continue
            else:
                continue
        if toggle==False:
            print('Unauthorized Access')




    elif user_choice=='3':
        break

    else:
        print('Enter a valid choice.')