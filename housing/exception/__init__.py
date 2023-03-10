import os
import sys

class HousingExceptions(Exception):
    
    def __init__(self,error_message:Exception, error_detail:sys):
        super().__init__(error_message) #Exception(error_message)
        self.error_message=HousingExceptions.get_detailed_error_messgae(error_message=error_message, 
                                                                        error_detail=error_detail)


    @staticmethod
    def get_detailed_error_messgae(error_message:Exception, error_detail:sys)->str:
        """
        error_messgae = Exception object,
        error_detail = object of the sys module
        """
        _,_,exec_tb=error_detail.exc_info()

        line_number=exec_tb.tb_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename
        error_message= f"Error occured in script: [{file_name}] at line number: [{line_number}] error message: [{error_message}]"


        return error_message

    ## when using HousingException object, __str__ will print the error message
    def __str__(self):
        return self.error_message
    
    ## when using HousingException object, __repr__ will return the error message    
    def __repr__(self)-> str:
        return HousingExceptions.__name__.str()

    