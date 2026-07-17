import sys


class StudyAgentException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()

        if exc_tb is not None:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.line_number = "Unknown"

        self.error_message = error_message

        super().__init__(self.__str__())

    def __str__(self):
        return (
            f"\nError occurred in Python script: [{self.file_name}]"
            f"\nLine Number: [{self.line_number}]"
            f"\nError Message: {self.error_message}"
        )