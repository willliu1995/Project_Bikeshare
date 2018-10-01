import time
import time
import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}

city_dict = {'1': 'Chicago', '2': 'New York City', '3': 'Washington'}
month_dict = {'0': 'all', '1': 'january', '2': 'february', '3': 'march', '4': 'april', '5': 'may', '6': 'june'}
days_of_week_dict = {'0': 'all', '1': 'monday', '2': 'tuesday', '3': 'wednesday',
                     '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'}  # 本脚本采用ISO国际标准历法


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(" Hello! Let\'s explore some US bikeshare data!")

    def get_data(data_sets, tips, error_msg, success_msg):
        """
        获取数据所用的函数，可被所有需要选择的数据复用
        data_sets 参数 用于指定查询的字典；
        tips 参数用于提示用户需要输入的内容；
        error_msg 参数用于在用户输入不符合规范的时候给予提示，并引导用户重新输入；
        success_msg 参数用于在用户输入符合要求的时候给予反馈

        返回 字典对应key的value
        """
        key = input(tips)  # 接受输入内容，tips参数作为输入的提示内容
        while True:
            if key in data_sets.keys():  # 当输入的数字是指定字典中的key时，对应key查询并返回相应的value,并终止循环
                value = data_sets[key]
                print(' {}'.format(value).title() + success_msg)
                break
            else:
                print(error_msg)  # 当输入的数字不是字典中的key时，显示error_msg进行错误提示，并要求用户重新输入
                key = input("\n Let's do it again! " + tips)
        return value

    # TO DO: get user input for city (chicago, new york city, washington).
    city_input = get_data(city_dict,
                          " First, specify a city: 1 for Chicago, 2 for New York City, and 3 for Washington: ",
                          "\n Oops, the City you looked for is NOT available. Please try again.",
                          "! Got it!")

    # TO DO: get user input for month (all, january, february, ... , june)
    month_input = get_data(month_dict,
                           "\n Now, specify a month: 0 for all, 1 for January, 2 for February... and 6 for June: ",
                           " Oops, the Month you just acquired is NOT available. Please try again.",
                           " it is then!")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = get_data(days_of_week_dict,
                         "\n Finally! Specify a day if you like: 0 for all, 1 for Monday, 2 for Tuesday..., "
                         "and 7 for Sunday: ",
                         " O.O! Have you invented a new calender?!",
                         "! Lovely!")

    print('-' * 40)
    return city_input, month_input, day_input


def load_data(city_input, month_input, day_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # city_input, month_input, day_input = get_filters()

    # loading csv according to city_input
    df = pd.read_csv(CITY_DATA[city_input])

    # 将Start Time列转化为datetimelike数据
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # 提取month信息，获得新列'month'
    df['month'] = df['Start Time'].dt.month

    # 直接使用Series的weekday方法提取星期信息.Monday为0，且Series没有isoweekday
    df['day_of_week'] = df['Start Time'].dt.weekday + 1

    # 如果month_input不是all，执行筛选器
    if month_input != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month_input) + 1
        df = df[df['month'] == month]

    # 如果day_input不是all，执行筛选器
    if day_input != 'all':
        days_of_week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days_of_week_list.index(day_input) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, city_input):
    """Displays statistics on the most frequent times of travel."""

    print('\n The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("     The Most Popular Month for", city_input, ":", month_dict[str(popular_month)].title())

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('     Most Popular Day of Week for', city_input, ":", days_of_week_dict[str(popular_day_of_week)].title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('     Most Popular Start Hour for', city_input, ":", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-' * 40)


def station_stats(df, city_input):
    """Displays statistics on the most popular stations and trip."""

    print('\n The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_heated_start = df['Start Station'].mode()[0]
    print("     The most commonly used start station in", city_input, "is:", most_heated_start)

    # TO DO: display most commonly used end station
    most_heated_end = df['End Station'].mode()[0]
    print("     The most commonly used end station in", city_input, "is:", most_heated_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " ---> " + df['End Station']
    most_frequent_trip = df['Trip'].mode()[0]
    print("     The most trip for users in", city_input, "is:", most_frequent_trip)

    print("\n This took %s seconds." % (time.time() - start_time))

    print('-' * 40)


def trip_duration_stats(df, city_input):
    """Displays statistics on the total and average trip duration."""

    print('\n Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print("     The most trip duration for users in", city_input, "is:", total_duration)

    # TO DO: display mean travel time
    average_duration = df['Trip Duration'].mean()
    print("     The average trip duration for users in", city_input, "is:", average_duration)

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city_input):
    """Displays statistics on bikeshare users."""

    print('\n User Stats...\n')
    start_time = time.time()

    # 本部分显示用户类别。为了优化用户体验，同时输出了不同用户类型1的计数和占比
    types_percent = df['User Type'].value_counts(normalize=True, sort=True)
    types_count = df['User Type'].value_counts()
    user_types = pd.DataFrame([types_count, types_percent])
    print("     User types counts and percentage: ", "\n", " ", user_types, "\n")

    # 本部分显示性别计数。为了优化用户体验，同时输出了占比
    if city_input != 'Washington':
        gender_count = df['Gender'].value_counts()
        gender_percent = df['Gender'].value_counts(normalize=True, sort=True)
        gender = pd.DataFrame([gender_count, gender_percent])
        print("     Gender counts and percentage: ", "\n", " ", gender, "\n")
    else:
        pass

    if city_input != 'Washington':
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print("     The earliest birth year in", city_input, "is:", earliest_birth)

        latest_birth = df['Birth Year'].max()
        print("     The most recent birth year in", city_input, "is:", latest_birth)

        most_common_birth = df['Birth Year'].mode()[0]
        print("     The most common birth year for bikeshare users in", city_input, "is:", most_common_birth)
    else:
        pass

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city_input, month_input, day_input = get_filters()
        df = load_data(city_input, month_input, day_input)

        time_stats(df, city_input)
        time.sleep(1.0)  # 每次函数调用之间增加1s的延时，以强化程序逐步执行的印象
        station_stats(df, city_input)
        time.sleep(1.0)  # 每次函数调用之间增加1s的延时，以强化程序逐步执行的印象
        trip_duration_stats(df, city_input)
        time.sleep(1.0)  # 每次函数调用之间增加1s的延时，以强化程序逐步执行的印象
        user_stats(df, city_input)
        time.sleep(1.0)  # 每次函数调用之间增加1s的延时，以强化程序逐步执行的印象

        restart = input('\n 1Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' or 'y':
            break


if __name__ == "__main__":
    main()
