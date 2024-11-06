'''
Provides encapsulation over Cathay Datastore

© 2024 Abdul Rehman <abrehman.bscs21seecs@seecs.edu.pk>
'''
import sqlite3
import os
import random
import hashlib
import base64
import datetime


class dbHandler:
    # Create and initialize the database
    def __init__(self, dbPath: str = "cathayDB.db"):
        self.dbPath = dbPath
        open(dbPath, 'a').close()  # Create file
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        # DB Schema
        queries = ["""
                CREATE TABLE IF NOT EXISTS Customers (
                    CustomerID VARCHAR(16) PRIMARY KEY
                );""",
                """
                CREATE TABLE IF NOT EXISTS Flights (
                    FlightID VARCHAR(16) PRIMARY KEY,
                    DepartureDateTime DATETIME NOT NULL,
                    ArrivalDateTime DATETIME NOT NULL,
                    DepartureAirport VARCHAR(100) NOT NULL,
                    ArrivalAirport VARCHAR(100) NOT NULL
                );""",
                """
                CREATE TABLE IF NOT EXISTS Booking (
                    BookingID VARCHAR(16) PRIMARY KEY,
                    CustomerID VARCHAR(16) NOT NULL,
                    FlightID VARCHAR(16) NOT NULL,
                    CordX DOUBLE NOT NULL,
                    CordY DOUBLE NOT NULL,
                    Baggage INT NOT NULL,
                    RideHailers INT NOT NULL,
                    IsFerry BOOLEAN NOT NULL,
                    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
                    FOREIGN KEY (FlightID) REFERENCES Flights(FlightID)
                );
                """
        ]
        for query in queries:
            cur.execute(query)
        conn.commit()
        conn.close()
    
    # Randomly add min(n, 2000) customers
    def addRandomCustomer(self, n: int = 2000) -> None:
        n = min(n, 2000)
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        for _ in range(n):
            customerID = "customer" + str(random.randint(0, 999999999999))
            customerID = base64.urlsafe_b64encode(hashlib.md5(customerID.encode('utf8')).digest())[:16]
            cur.execute(f'INSERT INTO Customers VALUES("{customerID}");')
        
        conn.commit()
        conn.close()
    
    # Randomly add min(n, 200) flights
    def addRandomFlight(self, n: int = 200) -> None:
        n = min(n, 200)
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        
        with open("airports.txt", 'r') as f:
            airports = f.read().strip().split('\n')
            if not airports:
                airports = ["HK-terminal1", "china-terminal1"]

        for _ in range(n):
            flightID = "flight" + str(random.randint(0, 999999999999))
            flightID = base64.urlsafe_b64encode(hashlib.md5(flightID.encode('utf-8')).digest())[:16]
            dest, arrival = random.sample(airports, k=2)
            
            # All flights are assumed to be between Nov 6 and Nov 7 with times in increment of 15 mins
            d1, d2 = random.choices(['07', '08'], k=2)
            h1, h2 = random.choices(["{:02d}".format(x) for x in range(0, 24)], k=2)
            m1, m2 = random.choices(['00', '15', '30', '45'], k=2)

            dt1 = datetime.datetime.fromisoformat(f"2024-11-{d1}T{h1}:{m1}:00")
            dt2 = datetime.datetime.fromisoformat(f"2024-11-{d2}T{h2}:{m2}:00")

            cur.execute(f'INSERT INTO Flights VALUES("{flightID}", "{dt1}", "{dt2}", "{dest}", "{arrival}");')
        
        conn.commit()
        conn.close()

    def dropDB(self) -> None:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        cur.execute(f"DROP TABLE Customers;")
        cur.execute(f"DROP TABLE Flights;")
        cur.execute(f"DROP TABLE Booking;")

        conn.commit()
        conn.close()
    
    def addBooking(customerID: str, flightID: str, baggage: int, rideHail: int, isFerry: bool) -> None:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        bookingID = "flight" + str(random.randint(0, 999999999999))
        bookingID = base64.urlsafe_b64encode(hashlib.md5(bookingID.encode('utf-8')).digest())[:16]

        cur.execute(f'INSERT INTO Booking VALUES("{bookingID}", "{customerID}", "{flightID}", {baggage}, {rideHail}, {isFerry});')


        conn.commit()
        conn.close()
    

if __name__ == '__main__':
    handle = dbHandler()
    handle.addRandomFlight()
    handle.addRandomCustomer()
    handle.dropDB()

