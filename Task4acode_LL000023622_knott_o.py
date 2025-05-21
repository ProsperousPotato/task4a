import pandas as pd
import matplotlib.pyplot as plt


# Outputs the initial menu and validates the input
# noinspection PyUnboundLocalVariable
def main_menu():
    flag = True

    while flag:

        print("####################################################")
        print("############# Botes Parcels CRM System #############")
        print("####################################################")
        print("")
        print("########### Please select an option ################")
        print("### 1. Total issues by type")
        print("### 2. Days to resolve by issue type")
        print("### 3. Average days to resolve issues by region")
        print("### 4. Total number of issues and resolutions per region")
        print("### 9. Exit")

        choice = input('Enter your number selection here: ')

        try:
            int(choice)
        except:
            print("Sorry, you did not enter a valid option")
            flag = True
        else:
            if int(choice) not in valid_options:  # If user enters an integer but it is not in valid options
                #                                   it will not print 'Choice Accepted' as it did before
                print("Sorry, you did not enter a valid option")
                flag = True
            else:
                print('Choice accepted!')
                flag = False

    return choice


# Submenu for totals, provides type check validation for the input and returns issue type as a string
# noinspection PyUnboundLocalVariable
def total_menu():
    flag = True

    issue_type_list = ["Customer Account Issue", "Delivery Issue", "Collection Issue", "Service Complaint"]

    while flag:

        print("####################################################")
        print("########### Select an issue to analyse #############")
        print("####################################################")
        print("")
        print("########## Please select an issue type ##########")
        print("### 1. Customer Account Issue")
        print("### 2. Delivery Issue")
        print("### 3. Collection Issue")
        print("### 4. Service Complaint")

        choice = input('Enter your number selection here: ')

        try:
            int(choice)
            while True:  # Stop users inputting integers that are out of the bounds of the list.
                if 0 < int(choice) <= (len(issue_type_list)):
                    break
                else:
                    print("Choice out of bounds, select again")
                    choice = input('Enter your number selection here: ')

        except:
            print("Sorry, you did not enter a valid option")
            flag = True
        else:
            print('Choice accepted!')
            choice = int(choice)
            flag = False

    issue_type = issue_type_list[choice - 1]

    return issue_type


# Function to load csv file, modularise code further
def load_data():
    df = pd.read_csv("Task4a_data.csv")
    return df


# Creates a new dataframe then counts the number of occurrences of the requested issue type

def get_total_data(menu_choice):
    try:
        issues = load_data()
    except FileNotFoundError:  # Catch file not found error and return from the function. Stops errors filling terminal
        #                        and cleanly exits
        print("Error: File Task4a_data.csv not found")
        return

    total = issues['Issue Type'].value_counts()[menu_choice]

    msg = "The total number of issues logged as a {} was: {}".format(menu_choice, total)
    return msg


def resolution_time(menu_choice):
    try:
        df = load_data()
    except FileNotFoundError:
        print("Error: File Task4a_data.csv not found")
        return

    # Group the dataframe by the issue type and limit by the days to resolve
    filtered_df = df.groupby("Issue Type")["Days To Resolve"]

    # Get the mean, max, and minimum values for the selected issue type choice
    average_days = filtered_df.mean()[menu_choice]
    highest_days = filtered_df.max()[menu_choice]
    lowest_days = filtered_df.min()[menu_choice]

    # Print the data in a human-readable format
    print(f"\nThe issue type '{menu_choice}' took on average {average_days:.2f} days to resolve")
    print(f"With a max time of {highest_days} days and a minimum time of {lowest_days} day to resolve\n")


def days_to_resolve_by_region():
    try:
        df = load_data()
    except FileNotFoundError:
        print("Error: File Task4a_data.csv not found")
        return

    # Get the average days to resolve and limit by the number
    avg_days = df.groupby("Region")["Days To Resolve"].mean()

    plt.style.use("ggplot")
    plt.figure(figsize=(10, 8))
    # Plot the data from the dataframe
    avg_days.plot(kind="bar")
    plt.xticks(rotation=45)
    plt.title("Average days to resolve issues by region")
    plt.xlabel("Region")
    plt.ylabel("Days")
    plt.tight_layout()
    plt.show()


def total_number_of_issues_per_region():
    # Number of issues and resolutions are the same. Only need to find the number of either
    try:
        df = load_data()
    except FileNotFoundError:
        print("Error: File Task4a_data.csv not found")
        return

    issues = df.groupby("Region")["Issue Type"].value_counts()

    # Get lists of the data for the axes
    regions_list = list(df["Region"].unique())

    issues_list = []

    # Append the sum of each region's issues to the list
    for i in regions_list:
        issues_list.append(int(issues.loc[i].sum()))

    plt.style.use("ggplot")
    plt.figure(figsize=(10, 8))
    # Plot the data from each of the lists
    plt.bar(regions_list, issues_list)
    plt.xticks(rotation=45)
    plt.title("Issue and Resolution Counts")
    plt.xlabel("Regions")
    plt.ylabel("Number of Issues and Resolutions")
    plt.tight_layout()
    plt.show()


valid_options = [1, 2, 3, 4, 9]

while True:
    main_menu_choice = main_menu()
    if main_menu_choice == "1":
        total_menu_choice = total_menu()
        print(get_total_data(total_menu_choice))
    elif main_menu_choice == "2":
        total_menu_choice = total_menu()
        resolution_time(total_menu_choice)
    elif main_menu_choice == "3":
        days_to_resolve_by_region()
    elif main_menu_choice == "4":
        total_number_of_issues_per_region()
    elif main_menu_choice == "9":
        exit(0)
