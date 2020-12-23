import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
DATA_FILTER = ["month", "day", "not at all"]
MONTHS_NAME = ["january", "february", "march", "april", "may", "june", "all"]
DAYS_NAME = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]

def get_filters():
    """
    Asks user to specify a cnoity, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #interactive code to get the city:
    city="not knowen yet"
    while city not in CITY_DATA.keys():
        city = str(input("Would you like to see data for 'Chicago', 'New York', or 'Washington'?\n")).lower()

        if city not in CITY_DATA.keys():
            print("City not entered correctly, please type it again.\n")


    #interactive code to get the filter:
    filter = "not knowen yet"
    month_value = "not knowen yet"
    day_value = "not knowen yet"
    while filter not in DATA_FILTER:
        filter = str(input("Would you like to filter the data by 'month', 'day', or 'not at all'?\n")).lower()

        if filter == "month":
            while month_value not in MONTHS_NAME:
                month_value = str(input("Which month - January, February, March, April, May, or June?\n")).lower()
                day_value = "all"
                if month_value not in MONTHS_NAME:
                    print("Month not entered correctly, please type it again.\n")

        elif filter == "day":
            while day_value not in DAYS_NAME:
                month_value = "all"
                day_value = str(input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")).lower()
                if day_value not in DAYS_NAME:
                    print("Day not entered correctly, please type it again.\n")

        elif filter == "not at all":
            month_value = "all"
            day_value = "all"

        else:
            print("Filter not entered correctly, please type it again.\n")

    # get user input for month (all, january, february, ... , june)
    month = month_value

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = day_value

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv('./{}'.format(CITY_DATA.get(city)))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print("Most common month is {}".format(MONTHS_NAME[common_month-1].capitalize()))

    # display the most common day of week
    df['day of week'] = df['Start Time'].dt.weekday_name
    common_day = df['day of week'].mode()[0]
    print("Most common day of week is {}".format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most common hour is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most common start station is {}".format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most common end station is {}".format(common_end))

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'] + ' to ' + df['End Station']
    combination = df['Start To End'].mode()[0]
    print("Most common trip is {}".format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    df['Total travel time'] = df['End Time'] - df['Start Time']
    total_time = df['Total travel time'].sum()
    print("Total travel time = {}".format(total_time))

    # display mean travel time
    time_mode = df['Total travel time'].mode()[0]
    print("Mean travel time = {}".format(time_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("count users types:\n{}".format(user_types))

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print("count users gender:\n{}".format(user_gender))
    except:
        print('No gender data to share')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print("Earliest user birth year: {}".format(int(earliest_birth)))
        print("Most recent user birth year: {}".format(int(recent_birth)))
        print("Most common user birth year: {}".format(int(common_birth)))
    except:
        print('No birth data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_display(df):
    option_list = ['yes', 'no']
    user_option = "not known yet"

    counter = 0
    while user_option not in option_list:
        user_option = str(input("Would you like to veiw individual trip data?\nType (yes) or (no)\n")).lower()

        if user_option not in option_list:
            print("please type your choice correctly.\n")
        elif user_option == "yes":
            print(df.head(5))

    while user_option == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        user_option = str(input("Would you like to veiw more trip data?\nType (yes) or (no)\n")).lower()
        #If user opts for it, this displays next 5 rows of data
        if user_option == "yes":
            print(df[counter:counter+5])
        elif user_option != "yes":
            break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
