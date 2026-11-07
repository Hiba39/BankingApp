class District:

    def __init__(self, district_id, name):

        self.district_id = district_id
        self.name = name

    def display_info(self):

        print(
            f"ID: {self.district_id} | "
            f"District: {self.name}"
        )


def add_district(districts):

    print("\n--- ADD NEW DISTRICT ---")

    district_id = input("Enter District ID: ").strip()
    name = input("Enter District Name: ").strip()

    if not district_id or not name:
        print("ID and name cannot be empty.")
        return

    for district in districts:

        if district.district_id == district_id:
            print("District ID already exists.")
            return

    new_district = District(district_id, name)

    districts.append(new_district)

    print("District added successfully!")


def view_districts(districts):

    print("\n--- DISTRICT LIST ---")

    if not districts:
        print("No districts registered.")
        return

    for district in districts:
        district.display_info()


def district_menu(districts):

    while True:

        print("\n===== DISTRICT MANAGEMENT =====")
        print("1. Add District")
        print("2. View Districts")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_district(districts)

        elif choice == "2":
            view_districts(districts)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")