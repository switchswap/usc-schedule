from uscschedule import Schedule

schedule = Schedule()


def test_course_counts():
    writ_340 = schedule.get_course(course_id="WRIT-340", semester_id=20201)
    assert writ_340.lecture_capacity == 2680
    assert writ_340.lecture_registered == 2492
    assert len(writ_340.sections) == 141


def test_course_details():
    csci_201 = schedule.get_course(course_id="CSCI-201", semester_id=20201)
    assert csci_201.cross_listed is False
    assert len(csci_201.sections) == 9
    assert len(csci_201.sections[0].instructors) == 1
    assert csci_201.sections[0].instructors[0].get_name() == "Jeffrey Miller"
    assert csci_201.sections[0].canceled is False
    assert csci_201.sections[0].distance_learning is False
    assert csci_201.sections[0].requires_d_clearance() is True
    assert csci_201.has_lab_sections() is True
    assert csci_201.has_lecture_sections() is True
    assert csci_201.has_discussion_sections() is False


def test_department_details():
    csci = schedule.get_department(department_id="CSCI", semester_id=20201)
    assert csci.department == "Computer Science"
    assert csci.abbreviation == "CSCI"
    assert csci.department_url == "http://www.cs.usc.edu/"
