'''
Provides encapsulation over Cathay and associated flights

© 2024 Abdul Rehman <abrehman.bscs21seecs@seecs.edu.pk>
'''
from typing import List, Dict
import hashlib
from customers import Customer
from dbHandle import dbHandler


class Flights:
    def __init__(self, flightID: str):
        self.flightID = flightID

    '''
    This function provides an abstraction over the actual booking into Cathay database
    Only limited to booking a specific fight and tracking transit preferences

    TODO: Add seat preferences
    '''
    def book_flight(customer: Customer, dest: (float, float), baggage: int, rideHail: int, isFerry:bool) -> str:
        handler = dbHandler()
        handler.addBooking(customer.customerID, self.flightID, dest[0], dest[1], baggage, rideHail, isFerry)

