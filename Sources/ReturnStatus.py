from enum import Enum

"""
Code by Lachlan Woods (lsw1@hw.ac.uk)
Files can not be copied and/or distributed without receiving permission from Lachlan Woods

ReturnStatus: Contains an enum of return statuses that can be returned by a function
"""

class ReturnStatus(Enum):
    BAD_ID = "Could not find any results with the specified user and document id"
    BAD_File = "Could not load file"
    NO_LIKES = "Could not find any 'also likes' documents"
    Bad_Task = "Invalid task name. Please type -h for usage info"
    SUCCESS = "Success"
