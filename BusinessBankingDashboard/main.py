from district import district_menu
from branch import branch_menu


def display_menu():

    print("\n" + "=" * 45)
    print(" BUSINESS BANKING PERFORMANCE SYSTEM")
    print("=" * 45)

    print("1. Manage Districts")
    print("2. Manage Branches")
    print("3. Set Planned Targets")
    print("4. Record Actual Performance")
    print("5. View District Performance")
    print("6. View Branch Performance")
    print("7. Performance Ranking")
    print("8. Generate Reports")
    print("9. Export to Excel")
    print("10. Exit")

    print("=" * 45)


def main():

    districts = []
    branches = []

    while True:

        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            district_menu(districts)

        elif choice == "2":
            branch_menu(branches, districts)

        elif choice == "10":
            print("Thank you for using the system!")
            break

        else:
            print("This feature will be developed in upcoming lessons.")


if __name__ == "__main__":
    main()