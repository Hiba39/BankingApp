class Branch:

    def __init__(self, branch_id, name, district_id):

        self.branch_id = branch_id
        self.name = name
        self.district_id = district_id


def add_branch(branches, districts):

    print("\n--- REGISTER NEW BRANCH ---")

    if not districts:
        print("Please register a district first.")
        return

    print("\nAvailable Districts:")

    for district in districts:
        district.display_info()

    branch_id = input("\nEnter Branch ID: ").strip()
    name = input("Enter Branch Name: ").strip()
    district_id = input("Enter District ID: ").strip()

    if not branch_id or not name or not district_id:
        print("All fields are required.")
        return

    for branch in branches:

        if branch.branch_id == branch_id:
            print("Branch ID already exists.")
            return

    district_exists = False

    for district in districts:

        if district.district_id == district_id:
            district_exists = True
            break

    if not district_exists:
        print("District not found.")
        return

    new_branch = Branch(branch_id, name, district_id)

    branches.append(new_branch)

    print("Branch registered successfully!")


def view_branches(branches, districts):

    print("\n--- REGISTERED BRANCHES ---")

    if not branches:
        print("No branches registered.")
        return

    for branch in branches:

        district_name = "Unknown"

        for district in districts:

            if district.district_id == branch.district_id:
                district_name = district.name
                break

        print("--------------------------------")
        print(f"Branch ID: {branch.branch_id}")
        print(f"Branch Name: {branch.name}")
        print(f"District: {district_name}")


def branch_menu(branches, districts):

    while True:

        print("\n===== BRANCH MANAGEMENT =====")
        print("1. Register Branch")
        print("2. View Branches")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_branch(branches, districts)

        elif choice == "2":
            view_branches(branches, districts)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Try again.")