# Employee management
## _A simple CRUD app made with django_

This is a CRUD app made with django that can perform standard actions on employee,
Made with django, hosted on heroku.

## Features

- Add/Delete/Edit any employee
- Add/Delete/Edit department or location a given employee works at
- PDF/Excel generator based on weekly payroll of a given department
- Many more 🥳








# Change Log
All notable changes to this project will be documented in this file.


## [1.0.0] - August 3 2022
First release of temp agency app.

### Added
- [EMPLOYEE MANAGEMENT](http://app.omegaplacement.ca/employee_management/)
  Main app -> can add/delete/update locations, employees and weekly calendars




## [1.0.1] - August 7 2022
### Fixed
- [EMPLOYEES](http://employee_management/)
  MINOR FIXES filename of PDF, EXCEL and PRINT
- [LOCATIONS](http://employee_management/locations)
  MINOR FIXES filename of PDF, EXCEL and PRINT
- [WEEKLY CALENDAR](http://employee_management/locations)
  MINOR FIXES filename of PDF, EXCEL and PRINT


## [1.0.2] - August 8 2022
### Added
- Added shared database between prod and dev for ==> postgrel and sqlite3

### Changed
- Changed on.DELETE method for employees, employees are still saved even when assigned location is deleted (default place == DEFAULT)



