'''
Groups together customers based on luggage, distance, and overall cost

© 2024 Abdul Rehman <abrehman.bscs21seecs@seecs.edu.pk>
'''
from typing import List, Dict, Tuple
from CathayDB.dbHandle import dbHandler
from transport import Taxi
import datetime
import numpy as np

# We assume we have enough taxis available for everyone
# Primary aim is to group together while minimizing travelling time
class Grouping:
    @staticmethod
    def getGrouping(curTime: datetime.datetime, taxiList: List[Taxi]) -> Dict(str, List[str]):
        handle = dbHandler()
        bookings = handle.getBookings(curTime)
    
    @staticmethod
    def groupCustomers(customers: List[Tuple[str, float, float, int, int]], taxiList: List[Taxi]):
        cords = np.array([[x[1], x[2]] for x in customers])
        baggage = np.array([x[3] for x in customers])
        hailers = np.array([x[4] for x in customers])
        dist = np.sqrt(np.square(cords - cords[:, None]))
        indices = np.argmin(dist, axis=1)

        # Goal is to minimize the additional distance while ensuring maximum baggage
        taxiList.sort(key = lambda taxi: taxi.costMultilpier)
        left = len(customers)
        completedUsers = {}
        groups = []
        for taxi in taxiList:
            if len(completedUsers) == len(customers):
                break
            groups.append(findCloseCustomer(baggage, indices, hailers, taxi.maxLuggage, taxi.maxCapacity, completedUsers))
            completedUsers = completedUsers.union(set(groups[-1]))
        
        return groups

    # returned customers are with min dist while having baggage and hailers bounded by c1, c2
    # Use exact constraint for c2 while baggage can vary
    @staticmethod
    def findCloseCustomer(baggage, idx, hailers, baggageConstraint, capacityConstraint, completedUsers):        
        blackList = {index for index in idx[0] if hailers[index] >= capacityConstraint}
        blackList = blackList.union(completedUsers)
        if len(idx) - len(blackList) < capacityConstraint:
            return findCloseCustomer(baggage, idx, hailers, baggageConstraint, capacityConstraint - 1, completedUsers)

        for index in idx:
            index = list(set(index).difference(blackList))
            curBaggage = baggage[index]
            curSum = sum(curBaggage[:capacityConstraint])
            selected = [x for x in range(capacityConstraint)]
            remaining = [x for x in range(capacityConstraint, len(baggage))]
            while curSum > baggageConstraint:
                moveIdx = math.argmax(baggage[selected])
                curSum -= baggage[selected[moveIdx]]
                if len(remaining) == 0:
                    continue
                selected[moveIdx] = remaining.pop(0)
                curSum += baggage[selected[moveIdx]]
            return selected
            
    



        


