import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins
import numpy as np


# Function to visualize on map the route
def route_and_stop_visualization(stops, shapes):
    ### We create a map with a view on the zone we are interested in
    map = folium.Map(location=[43.9941, 10.2301], tiles="OpenStreetMap", zoom_start=9)
    
    ### We Circle The Stops belonging to the route
    for point in stops.geometry:
        folium.CircleMarker((point.xy[1][0],point.xy[0][0]), color="blue", weight=0.5, opacity=1).add_to(map)
    
    ### The lists of shapes have duplicates because each shape describe the trip for both direction
    ### so for drawing purposes we want to select only one of the way. Then we draw the shapes
    shape_id_list_duplicates = shapes["shape_id"].to_list()
    shape_id_list = list(set(shape_id_list_duplicates))
    
    for shape_id in shape_id_list:
        shape_df_list = []
        shape_to_draw = shapes.loc[(shapes['shape_id'] == shape_id)]
        shape_to_draw.drop_duplicates(subset='shape_pt_sequence', keep="first",inplace=True)
        for point in shape_to_draw.geometry:
            shape_df_list.append((point.xy[1][0],point.xy[0][0]))
        folium.PolyLine(shape_df_list, color="red", weight=1.5, opacity=1).add_to(map)
    
    return map

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def calendar_2022():
    array_calendar=['20220103','20220110','20220117','20220124','20220131',
                    '20220207','20220214','20220221','20220228','20220307',
                    '20220314','20220321','20220328','20220404','20220411',
                    '20220418','20220425','20220502','20220509','20220516',
                    '20220523','20220530','20220606','20220613','20220620',
                    '20220627','20220704','20220711','20220718','20220725',
                    '20220801','20220808','20220815','20220822','20220829',
                    '20220905','20220912','20220919','20220926','20221003',
                    '20221010','20221017','20221024','20221031','20221107',
                    '20221114','20221121','20221128','20221205','20221212',
                    '20221219','20221226','20230102']

    return array_calendar

def stop_sequence_statistics(df_analytics):
    # Basic statistics on the number of stops
    print("Mean of stop_sequence : " + str(df_analytics.stop_sequence.mean()))
    print('-' * 50)
    print("Median of stop_sequence : " + str(df_analytics.stop_sequence.median()))
    print('-' * 50)
    print("Standard Deviation of stop_sequence : " + str(df_analytics.stop_sequence.std()))
    print('-' * 50)
    print("Skewness of stop_sequence : " + str(df_analytics.stop_sequence.skew()))
    # Distribution of number of stops in the dataset
    plt.title('Distribution of the no. stops in the dataset')
    plt.hist(df_analytics.stop_sequence)
    plt.xlabel('No. Stops')
    plt.ylabel('Frequency')
    plt.show()

def boxplot_stop_sequence(df_analytics):
    plt.boxplot(df_analytics.stop_sequence)
    plt.title('No. stops per trip')
    plt.show()

def boxplot_time(df_analytics):
    plt.boxplot(df_analytics.time_diff)
    plt.title('Time Diff')
    plt.ylabel("seconds (s)")
    plt.show()

def boxplot_distance(df_analytics):
    plt.boxplot(df_analytics.dist_diff)
    plt.title('Distance Diff')
    plt.ylabel("Kilometers (km)")
    plt.show()

def boxplot_speed(df_analytics):
    plt.boxplot(df_analytics.speed)
    plt.title('Speed')
    plt.ylabel("Kilometer per hour (km/h)")
    plt.show()

def speed_statistics(df_analytics):
    print("Mean of speed : " + str(df_analytics.speed.mean()))
    print('-' * 50)
    print("Standard Deviation of speed : " + str(df_analytics.speed.std()))
    print('-' * 50)
    print("Skewness of speed : " + str(df_analytics.speed.skew()))
    print('-' * 50)
    # Distribution of number of stops in the dataset
    plt.title('Distribution of speed between stops')
    plt.hist(df_analytics.speed)
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Frequency')
    plt.show()

def distance_statistics(df_analytics):
    # Basic statistics on the number of stops
    print("Mean of distance difference : " + str(df_analytics.dist_diff.mean()))
    print('-' * 50)
    print("Standard Deviation of distance difference : " + str(df_analytics.dist_diff.std()))
    print('-' * 50)
    print("Skewness of distance difference : " + str(df_analytics.dist_diff.skew()))
    print('-' * 50)
    # Distribution of number of stops in the dataset
    plt.title('Distribution of distance between stops')
    plt.hist(df_analytics.dist_diff)
    plt.xlabel('Distance Difference (km)')
    plt.ylabel('Frequency')
    plt.show()

def time_statistics(df_analytics):
    # Basic statistics on the number of stops
    print("Mean of time difference : " + str(df_analytics.time_diff.mean()))
    print('-' * 50)
    print("Standard Deviation of time difference : " + str(df_analytics.time_diff.std()))
    print('-' * 50)
    print("Skewness of time difference : " + str(df_analytics.time_diff.skew()))
    print('-' * 50)
    # Distribution of number of stops in the dataset
    plt.title('Distribution of time between stops')
    plt.hist(df_analytics.time_diff)
    plt.xlabel('Time Difference (s)')
    plt.ylabel('Frequency')
    plt.show()

def plot_number_stops(df_analytics):
    max_stop = df_analytics['stop_sequence'].max()
    min_stop = df_analytics['stop_sequence'].min()
    dataset_settings = {'last_stop_sequence': range(min_stop, max_stop + 2) , 'value': 0}
    result = pd.DataFrame(data = dataset_settings).set_index('last_stop_sequence')
    df = df_analytics.groupby(['trip_id']).max('stop_sequence').reset_index()
    for index, row  in df.iterrows():
        result.loc[row['stop_sequence'] ,'value'] = result.loc[row['stop_sequence'] ,'value'] + 1
    result = result.reset_index()
    print("For each value:")
    print(result)
    print(50 * '-')
    result.plot(x='last_stop_sequence', y= 'value')
    return result 

def aggregated_number_stops(result, input_value):
    max_value = result['last_stop_sequence'].max()
    df = result.groupby(pd.cut(result['last_stop_sequence'], np.arange(0, max_value + 5, input_value)))['value'].sum()
    df = df.reset_index()
    print(df.head(max_value))


def scatter_speed_distance(df_analytics):
    plt.scatter(df_analytics['speed'], df_analytics['dist_diff'])
    plt.title('Correlation between Speed and Distance')
    plt.xlabel('Speed')
    plt.ylabel('Distance Difference Between Stops')
    plt.show()

def scatter_time_distance(df_analytics):
    plt.scatter( df_analytics['dist_diff'],df_analytics['time_diff'])
    plt.ylabel('Time Difference')
    plt.xlabel('Distance Difference Between Stops')
    plt.title('Correlation between Time and Distance')
    plt.show()

def scatter_time_speed(df_analytics):
    plt.scatter(df_analytics['speed'],df_analytics['time_diff'])
    plt.ylabel('Time Difference between Stops')
    plt.xlabel('Speed')
    plt.title('Correlation between Time and Speed')
    plt.show()

def calculate_list_of_range_times(value):
    list_of_ammisible_value = [1,2,3,4,6,8,12]
    if value not in list_of_ammisible_value:
        return "Error the value is not in (1,2,3,4,6,8,12)"
    list_of_range_time = []
    x = np.arange(0,26,value).tolist()
    for i in range(len(x)):
        array_to_append = []
        if x[i] < 10 and x[i+1] < 10:
            array_to_append = ['0' + str(x[i]) + ':00:00' , '0' + str(x[i+1]) + ':00:00']
        elif x[i] < 10 and x[i+1] >= 10:
            array_to_append = ['0' + str(x[i]) + ':00:00' , str(x[i+1]) + ':00:00']
        elif (i+1) >= len(x):
            continue
        else:
            array_to_append = [ str(x[i]) + ':00:00' , str(x[i+1]) + ':00:00']
        list_of_range_time.append(array_to_append)
    return list_of_range_time


def period_stop_based_data(df_analytics,list_of_range_time):
    # Needed information to process
    trip_ids = df_analytics['trip_id'].drop_duplicates().to_list()
    # counters
    counter = [0] * len(list_of_range_time)
    # Creation of resulting dataframe
    result = pd.DataFrame(columns=['time_period_index', 'time_period', 'stop_sequence', 'total_trains'])
    for i in range(len(counter)):
        for j in range(2,df_analytics['stop_sequence'].max()+1):
            new_row = {'time_period_index': i , 'time_period': list_of_range_time[i] , 'stop_sequence': j, 'total_trains':0}
            result = pd.concat([result, pd.DataFrame([new_row])], ignore_index=True)
            
    #Calculations (O(n*m))
    for key in trip_ids:
        for i in range(len(list_of_range_time)):
            #the subset for our trip
            data = df_analytics.loc[(df_analytics['trip_id'] == key)]   
            #Row of first stop and row of last stop
            start_row = data.loc[data['stop_sequence'] == 1]
            end_row = data.loc[data['stop_sequence'] == data['stop_sequence'].max()]

            # If trip start during range or trip is traveling during range or trip arrives during range
            if (
                (start_row['departure_time'].item() >= list_of_range_time[i][0]) and 
                (start_row['departure_time'].item() <= list_of_range_time[i][1])
            ) or (
                (start_row['departure_time'].item() <= list_of_range_time[i][0]) and
                (end_row['arrival_time'].item() >= list_of_range_time[i][1])
            ) or (
                (end_row['arrival_time'].item() >= list_of_range_time[i][0]) and
                (end_row['arrival_time'].item() <= list_of_range_time[i][1])
            ):
                counter[i] += 1
                result.loc[(result['time_period_index'] == i) & (result['stop_sequence'] == data['stop_sequence'].max()),'total_trains'] += 1            
    
    for i in range(len(counter)):
        print('the number of trains in transit during ' + str(list_of_range_time[i]) + ' is ' + str(counter[i]))

    print(counter)
    return result