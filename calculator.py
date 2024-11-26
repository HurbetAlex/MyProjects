
def changes_value(index, current_values):
    new_value = float(input("Enter the new value: "))
    current_values[index - 1] = new_value
    return current_values

def enter_values():
    temp1 = float(input("Enter first number: "))
    temp2 = float(input("Enter second number: "))
    return temp1, temp2

def operation_choice():
    print("Calculation Menu:"
          "\n1 Addition (+)"
          "\n2 Subtraction (-)"
          "\n3 Multiplication (*)"
          "\n4 Division (/)"
          "\nC: Clear last input"
          "\nAC: Reset everything"
          "\nEnter your choice"
          )
    return input("Your choice: ").strip()

def calculate(current_values, choice, previous_result):
    if choice == "1":
        return current_values[0] + current_values[1]
    elif choice == "2":
        return current_values[0] - current_values[1]
    elif choice == "3":
        return current_values[0] * current_values[1]
    elif choice == "4":
        if current_values[1] == 0:
            return "ERROR (Division by zero)"
        return current_values[0] / current_values[1]
    elif choice.upper() == "C":
        print("Which number do you want to clear? (1 or 2)")
        index = int(input())
        current_values[index - 1] = 0
        return previous_result
    elif choice.upper() == "AC":
        return "RESET"
    else:
        return "ERROR: Invalid choice"

def main():
    print("Welcome to Calculator")
    current_values = enter_values()
    previous_result = 0

    while True:
        choice = operation_choice()
        if choice.upper() == "AC":
            current_values = enter_values()
            previous_result = 0
            print("Reset Complete. Entered new numbers.")
        else:
            result = calculate(current_values, choice, previous_result)
            if result == "RESET":
                current_values = enter_values()
                previous_result = 0
            elif result == "ERROR (Division by zero)":
                print(result)
            elif result == "ERROR: Invalid choice":
                print("Please enter a valid choice.")
            else:
                print(f"Result: {result}")
                previous_result = result
            if choice.upper() != "C":
                print("Do you want to update any value? (y/n)")
                update = input().strip().lower()
                if update == "y":
                    print("Which number do you want to change? (1 or 2)")
                    index = int(input())
                    current_values = changes_value(index, current_values)

if __name__ == "__main__":
    main()