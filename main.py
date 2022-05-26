#Author : Shubham Chander
#Student number : 101012052
'''
 Description :
   
    The following code is for the environment code. The environment is a single line from 0 to 1
    The code's input is the environment (single line), and the current position given by the Robot from the LearningAutomata.py
    The code's output is the direction to be given to the robot to move towards. The direction will be determined randomly based on
    if the oracle is a stochastic teacher or a stochastic liar.
   
    The following is also the main code from where the simulation and tests will run.
'''

from decimal import *   

from StochasticOracle import Oracle
from LearningAutomata import LearningAutomata


'''

The environment is represented as follows:

    
            
        |--I--|--I--|--I--|
        0   (1/3) (2/3)   1


    - The interval of the environment is 0 to 1.
    - The three sub-intervals that the three robots will operate and start on will be (1/4), (2/4), (3/4). They are represented by I


'''

# OutputsForLA_One OutputsForLA_Two OutputsForLA_Three New Sub-interval to search
DecisionTable = [["Left", "Left", "Left", "One"],
    ["Inside", "Left", "Left", "One" ],
    ["Right", "Left", "Left", "One and Two"],
    ["Right", "Inside", "Left", "Two"],
    ["Right", "Right", "Left", "Two and Three"],
    ["Right", "Right", "Inside", "Three"],
    ["Right", "Right", "Right", "Three"]]
    


def getStartingPosNewInterval(subInterval):
    '''
    For starting positions within the new subintervals, formula is:

    ((y-x) * (1/2)) + x
    '''
    
    x = subInterval[0]
    y = subInterval[1]
    
    startingPos = ((y-x) * (1/2)) + x
    
    return startingPos


def newSubIntervalRangesForLAs(SubIntervalRange): # if due to the decision table elimination, a new sub interval is chosen, then the sub interval will be 
# divided into three parts for each of the three robots. 
    '''
    To continuously subdivide the interval into three parts, for any interval range
    [x,y]
    
    ((y-x) * (1/3)) + x AND 
    ((y-x) * (2/3)) + x 
    ''' 
    x = SubIntervalRange[0]
    y = SubIntervalRange[1]
    
    subinterval_One = ((y-x) * (1/3)) + x
    subinterval_Two = ((y-x) * (2/3)) + x
    
    print([[x,subinterval_One],[subinterval_One,subinterval_Two],[subinterval_Two,y]])
    
    #print("Starting Position for LA One in new sub interval will be ", getStartingPosNewInterval([x,subinterval_One]))
    #print("Starting Position for LA Two in new sub interval will be ", getStartingPosNewInterval([subinterval_One,subinterval_Two]))
    #print("Starting Position for LA Three in new sub interval will be ", getStartingPosNewInterval([subinterval_Two, y]))
    return [[x,subinterval_One],[subinterval_One,subinterval_Two],[subinterval_Two,y]]
    
    

#check all three lri arrays against the decision tables to see if oracle is a liar or not. 
def checkOracleHonesty(LRI_Array,Oracle):
    UnknownPoint = Oracle.getUnknownPoint()
    decisionFound = False
    #print("LRI ARRAY --> [LEFT,RIGHT]")
    # LRI_ARRAY ---> [0,1] for right, [1,0] for left
    #print("THE INTERVAL RANGE IS [-1,0], [0,1] , [1,2]")
    
    decision = []
    precisionValue = 0.04
    
    print(LRI_Array)
    
    for alpha in LRI_Array:
        left = alpha[0]
        right = alpha[1]
        
        #Maybe only try one value either check for 0 or 1 because they are already connected. If one is affected
        #The other is also automatically affected
        
        print("The value of left is ======> ", left )
        #print("The absolute value of left - 0.000000 is =====> ", (abs(left - 0.0000)))
        
        #Maybe instead of LRI_ARRAY, try checking the difference of the position of the LA
        if((abs(left - 0.00) <= precisionValue) and (abs(right - 1.00) <= precisionValue)):
            decision.append("Right")
            
        elif((abs(left - 1.00) <= precisionValue) and (abs(right - 0.00) <= precisionValue)):
                decision.append("Left")        
        else:
            decision.append("Inside")
            
    #print("The decision of all the LAs outside of the loop is ", decision)
    
    for decisionList in DecisionTable:
        #if all(dec in decisionList for dec in decision):
        if(decision[0] == decisionList[0] and decision[1] == decisionList[1] and decision[2] == decisionList[2]):
            #print("This decision exists in the Decision Table")
            #print("The sub-interval chosen for further search is ", decisionList[3])
            decisionFound = True
            break
        #else:
            #print("no")
    
    if(decisionFound):
        print("The oracle is honest")
    else:
        print("The oracle is dishonest")
        
    return decisionFound
    
    

#if((LRI_ARRAY_One == [0,1]) or (LRI_ARRAY_One == [1,0])):
#check for LRI Array bring either completely left or right
def checkForLRIArrayLeftOrRight(LeftAlphaVal, RightAlphaVal):
    precValue = 0.01
    if(((abs(LeftAlphaVal - 0.00) <= precValue) and ((abs(RightAlphaVal - 1.00)) <= precValue)) or ((abs(LeftAlphaVal - 1.00) <= precValue) and ((abs(RightAlphaVal - 0.00)) <= precValue))):
        return True
    return False
   

def moveLA_checkingHonesty(LA_Robot,directionFromOracle,N):

    LRI_ARRAY = LA_Robot.get_lriArray()
    
    if(directionFromOracle == "Left"):
        currPos = LA_Robot.get_CurrPos()
        newPos = currPos - (1/N)
        LA_Robot.update_pos(newPos)
        
        newLRI_array_one = [LRI_ARRAY[0] + (1/N),LRI_ARRAY[1] - (1/N)]
        LA_Robot.update_lriArray(newLRI_array_one)
    
    if(directionFromOracle == "Right"):
        currPos = LA_Robot.get_CurrPos()
        newPos = currPos + (1/N)
        LA_Robot.update_pos(newPos)
        
        newLRI_array_one = [LRI_ARRAY[0] - (1/N),LRI_ARRAY[1] + (1/N)]
        LA_Robot.update_lriArray(newLRI_array_one)


def main():
    
    StartingIntervalRange = [-1,2]
    ContinueIntervalRange = [0,1]
    StochasticOracle = Oracle(StartingIntervalRange)
    N = 950
    Min_PrecValue = 0.005
    NumParallelTests = 5
    NumParallelTestsList = []
    NumParallelTestsList2 = []
   
    #LA_One = LearningAutomata(1,(1/4),0,(1/3))
    #LA_Two = LearningAutomata(2,(2/4),(1/3),(2/3))
    #LA_Three = LearningAutomata(3,(3/4),(2/3),1)


    #Step 0 : This step is to figure out if the teacher that the learning automata communicates with is a liar or not.
    for a in range(NumParallelTests):
        LA_One = LearningAutomata(1,[-1,0],[0.5,0.5])
        LA_Two = LearningAutomata(2,[0,1],[0.5,0.5])
        LA_Three = LearningAutomata(3,[1,2],[0.5,0.5])

    
        for i in range(N):
            #print("THIS IS ITERATION NUMBER ",i)
            # Give oracle current location and recieve direction.
            #print("LA_One locations is", LA_One.get_CurrPos())
            directionFromOracle = StochasticOracle.recieveLALocationsAndReturnDirection(LA_One.get_CurrPos())
            directionFromOracleTwo = StochasticOracle.recieveLALocationsAndReturnDirection(LA_Two.get_CurrPos())
            directionFromOracleThree = StochasticOracle.recieveLALocationsAndReturnDirection(LA_Three.get_CurrPos())
            
            #if(LA_One.get_lriArray() is either [0,1] or [1,0]):
                # break out of the loop and declare weather oracle is a liar or not
            #else:
                #move in the direction given by oracle 1/N steps and update location of LA_One in position (pos +- (1/250)) and lriArray by [(0.5 +- (1/250)),(0.5 +- (1/250))] 


            #LRI_ARRAY ------> [left,right]
            LRI_ARRAY_One = LA_One.get_lriArray()
            LeftAlpha = LRI_ARRAY_One[0]
            RightAlpha = LRI_ARRAY_One[1]
            
            LRI_ARRAY_Two = LA_Two.get_lriArray()
            LeftAlphaTwo = LRI_ARRAY_Two[0]
            RightAlphaTwo = LRI_ARRAY_Two[1]
            
            LRI_ARRAY_Three = LA_Three.get_lriArray()
            LeftAlphaThree = LRI_ARRAY_Three[0]
            RightAlphaThree = LRI_ARRAY_Three[1]
            
            #if((LRI_ARRAY_One == [0,1]) or (LRI_ARRAY_One == [1,0])):
            #check for LRI Array bring either completely left or right
            #checkForLRIArrayLeftOrRight(LeftAlphaVal, RightAlphaVal) --> returns true or false
            #if(((abs(LeftAlpha - 0) <= 0.01) and ((abs(RightAlpha - 1)) <= 0.01)) or ((abs(LeftAlpha - 1) <= 0.01) and ((abs(RightAlpha - 0)) <= 0.01))):
            
            # CHECK FOR LEARNING AUTOMATA ONE 
            
            if(checkForLRIArrayLeftOrRight(LeftAlpha,RightAlpha) == True):
                break 
            else:
                #updating position in the direction given by oracle by 1/N
                #updating LRI_Array in the direction given by oracle
                moveLA_checkingHonesty(LA_One,directionFromOracle,N)
                    
            # CHECK FOR LEARNING AUTOMATA TWO
            
            if(checkForLRIArrayLeftOrRight(LeftAlphaTwo,RightAlphaTwo) == True):

                break 
            else:
                #updating position in the direction given by oracle by 1/N
                #updating LRI_Array in the direction given by oracle
                moveLA_checkingHonesty(LA_Two,directionFromOracleTwo,N)
                    
            # CHECK FOR LEARNING AUTOMATA Three
            
            if(checkForLRIArrayLeftOrRight(LeftAlphaThree,RightAlphaThree) == True):

                break 
            else:
                #updating position in the direction given by oracle by 1/N
                #updating LRI_Array in the direction given by oracle
                moveLA_checkingHonesty(LA_Three,directionFromOracleThree,N)
            
        #check all three lri arrays against the decision tables to see if oracle is a liar or not. 
        OracleHonesty =  checkOracleHonesty([LRI_ARRAY_One, LRI_ARRAY_Two, LRI_ARRAY_Three],StochasticOracle)
        NumParallelTestsList.append(OracleHonesty)
        
    #print(NumParallelTestsList)
        
    
    
    #Step 1: Repeat Step 0, however this time with IntervalRange [0,1], and with OracleHonesty variable 
    print("Step 1: Repeat Step 0, however this time with IntervalRange [0,1], and with OracleHonesty variable") 
    
    LA_One.Reset_IntervalRangeSettings([0,(1/3)],[0.5,0.5])
    LA_Two.Reset_IntervalRangeSettings([(1/3),(2/3)],[0.5,0.5])
    LA_Three.Reset_IntervalRangeSettings([(2/3),1],[0.5,0.5])
    StochasticOracle.updateIntervalRange(ContinueIntervalRange)
    
    #LRI_ARRAY_One = LA_One.get_lriArray() 
    #LRI_ARRAY_Two = LA_Two.get_lriArray() 
    #LRI_ARRAY_Three = LA_Three.get_lriArray() 
    counterForStepOne = 1
    while True:
        print("\n")
        print("\n")
        print("THIS IS STEP NUMBER +++++++++++++++++++================= > : ", counterForStepOne)
        #if interval range is <= 0.01, break out of the loop and present the interval range that was chosen for the next loop. The unknown point lies
        #in the mid point between those two interval range. 
        #newSubIntervalRangesForLAs([(1/3),(2/3)])
        LRI_ARRAY_One = LA_One.get_lriArray() 
        LRI_ARRAY_Two = LA_Two.get_lriArray() 
        LRI_ARRAY_Three = LA_Three.get_lriArray() 
        
        # In the paper, after the last step, there is another movement by the LA, it doesnt just stop. Check step 10 in paper
        if(abs(ContinueIntervalRange[1] - ContinueIntervalRange[0]) <= Min_PrecValue):
        
            LA_ONE_Pos_temp = LA_One.get_CurrPos()
            LA_TWO_Pos_temp = LA_Two.get_CurrPos()
            LA_THREE_Pos_temp = LA_Three.get_CurrPos()
            NumParallelTestsList2.clear()
            
            print("\n")
            print("\n")
            print("The current position of LA_ONE IN THE TEMP ONE is ", LA_ONE_Pos_temp)
            print("\n")
            
            
            for c in range(NumParallelTests):
                for i in range(N):
                    directionFromOracle = StochasticOracle.recieveLALocationsAndReturnDirection(LA_ONE_Pos_temp)
                    directionFromOracleTwo = StochasticOracle.recieveLALocationsAndReturnDirection(LA_TWO_Pos_temp)
                    directionFromOracleThree = StochasticOracle.recieveLALocationsAndReturnDirection(LA_THREE_Pos_temp)
                    
                    
                    if(checkForLRIArrayLeftOrRight(LA_One.get_lriArray()[0],LA_One.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_One,OracleHonesty,directionFromOracle,N)
                    
                    if(checkForLRIArrayLeftOrRight(LA_Two.get_lriArray()[0],LA_Two.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_Two,OracleHonesty,directionFromOracleTwo,N)
                        
                    if(checkForLRIArrayLeftOrRight(LA_Three.get_lriArray()[0],LA_Three.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_Three,OracleHonesty,directionFromOracleThree,N)
                
                NumParallelTestsList2.append(LA_One.get_lriArray())
                    
            print(NumParallelTestsList2)
            print("The length of the NumParallelTestsList2 IN TEMP ONE is ===> ", len(NumParallelTestsList2) )
            
            LAONE_MajorityWinList = determineMajorityWin(NumParallelTestsList2)
            
            NumParallelTestsList2.clear()
            
            if(LAONE_MajorityWinList == True):
                #print("THE INTERVAL RANGE THAT LRI ONE IS WORKING ON IS ", LA_One.get_IntervalRange())
                ContinueIntervalRange = pruneDecisionTableAndchooseNewInterval(LA_One,LA_Two,LA_Three,ContinueIntervalRange)
                #print("The NEW CONTINUEINTERVAL RANGE IS ", ContinueIntervalRange)
                #print("\n")
                print("\n")
                print("The loop will end here...")
                #print("The interval difference is found to be below 0.01")
                #print("The unknown point is at the mid-point of the interval")
                print("The interval range is ",ContinueIntervalRange)
                print("THE DIFFERNCE OF THE CONTINUE INTERVAL RANGE IS ", ContinueIntervalRange[1] - ContinueIntervalRange[0])
                print("\n")
                break
        else:
          
            LA_ONE_Pos = LA_One.get_CurrPos()
            LA_TWO_Pos = LA_Two.get_CurrPos()
            LA_THREE_Pos = LA_Three.get_CurrPos()
            
            print("\n")
            print("\n")
            print("The current position of LA_ONE is ", LA_ONE_Pos)
            print("\n")
            
            for b in range(NumParallelTests):
                for i in range(N):
                    directionFromOracle = StochasticOracle.recieveLALocationsAndReturnDirection(LA_ONE_Pos)
                    directionFromOracleTwo = StochasticOracle.recieveLALocationsAndReturnDirection(LA_TWO_Pos)
                    directionFromOracleThree = StochasticOracle.recieveLALocationsAndReturnDirection(LA_THREE_Pos)
                    
                    
                    if(checkForLRIArrayLeftOrRight(LA_One.get_lriArray()[0],LA_One.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_One,OracleHonesty,directionFromOracle,N)
                    
                    if(checkForLRIArrayLeftOrRight(LA_Two.get_lriArray()[0],LA_Two.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_Two,OracleHonesty,directionFromOracleTwo,N)
                        
                    if(checkForLRIArrayLeftOrRight(LA_Three.get_lriArray()[0],LA_Three.get_lriArray()[1]) == True):
                        break 
                    else:
                        moveLA(LA_Three,OracleHonesty,directionFromOracleThree,N)
                        
                    
                NumParallelTestsList2.append(LA_One.get_lriArray())
                
            print(NumParallelTestsList2)
            print("The length of the NumParallelTestsList2 is ===> ", len(NumParallelTestsList2) )
            
            
            LAONE_MajorityWinList = determineMajorityWin(NumParallelTestsList2)
            
            NumParallelTestsList2.clear()
            
            if(LAONE_MajorityWinList == True):
                #print("THE INTERVAL RANGE THAT LRI ONE IS WORKING ON IS ", LA_One.get_IntervalRange())
                ContinueIntervalRange = pruneDecisionTableAndchooseNewInterval(LA_One,LA_Two,LA_Three,ContinueIntervalRange)
                print("The NEW CONTINUEINTERVAL RANGE IS ", ContinueIntervalRange)
                newIntervalRanges = newSubIntervalRangesForLAs(ContinueIntervalRange)
                print("THE NEW SUB INTERVALS FOR EACH LA IS ", newIntervalRanges)
                LA_One.Reset_IntervalRangeSettings(newIntervalRanges[0],[0.5,0.5])
                LA_Two.Reset_IntervalRangeSettings(newIntervalRanges[1],[0.5,0.5])
                LA_Three.Reset_IntervalRangeSettings(newIntervalRanges[2],[0.5,0.5])
                counterForStepOne+=1
    
 
def determineMajorityWin(Listtocheck):
    
    print("THIS LIST TO CHECK IS --------------------------->>>>>", Listtocheck)
    print(Listtocheck[0][1])
    print(Listtocheck[1][1])
    print(Listtocheck[2][1])
    print(Listtocheck[3][1])
    print(Listtocheck[4][1])
    
    if((Listtocheck[0][1] - Listtocheck[2][1] <= 0.01) and (Listtocheck[0][1] - Listtocheck[3][1] <= 0.01) and(Listtocheck[0][1] - Listtocheck[4][1] <= 0.01)):
        print("THIS IS A VERYYYY GOOOD SUCCESSSS")
        return True
    else:
        return False
    
    

def pruneDecisionTableAndchooseNewInterval(LA_One,LA_Two,LA_Three,IntervalRange):
    
    
    decision = []
    precisionValue = 0.5
    LRI_ARRAY = [LA_One.get_lriArray(),LA_Two.get_lriArray(),LA_Three.get_lriArray()]
    #print("THE LRI ARRAY THAT WE ARE WORKING IS ", LRI_ARRAY)
    #print("THE INTERVAL RANGE THAT LRI ONE IS WORKING ON IS ", LA_One.get_IntervalRange())
    
    for alpha in LRI_ARRAY:
        left = alpha[0]
        right = alpha[1]
        
        if((abs(left - 0) <= precisionValue) and (abs(right - 1) <= precisionValue)):
            decision.append("Right")
            
        elif((abs(left - 1) <= precisionValue) and (abs(right - 0) <= precisionValue)):
                decision.append("Left")        
        else:
            decision.append("Inside")
            
    print("The decision of all the LAs INSIDE THE VALID BOUNDS OF [0,1] of the loop is ", decision)
    
    for decisionList in DecisionTable:
        #if all(dec in decisionList for dec in decision):
        if(decision[0] == decisionList[0] and decision[1] == decisionList[1] and decision[2] == decisionList[2]):
            print("This decision exists in the Decision Table")
            print("The sub-interval chosen for further search is ", decisionList[3])
            decisionFound = True
            break
           
    newSubInterval = []   
    
    if(decision[0] == "Right"):
        if(decision[1] == "Right"):
            if(decision[2] == "Right"):
                print("New subinterval is one with LA_THREE")		
                newSubInterval = LA_Three.get_IntervalRange()

            elif(decision[2] == "Inside"):
                print("New subinterval is one with LA_THREE")
                newSubInterval = LA_Three.get_IntervalRange()

            elif(decision[2] == "Left"):
                print("New subinterval is one with LA_TWO and LA_THREE")
                newSubInterval = [LA_Two.get_IntervalRange()[0], LA_Three.get_IntervalRange()[1]]
                

        elif(decision[1] == "Left"):
            if(decision[2] == "Right"):
                print("This should not be possible")
            elif(decision[2] == "Inside"):
                print("This should not be possible")
            elif(decision[2] == "Left"):
                print("New subinterval is one with LA_ONE and LA_TWO")
                newSubInterval = [LA_One.get_IntervalRange()[0],LA_Two.get_IntervalRange()[1]]

        elif(decision[1] == "Inside"):
            if(decision[2] == "Right"):
                print("This should not be possible")
            elif(decision[2] == "Inside"):
                print("This should not be possible")
            elif(decision[2] == "Left"):
                print("New subinterval is one with LA_TWO")
                newSubInterval = LA_Two.get_IntervalRange()

    elif(decision[0] == "Left"):
        if(decision[1] == "Right"):
            if(decision[2] == "Right"):
                print("This should not be possible")
            elif(decision[2] == "Inside"):
                print("This should not be possible")
            elif(decision[2] == "Left"):
                print("This should not be possible")
                
        elif(decision[1] == "Left"):
            if(decision[2] == "Right"):
                print("This should not be possible")
            elif(decision[2] == "Inside"):
                print("This should not be possible")
            elif(decision[2] == "Left"):
                print("New subinterval is one with LA_One")
                newSubInterval = LA_One.get_IntervalRange()

        elif(decision[1] == "Inside"):
            if(decision[2] == "Right"):
                print("This should not be possible")
            elif(decision[2] == "Inside"):
                print("This should not be possible")
            elif(decision[2] == "Left"):
                print("This should not be possible")
    elif(decision[0] == "Inside"):
        if(decision[1] == "Left"):
            if(decision[2] == "Left"):
                print("New subinterval is one with LA_One")
                newSubInterval = LA_One.get_IntervalRange()
    
    
    print("New sub interval chosen is : ++++++++++++++++++++++++++>", newSubInterval)
    return newSubInterval
    #return newSubIntervalRangesForLAs([x,y])
    
    
    
  
    
def moveLA(LA_Robot,OracleHonesty,directionFromOracle,N):
    
 
    #updating position in the direction given by oracle by 1/N
    #updating LRI_Array in the direction given by oracle
    
    #print("THE ID OF THE ROBOT THAT WE ARE WORKING WITH IS ID ======> : ", LA_Robot.get_LA_ID())
    
    LRI_ARRAY = LA_Robot.get_lriArray()
    
    if(OracleHonesty == True):
        if(directionFromOracle == "Left"):
            currPos = LA_Robot.get_CurrPos()
            newPos = currPos - (1/N)
            LA_Robot.update_pos(newPos)
            
            newLRI_array = [LRI_ARRAY[0] + (1/N),LRI_ARRAY[1] - (1/N)]
            LA_Robot.update_lriArray(newLRI_array)
        
        if(directionFromOracle == "Right"):
            currPos = LA_Robot.get_CurrPos()
            newPos = currPos + (1/N)
            LA_Robot.update_pos(newPos)
            
            newLRI_array = [LRI_ARRAY[0] - (1/N),LRI_ARRAY[1] + (1/N)]
            LA_Robot.update_lriArray(newLRI_array)
    
    elif(OracleHonesty == False):
        if(directionFromOracle == "Left"):
            currPos = LA_Robot.get_CurrPos()
            newPos = currPos + (1/N)
            LA_Robot.update_pos(newPos)
            
            newLRI_array = [LRI_ARRAY[0] - (1/N),LRI_ARRAY[1] + (1/N)]
            LA_Robot.update_lriArray(newLRI_array)
        
        if(directionFromOracle == "Right"):
            currPos = LA_Robot.get_CurrPos()
            newPos = currPos - (1/N)
            LA_Robot.update_pos(newPos)
            
            newLRI_array = [LRI_ARRAY[0] + (1/N),LRI_ARRAY[1] - (1/N)]
            LA_Robot.update_lriArray(newLRI_array)
    


#Calling main function to start program
main()
