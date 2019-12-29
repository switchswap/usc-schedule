class CourseNotFoundException(Exception):
    def __init__(self, message):
        self.error = message
        super(CourseNotFoundException, self).__init__(message)


class DepartmentNotFoundException(Exception):
    def __init__(self, message):
        self.error = message
        super(DepartmentNotFoundException, self).__init__(message)
