class Base:
    def __init__(self, response: dict):
        self.response = response


class Department(Base):
    def __init__(self, response: dict):
        super().__init__(response)
        self.schedule_sync_time = response.get("schd_sync_dtm")

        department_info = response.get("Dept_Info")
        self.department = department_info.get("department")
        self.abbreviation = department_info.get("abbreviation")
        self.phone_number = department_info.get("phone_number")
        self.address = department_info.get("address")
        self.notes = department_info.get("Notes")
        self.term_notes = department_info.get("TermNotes")
        self.department_url = department_info.get("dept_url")
        self.courses = self.__get_courses()

    def __get_courses(self):
        if type(self.response.get("OfferedCourses").get("course")) is list:
            return [Course(response) for response in self.response.get("OfferedCourses").get("course")]
        elif type(self.response.get("OfferedCourses").get("course")) is dict:
            return [Course(self.response.get("OfferedCourses").get("course"))]
        else:
            return []


class Course(Base):
    def __init__(self, response: dict):
        super().__init__(response)
        self.cross_listed = True if response.get("IsCrossListed") == "Y" else False
        self.published_course_id = response.get("PublishedCourseID")
        self.scheduled_course_id = response.get("ScheduledCourseID")
        # Grab course data
        response = self.response.get("CourseData")
        self.prefix = response.get("prefix")
        self.number = response.get("number")
        self.sequence = response.get("sequence")
        self.suffix = response.get("suffix")
        self.title = response.get("title")
        self.description = response.get("description")
        self.units = response.get("units")
        self.restriction_by_major = response.get("restriction_by_major")
        self.restriction_by_class = response.get("restriction_by_class")
        self.restriction_by_school = response.get("restriction_by_school")
        self.course_notes = response.get("CourseNotes")
        self.course_term_notes = response.get("CourseTermNotes")
        self.prereq_text = response.get("prereq_text")
        self.coreq_text = response.get("coreq_text")
        self.sections = self.__get_section_data()
        self.lecture_capacity = 0
        self.lecture_registered = 0
        self.lab_capacity = 0
        self.lab_registered = 0
        self.discussion_capacity = 0
        self.discussion_registered = 0
        self.is_lab_only = True
        # Parse class data from section data
        self.__parse_class_data()

    def __get_section_data(self):
        response = self.response.get("CourseData")
        if type(response.get("SectionData")) is list:
            return [SectionData(response) for response in response.get("SectionData")]
        elif type(response.get("SectionData")) is dict:
            return [SectionData(response.get("SectionData"))]
        else:
            return []

    def __parse_class_data(self):
        for section in self.sections:
            # If section is lecture type (Lecture, Lecture-Lab, Lecture-Discussion)
            if section.type == "Lec" or section.type == "Lec-Lab" or section.type == "Lec-Dis":
                self.is_lab_only = False
                self.lecture_capacity += section.capacity
                self.lecture_registered += section.registered
            elif section.type == "Lab":
                self.lab_capacity += section.capacity
                self.lab_registered += section.registered
            elif section.type == "Dis":  # Discussion
                self.is_lab_only = False
                self.discussion_capacity += section.capacity
                self.discussion_registered += section.registered
            else:  # Quiz (Qz)
                self.is_lab_only = False

    def is_full(self) -> bool:
        """
        If all sections are full, the course is fully closed
        """
        # If difference of capacity and registered students is less than 0, the class must be full
        return (self.lecture_capacity + self.lab_capacity + self.discussion_capacity) - \
               (self.lecture_registered + self.lab_registered + self.discussion_registered) <= 0

    def has_lecture_sections(self) -> bool:
        return self.lecture_capacity > 0

    def has_discussion_sections(self) -> bool:
        return self.discussion_capacity > 0

    def has_lab_sections(self) -> bool:
        return self.lab_capacity > 0

    def all_lectures_closed(self) -> bool:
        return self.lecture_capacity - self.lecture_registered <= 0

    def all_discussions_closed(self) -> bool:
        return self.discussion_capacity - self.discussion_registered <= 0

    def all_labs_closed(self) -> bool:
        return self.lab_capacity - self.lab_registered <= 0


class SectionData(Base):
    def __init__(self, response: dict):
        super().__init__(response)
        self.id = response.get("id")
        self.session = response.get("session")
        self.dclass_code = response.get("dclass_code")
        self.title = response.get("title")
        self.section_title = response.get("section_title")
        self.description = response.get("description")
        self.notes = response.get("notes")
        self.type = response.get("type")
        self.units = response.get("units")
        self.capacity = int(response.get("spaces_available"))
        self.registered = int(response.get("number_registered"))
        self.wait_quantity = response.get("wait_qty")
        self.canceled = True if self.response.get("canceled") == "Y" else False
        self.blackboard = response.get("blackboard")
        self.day = response.get("day")
        self.start_time = response.get("start_time")
        self.end_time = response.get("end_time")
        self.location = response.get("location")
        self.distance_learning = True if response.get("IsDistanceLearning") == "Y" else False
        self.instructors = self.__get_instructors()
        self.fees = self.__get_fees()

        # Section is close if there are greater or equal registered than available
        self.closed = self.registered >= self.capacity

    def __get_instructors(self):
        if type(self.response.get("instructor")) is list:
            return [Instructor(response) for response in self.response.get("instructor")]
        elif type(self.response.get("instructor")) is dict:
            return [Instructor(self.response.get("instructor"))]
        else:
            return []

    def __get_fees(self):
        if type(self.response.get("fee")) is list:
            return [Fee(response) for response in self.response.get("fee")]
        elif type(self.response.get("fee")) is dict:
            return [Fee(self.response.get("fee"))]
        else:
            return []

    def get_available_spots(self) -> int:
        return self.capacity - self.registered

    def requires_d_clearance(self) -> bool:
        return self.dclass_code == 'D'


class Instructor(Base):
    def __init__(self, response: dict):
        super().__init__(response)
        self.first_name = response.get("first_name")
        self.last_name = response.get("last_name")
        self.bio_url = response.get("bio_url")

    def get_name(self):
        return self.first_name + " " + self.last_name


class Fee(Base):
    def __init__(self, response: dict):
        super().__init__(response)
        self.description = response.get("description")
        self.amount = response.get("amount")
