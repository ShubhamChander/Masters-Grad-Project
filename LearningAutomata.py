#Author : Shubham Chander
#Student number : 101012052
'''
 Description :
   
    The following code is for the learning automata/Robot code.
    The code's input is the environment (single line), and the direction given by the oracle from the oracle.py
    The code's output is the direction chosen by the robot to move towards.

'''

# OutputsForLA_One OutputsForLA_Two OutputsForLA_Three New Sub-interval to search

DecisionTable = [["Left", "Left", "Left", "One"],
    ["Inside", "Left", "Left", "One" ],
    ["Right", "Left", "Left", "One and Two"],
    ["Right", "Inside", "Left", "Two"],
    ["Right", "Right", "Left", "Two and Three"],
    ["Right", "Right", "Inside", "Three"],
    ["Right", "Right", "Right", "Three"]]
    

class LearningAutomata(object):
    
    '''
        This defines an interface for a Learning Automata. 
    '''
    
    def __init__(self,ID,interval_range,lri_Array):
        
        self.LA_ID = ID
        self.currPosition = (interval_range[0] + interval_range[1])/2
        self.IntervalRange = interval_range
        self.LRI_Array = lri_Array
        self.OracleTrustworthyBoolean = True
    
    
    def get_LA_ID(self):
        return self.LA_ID
        
    def get_CurrPos(self):
        return self.currPosition
        
    def get_IntervalRange(self):
        return self.IntervalRange
        
    
    def Reset_IntervalRangeSettings(self,intervalRange,newLRI_Array):
        self.IntervalRange = intervalRange
        self.currPosition = (intervalRange[0] + intervalRange[1])/2
        self.LRI_Array = newLRI_Array
        
        
    # LRI_Array = [left, right] ----> Absolute left will be [1,0], Absolute Right will be [0,1]
    def get_lriArray(self):
        return self.LRI_Array
        
        
    def update_pos(self,x):
        self.currPosition = x
    
    def update_lriArray(self,newLRI):
        self.LRI_Array = [newLRI[0],newLRI[1]]
        
    
        
    