# USC-Schedule
USC Schedule of Classes API wrapper

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/switchswap/usc-schedule/Python%20package?style=for-the-badge) 
![PyPI](https://img.shields.io/pypi/v/usc-schedule?style=for-the-badge) 

## Introduction
This library provides a python interface for the USC Schedule of Classes api. It works for Python versions from 3.6 onwards.

## Installation
`$ pip install usc-schedule`

## Usage
### Setup
```python
from uscschedule import Schedule
schedule = Schedule()
```

### Get department
```python
csci_department = schedule.get_department(department_id="CSCI", semester_id=20201)
# Alternatively: schedule.get_department("CSCI", 20201)
print(csci_department.department)
print(csci_department.abbreviation)
print(csci_department.department_url)

# Prints:
# Computer Science
# CSCI
# http://www.cs.usc.edu/

```

### Get course details
```python
csci_course = schedule.get_course(course_id="CSCI-201", semester_id=20201)
# Alternatively: schedule.get_course("CSCI-201", 20201)
print(csci_course.title)
print(csci_course.units)
print(csci_course.description)

# Prints:
# Principles of Software Development
# 4.0
# Object-oriented paradigm for programming-in-the-large in Java; writing sophisticated concurrent 
# applications with animation and graphic user interfaces; using professional tools on team project.
# Prerequisite: CSCI 104L.
```
