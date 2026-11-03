'''
name = input("What is your name? ")
file = open("names.csv", "a")
file.write(f"{name}\n")
file.close()
'''
"""
name = input("What is your name? ")
with open("names.csv", "a") as file:
    file.write(f"{name}\n")
"""
"""
import csv
students = []
with open("names.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({"name": row["name"], "home": row["house"]})



for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['home']}")
"""
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Invalid name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def main():
    student = get_student()
    student.house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
