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
from typing import List, Tuple, Dict, Any
from collections import defaultdict

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
    
    def addBooking(self, customerID: str, flightID: str, cordX: float, cordY:float, baggage: int, rideHail: int, isFerry: bool) -> None:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        bookingID = "flight" + str(random.randint(0, 999999999999))
        bookingID = base64.urlsafe_b64encode(hashlib.md5(bookingID.encode('utf-8')).digest())[:16]

        cur.execute(f'INSERT INTO Booking VALUES("{bookingID}", "{customerID}", "{flightID}", {cordX}, {cordY}, {baggage}, {rideHail}, {isFerry});')

        conn.commit()
        conn.close()
    
    def addCustomer(self, customerID: str) -> None:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        cur.execute(f'INSERT INTO Customers VALUES("{customerID}");')

        conn.commit()
        conn.close()
    
    def addFlight(self, flightID: str, dt1: datetime, dt2: datetime, departure: str, arrival: str) -> None:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        cur.execute(f'INSERT INTO Flights VALUES("{flightID}", "{dt1}", "{dt2}", "{departure}", "{arrival}");')

        conn.commit()
        conn.close()
    
    def getBookings(self, curTime: datetime) -> Dict[str, List]:
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()

        query = f"""
            SELECT
                Flights.ArrivalAirport,
                Booking.CustomerID,
                Booking.CordX,
                Booking.CordY,
                Booking.Baggage,
                Booking.RideHailers,
                Booking.IsFerry
            FROM Booking
            INNER JOIN Flights ON Booking.FlightID = Flights.FlightID
            WHERE Flights.ArrivalDateTime >= '{curTime.strftime('%Y-%m-%d %H:%M:%S')}' AND Flights.ArrivalDateTime <= '{(curTime + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')}'
        """

        cur.execute(query)
        res = cur.fetchall()
        conn.commit()
        conn.close()

        result = defaultdict(list)
        for row in res:
            result[row[0]].append(row[1:])
        return result
    

if __name__ == '__main__':
    handle = dbHandler()
    # handle.addRandomFlight()
    # handle.addRandomCustomer()

    try:
        handle.addCustomer("123456")
        handle.addCustomer("123457")
        handle.addCustomer("123458")
        handle.addCustomer("123482")
        handle.addCustomer("123158")

        handle.addFlight("1", datetime.datetime.fromisoformat("2024-11-07T13:00:00"), datetime.datetime.fromisoformat("2024-11-07T15:00:00"), "A", "D")
        handle.addFlight("2", datetime.datetime.fromisoformat("2024-11-07T14:00:00"), datetime.datetime.fromisoformat("2024-11-07T15:15:00"), "B", "E")
        handle.addFlight("3", datetime.datetime.fromisoformat("2024-11-07T10:00:00"), datetime.datetime.fromisoformat("2024-11-07T15:30:00"), "C", "F")


        handle.addBooking("123456", "1", 1.1, 1.2, 20, 2, True)
        handle.addBooking("123457", "1", 100, 200, 20, 2, True)
        handle.addBooking("123482", "2", 300, 203, 20, 2, True)
        handle.addBooking("123458", "2", 2, 20, 20, 2, True)
        handle.addBooking("123158", "3", 123, 200, 20, 2, True)

        print(handle.getBookings(datetime.datetime.fromisoformat("2024-11-07T15:15:00")))
    except Exception as e:
        print(e)
    finally:
        handle.dropDB()

