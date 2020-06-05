from . import models
from . import exceptions
from . import util
import json
import requests


class Schedule:
    def __init__(self):
        self.session = requests.Session()

    def get_course(self, course_id: str, semester_id: int) -> models.Course:
        # Split course_id into Department and Number
        course_info = course_id.split('-')

        # Error check the given information
        if len(course_info) != 2:
            raise exceptions.CourseNotFoundException("Could not find course!")
        if not course_info[0].isalpha() or not course_info[1].isdigit():
            raise exceptions.CourseNotFoundException("Could not find course!")

        # Get department of course
        dept_courses = self.get_department_courses(course_info[0], semester_id)

        # Look for course matching number and return it
        for course in dept_courses:
            if course.number == course_info[1]:
                return course

        # If it can't be found, raise Exception
        raise exceptions.CourseNotFoundException("Could not find course!")

    def get_department(self, department_id: str, semester_id: int) -> models.Department:
        url = f"https://web-app.usc.edu/web/soc/api/classes/{department_id}/{semester_id}"
        try:
            response = self.session.get(url).json()
            return models.Department(response)
        except json.JSONDecodeError:
            raise exceptions.DepartmentNotFoundException("Could not find department!")

    def get_department_courses(self, department_id: str, semester_id: int) -> list:
        department = self.get_department(department_id, semester_id)
        return department.courses

    def get_course_listing_json(self, semester_id: int):
        data = {}
        for department_id in util.departments:
            try:
                department = self.get_department(department_id, semester_id)
                data[department_id] = department
            except exceptions.DepartmentNotFoundException:
                pass
        return json.dumps(data, cls=util.ScheduleEncoder)
