#Author : Shubham Chander
#Student number : 101012052
'''
 Description :
   
    The following code is for the stochastic Oracle code.
    The code's input is the environment (single line), and the current position given by the Robot from the LearningAutomata.py
    The code's output is the direction to be given to the robot to move towards. The direction will be determined randomly based on
    if the oracle is a stochastic teacher or a stochastic liar.

'''

import random


# IN the paper, the location of the unknown point is 0.9123
#locationOfUnknownPoint = 0.9123
locationOfUnknownPoint = 0.45
#The value of p is the probability of the Oracle telling the truth. Likewise 1-p is the probability of the Oracle telling the Lies
p = 0.85

class Oracle(object):

    EnvironmentDim = []
    
    
    def __init__(self,environmentDim):
        
        self.EnvironmentDim = environmentDim
        
        
    def getUnknownPoint(self):
        return locationOfUnknownPoint
        
    def getIntervalRange(self):
        return EnvironmentDim
        
    
    def updateIntervalRange(self,newIntervalRange):
    
        self.EnvironmentDim = newIntervalRange 
    
        
    def recieveLALocationsAndReturnDirection(self,LaLocation):
    
        DirectionToReturn = ""
        coinToss = random.uniform(0,1)
        
        #print("The value of coinToss is ", coinToss, "and the value of p is ",p)
        #print("The location of LA is ",LaLocation,"and the location of unknownPoint", locationOfUnknownPoint)
        
        if(LaLocation - locationOfUnknownPoint) < 0:
            if(coinToss <= p):
                DirectionToReturn = "Right"
            else:
                DirectionToReturn = "Left"
        
        elif(LaLocation - locationOfUnknownPoint) > 0:
            if(coinToss <= p):
                DirectionToReturn = "Left"
            else:
                DirectionToReturn = "Right"
                
        return DirectionToReturn
        
            
        
        
    def get_EnvironDim(self):
        return self.EnvironmentDim