import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_dict = {'1': 'Chicago', '2': 'New York City', '3': 'Washington'}
    month_dict = {'0': 'all', '1': 'january', '2': 'february', '3': 'march', '4': 'april', '5': 'may', '6': 'june'}
    days_of_the_week_dict = {'0': 'all', '1': 'monday', '2': 'tuesday', '3': 'wednesday',
                             '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'}  # 本脚本采用ISO国际标准历法

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
    day_input = get_data(days_of_the_week_dict,
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

    # loading csv according to city_input
    df = pd.read_csv(CITY_DATA[city_input])

    # 将Start Time列转化为datetimelike数据
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # 提取month信息，获得新列'month'
    df['month'] = df['Start Time'].dt.month

    # 直接使用Series的weekday方法提取星期信息.Monday为0，且Series没有isoweekday
    df['day_of_the_week'] = df['Start Time'].dt.weekday + 1

    # 如果month_input不是all，执行筛选器
    if month_input != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month_input) + 1
        df = df[df['month'] == month]

    # 如果day_input不是all，执行筛选器
    if day_input != 'all':
        days_of_the_week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days_of_the_week_list.index(day_input) + 1
        df = df[df['day_of_the_week'] == day]

    return df


city_input, month_input, day_input = get_filters()
df = load_data(city_input, month_input, day_input)
print(df)