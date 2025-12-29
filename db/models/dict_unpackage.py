person_json = {
    "name": "Nikolai",
    "age": 39,
    "job": "Accountant",
}

another_json = {
    "name": "Danus",
    "age": 70,
    "job": "Engineer",
}

class Person:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

    def get_info(self):
        print(f"{self.name} is {self.age} and is a/an {self.job}")

person = Person(person_json["name"], person_json["age"], person_json["job"])
person.get_info()

person2 = Person(**another_json)
person2.get_info()