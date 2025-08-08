🔧 Objective
To provide HR managers a convenient way to assign employee shifts in bulk through an Excel template with validations, upload capability, holiday list integration, and employee limits.
1️⃣ Key Features
✅ Shift Allocation Tool
Custom DocType to manage shift allocations.

Includes:

Date range selection.

Shift type selection.

“Get Employees” button to fetch eligible employees based on filters.

Excel Download and Upload options for shift assignment.

✅ Excel Template
Dynamic column generation for each day in the selected date range.

Pre-filled with:

Serial number

Employee ID

Employee Name

Supports:

Drop-down for shift selection using data validation.

Weekday header for better readability.

✅ Upload & Validation
Uploaded Excel is validated for:

Existing entries (prevent duplicates).

Employee limit (max 50 employees allowed).

Empty/missing data (employee/shift).

Error messages shown to guide user if upload fails.

✅ Holiday Check
On upload, validates if employee has holiday list assigned.

Automatically integrates weekly off if not in existing holiday list.
2️⃣ 🔧 Manual Setup Required by User
Before using the Shift Allocation Tool, the user must manually configure the following:

🔹 1. Shifts
Go to: HR > Shift Type

Create shift types such as:

Morning Shift

Evening Shift

Night Shift

Ensure fields like:

Shift Name

Start Time

End Time

Holiday List (optional)
are properly configured.

🔹 2. Holiday List
Go to: Setup > Holiday List

Create or update a holiday list with:

Weekly offs (e.g., Sundays)

National holidays

Assign this list to:

Each Employee

Or include in Shift Type

🔹 3. Employee Records
Ensure each employee:

Has a valid Employee ID

Is marked as Active

Has a Holiday List linked (important for validation)

Is assigned to the relevant Department or Branch (if filters are used)

🔹 4. Permissions
Assign role-based permissions to HR Manager or HR User for:

Reading/Writing Shift Allocation Tool

Accessing Shift Type, Employee, Holiday List
