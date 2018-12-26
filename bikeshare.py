import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Enter a city (Chicago, New York City, Washington): ')
            if city.lower() in ['chicago', 'new york city', 'washington']:
                break
            else:
                print('Not a valid city. Please try again.')
        except:
            print('Not a valid input.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Enter a month (January to June) or all for all months: ')
            if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Not a valid month. Please try again.')
        except:
            print('Not a valid input.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Enter a day of the week or all: ')
            if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('Not a valid input.')
        except:
            print('Not a valid input.')

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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    #print(df.head())
    
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month_num = months.index(month.lower()) + 1
        #df = df[df['month'] ==  month_num]
        df = df[df['month'] ==  months.index(month.lower()) + 1]

    if day.lower() != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #day_num = days.index(day.lower())
        #df = df[df['day_of_week'] == day_num]
        df = df[df['day_of_week'] == days.index(day.lower())]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if 'month' not in df.columns:
        df['month'] = df['Start Time'].dt.month
        
    popular_month = df['month'].value_counts().first_valid_index()
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[popular_month - 1]
    
    # display the most common day of week
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        
    popular_day = df['day_of_week'].value_counts().first_valid_index()
    days = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays']
    popular_day = days[popular_day]
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().first_valid_index()
    h = datetime.timedelta(hours = int(popular_hour))

    print('Most popular month to ride a bike is {}.\nMost popular day of the week to ride a bike is {}.\nThe most popular hour to a ride a bike is {}.'.format(popular_month, popular_day, h))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].value_counts().first_valid_index()
    print('Most popular start station is {}.'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().first_valid_index()
    print('Most popular end station is {}.'.format(popular_end))

    # display most frequent combination of start station and end station trip
    df['Start_Stop'] = df['Start Station'] + ' and ' + df['End Station']
    popular_start_end = df['Start_Stop'].value_counts().first_valid_index()
    print('Most popular combination of start and stop is {}.'.format(popular_start_end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    travel_time = str(datetime.timedelta(seconds = int(travel_time)))
    print('Total travel time during the given time window is {}.'.format(travel_time))

    # display mean travel time
    travel_mean = df['Trip Duration'].mean()
    travel_mean = str(datetime.timedelta(seconds=float(travel_mean)))
    print('Mean travel time during the given time window is {}.'.format(travel_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('The count of the different user types within the given time window are as follows:') 
        print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nThe count of the different user\'s gender within the gien time window are as follows:')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        common_bday = df['Birth Year'].value_counts().first_valid_index()
        print('\nThe earlierst birthyear: {}\nMost recent birthyear: {}\nMost common birthyear: {}'.format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(common_bday)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data as requested by the user 5 rows at a time."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    show = input('Would you like to see the first 5 rows of raw data? (Yes or No): ')
    if show.lower() == 'yes':
        i = 0
        while True:
            #Excludes the columns I added to dataframe for other methods.
            print(df[df.columns[0:len(df.columns)-4]][i:i+5])
            i += 5
            show = input('Would you like to see the next 5 rows? (Yes or No): ')
            if show.lower() != 'yes':
                break
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
