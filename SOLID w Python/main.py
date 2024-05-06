from departments.dept_storage import DeptStorage
from departments.dept_service import DeptService
from employees.emp_storage import EmpStorage
from employees.emp_service import EmpService

if __name__ == "__main__":
    department_storage = DeptStorage()
    department_service = DeptService(department_storage)

    employee_storage = EmpStorage()
    employee_service = EmpService(employee_storage)

    department_service.add_department("HR", 50)
    department_service.add_department("IT", 30)

    employee_service.add_emp("sakib" , 23)
    employee_service.add_emp("Rahim", 18)
    employee_service.add_emp("sadman" , 23)

    print(department_service.getAlldepartment()) 
    print(employee_service.getAllEmp())

    department_service.removeDepartment("HR")
    employee_service.rmvEmp("Rahim")

    print(department_service.getAlldepartment()) 
    print(employee_service.getAllEmp())
