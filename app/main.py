"""
This is the entry point for the app. It consists of CRUD API endpoints for the employee table.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Employee

app = FastAPI()

@app.on_event("startup")
def create_table():
    """This function creates the table."""
    Base.metadata.create_all(bind=engine)

@app.post("/employees/")
def create_employee(name: str, department: str, database: Session = Depends(get_db)):
    """This function creates an employee.

    Args:
        name (str): Name of the employee.
        department (str): Department of the employee.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raises exception in case of a bad request.

    Returns:
        dict: JSON response with the employee added.
    """
    try:
        employee = Employee(name=name, department=department)
        database.add(employee)
        database.commit()
        return {"Employee added": employee.name}
    except HTTPException as ex:
        raise ex(status_code=status.HTTP_400_BAD_REQUEST) from None

@app.get("/employees/")
@app.get("/employees/{employee_id}")
def get_employee(employee_id: str = None, database: Session = Depends(get_db)):
    """Get employees either by ID or all employees.

    Args:
        employee_id (str, optional): ID of the employee. Defaults to None.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raises 404 if employee(s) not found.

    Returns:
        dict: JSON response with status and employee data.
    """
    if employee_id:
        employee = database.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employee with ID {employee_id} not found")
        return {"status": status.HTTP_200_OK, "employee": employee}
    employees = database.query(Employee).all()
    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Employees not found")
    return {"status": status.HTTP_200_OK, "employees": employees}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, database: Session = Depends(get_db)):
    """This function deletes the record of an employee.

    Args:
        employee_id (str): ID of the employee.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raises exception if the employee is not found.

    Returns:
        Response: Response with status code indicating success.
    """
    employee_query = database.query(Employee).filter(Employee.id == employee_id)
    employee = employee_query.first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with ID {employee_id} not found")
    employee_query.delete(synchronize_session=False)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/employees/{employee_id}/{column}/{new_value}")
def update_employee(employee_id: str,
                    column: str,
                    new_value: str,
                    database: Session = Depends(get_db)):
    """
        This function updates the record of an employee.

        Args:
            employee_id (str): ID of the employee.
            column (str): Column name to update.
            new_value (str): New value for the column.
            db (Session, optional): Database session. Defaults to Depends(get_db).

        Raises:
          HTTPException: Raises exception if the employee is not found.

        Returns:
            dict: JSON response indicating success and the updated employee data.
    """
    employee_query = database.query(Employee).filter(Employee.id == employee_id)
    database_employee = employee_query.first()

    if not database_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with ID {employee_id} not found")

    setattr(database_employee, column, new_value)
    database.add(database_employee)
    database.commit()
    database.refresh(database_employee)
    return {"status": "success", "employee": database_employee}
