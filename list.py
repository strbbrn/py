students = [
    {'name': 'shashi', 'roll_no': '123', 'year': '2023'},
    {'name': 'rajshree', 'roll_no': '456', 'year': '2023'},
    {'name': 'bikram', 'roll_no': '789', 'year': '2024'},
    {'name': 'blue', 'roll_no': '101', 'year': '2024'}
]


def print_students():
    print("######print_students#######")
    print(students)
    print("#############")

print_students()
### OUTPUT OF THIS FUNCTION CALL
##  [
# {'name': 'shashi', 'roll_no': '123', 'year': '2023'}, 
# {'name': 'rajshree', 'roll_no': '456', 'year': '2023'}, 
# {'name': 'bikram', 'roll_no': '789', 'year': '2024'}, 
# {'name': 'blue', 'roll_no': '101', 'year': '2024'}
#   ]
###

def print_only_one():
    print("######print_only_one#######")
    print(students[0]) ## passing the 0 index to print the first obj
    print("#############")
print_only_one()    
######print_only_one#######
#{'name': 'shashi', 'roll_no': '123', 'year': '2023'}
#############

def loop_through_list():
    print("######loop_through_list#######")
    for student in students:
        print(student)
    print("#############")
loop_through_list()
######loop_through_list#######
#{'name': 'shashi', 'roll_no': '123', 'year': '2023'}
#{'name': 'rajshree', 'roll_no': '456', 'year': '2023'}
#{'name': 'bikram', 'roll_no': '789', 'year': '2024'}
#{'name': 'blue', 'roll_no': '101', 'year': '2024'}
#############

def filter_list():
    print("#######filter_list######")
    for student in students:
        if student['year'] == "2023":
            print(student)
    print("#############")
filter_list()
#######filter_list######
#{'name': 'shashi', 'roll_no': '123', 'year': '2023'}
#{'name': 'rajshree', 'roll_no': '456', 'year': '2023'}
#############

#storing filtered students in a new list
def filter_list_store():
    print("#######filter_list_store######")
    new_student=[]
    for student in students:
        if student['year'] == "2023":
            new_student.append(student)
    print(new_student)
    print("#############")
filter_list_store()
#######filter_list_store######
#[{'name': 'shashi', 'roll_no': '123', 'year': '2023'}, {'name': 'rajshree', 'roll_no': '456', 'year': '2023'}]
#############
