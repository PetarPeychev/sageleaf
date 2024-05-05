import {
    math,
    pprint from string
}

export {
    Employee,
    print_person
}

interface Person = {name: str, age: int};

# Employee satisfies the Person interface
type Employee = {name: str, age: int, salary: int};

print_person(person: Person) {
    print("Name: " + person.name);
    print("Age: " + person.age);
}

main() {
    let employee: Employee = {name: "John Doe", age: 42, salary: 100000};

    # since Employee satisfies the Person interface, we can pass it to print_person
    print_person(employee);
}
