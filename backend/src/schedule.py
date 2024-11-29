from ortools.sat.python import cp_model


def shift_schedule(*, employees, shifts, availability):
    model = cp_model.CpModel()

    # Variables: employee-shift assignment
    employee_shift_vars = {}
    for employee in employees:
        for shift in shifts:
            employee_shift_vars[(employee.id, shift.id)] = model.NewBoolVar(
                f"employee_{employee.id}_shift_{shift.id}"
            )

    # Constraint: Employee availability based on day and time range
    for employee in employees:
        employee_availability = [
            avail for avail in availability if avail.employee_id == employee.id
        ]
        for shift in shifts:
            is_available = False
            for avail in employee_availability:
                if (
                    shift.shift_week_day == avail.day_of_week
                    and shift.shift_start_time >= avail.start_time
                    and shift.shift_end_time <= avail.end_time
                ):
                    is_available = True
                    break
            if not is_available:
                model.Add(employee_shift_vars[(employee.id, shift.id)] == 0)

    # Objective: Maximize the number of assigned shifts
    model.Maximize(sum(employee_shift_vars.values()))

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Collect the solution
    assignments = []
    if status == cp_model.OPTIMAL:
        for employee in employees:
            for shift in shifts:
                if solver.Value(employee_shift_vars[(employee.id, shift.id)]) == 1:
                    assignments.append(
                        {
                            "employee_id": employee.id,
                            "shift_id": shift.id,
                            "shift_date": shift.shift_date,
                            "shift_desc": shift.shift_desc,
                            "shift_start_time": shift.shift_start_time,
                            "shift_end_time": shift.shift_end_time,
                            "assigned": True,
                        }
                    )
    return assignments
