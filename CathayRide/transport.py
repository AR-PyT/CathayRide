'''
Simulates API for Cathay partners e.g. Uber, DiDi, Ferry

© 2024 Abdul Rehman <abrehman.bscs21seecs@seecs.edu.pk>
'''

from typing import Tuple, List, Set
import math
import numpy as np

'''
    Each transport has its own serviceable area
    Area represented in a rectangular map. All points within the rectangle are serviced
    Each transport can give an estimated price for travel given the time and dest/final loc
    To simplify calculations we use euc distance in 2D but ideally this data is based on past records of the transport agency

    Cathay uses the API interface to give estimated price and find routes for customers
'''

class Transport:
    # costMultilpier to indicate differences in taxi/ferry/shuttle
    def __init__(self, costMultiplier: float, speed: float):
        self.costMultiplier = costMultiplier
        self.speed = speed
        self.distance = lambda x, y: np.sqrt(np.square(x[0] - y[0]) + np.square(x[1] - y[1]))


    # Price estimate
    def getPrice(self, ini: (float, float), final: (float, float), startHour: int) -> float:
        estCost = self.distance(ini, final) * self.costMultiplier
        return estCost if 6 < startHour <  23 else estCost * 1.1  # Add night charge
    
    # Travel time estimate
    def getTime(self, ini: (float, float), final: (float, float)) -> float:
        return self.distance(ini, final) / self.speed
    
    
class Taxi(Transport):
    def __init__(self, serviceArea: List[Tuple[float, float, float, float]], maxCapacity: int, maxLuggage: int):
        super().__init__(2.0, 90)
        self.serviceArea = serviceArea
        self.maxCapacity = maxCapacity
        self.maxLuggage = maxLuggage
    
    def isServiced(self, loc: Tuple[float, float]):
        for rect in self.serviceArea:
            if rect[0] <= loc[0] <= rect[0] + rect[2] and rect[1] <= loc[1] <= rect[1] + rect[3]:
                return True
        return False
    
    def getPrice(self, ini: Tuple[float, float], final: Tuple[float, float]):
        if self.isServiced(final):
            return super().getPrice(ini, final)
        return math.inf    

    def getDropPoint(self, ini: Tuple[float, float], dropPoints: List[Tuple[float, float]], estPrices: List[float]) -> List[float]:
        return list(map(lambda x, y: self.getPrice(ini, x) + y, zip(dropPoints, estPrices)))
    
        
class Shuttle(Transport):
    def __init__(self, serviceArea: List[Tuple[float, float, float, float]], maxCapacity: int, maxLuggage: int):
        super().__init__(1.0, 90)
        self.serviceArea = serviceArea
        self.maxCapacity = maxCapacity
        self.maxLuggage = maxLuggage
    
    def isServiced(self, loc: Tuple[float, float]):
        for rect in self.serviceArea:
            if rect[0] <= loc[0] <= rect[0] + rect[2] and rect[1] <= loc[1] <= rect[1] + rect[3]:
                return True
        return False
    
    def getPrice(self, ini: Tuple[float, float], final: Tuple[float, float]):
        if self.isServiced(final):
            return super().getPrice(ini, final)
        return math.inf

    def getDropPoint(self, ini: Tuple[float, float], dropPoints: List[Tuple[float, float]], estPrices: List[float]) -> List[float]:
        return list(map(lambda x, y: self.getPrice(ini, x) + y, zip(dropPoints, estPrices)))
        

class Ferry(Transport):
    def __init__(self, startPoints: List[Tuple[float, float]], dropPoints: List[Tuple[float, float]]):
        super().__init__(0.7, 90)
        self.startPoints = startPoints
        self.dropPoints = dropPoints
