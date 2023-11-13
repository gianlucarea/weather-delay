import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins
import numpy as np
import seaborn as sns
import gtfs_kit as gk

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

def mappaloccodice():
    mappa_location_codice = {
                  0:'S06500_1',
                  1:'S06501_1',
                  2:'S06400_1',
                  3:'S06401_1',
                  4:'S06402_1',
                  5:'S06404_1',
                  6:'S06313_1',
                  7:'S06312_1',
                  8:'S06310_1',
                  9:'S06309_1',
                  10:'S06308_1',
                  11:'S06306_1',
                  12:'S06304_1',
                  13:'S06303_1',
                  14:'S06302_1',
                  15:'S06301_1',
                  16:'S06300_1',
                  17:'S06322_1',
                  18:'S06323_1',
                  19:'S06324_1',
                  20:'S06325_1',
                  21:'S06227_1',
                  22:'S06226_1',
                  23:'S06225_1',
                  24:'S06224_1',
                  25:'S06223_1',
                  26:'S06222_1',
                  27:'S06013_1'}
    return mappa_location_codice


def hours_of_the_day():
    hours = ["00","01","02","03","04","05","06","07",
             "08","09","10","11","12","13","14","15",
             "16","17","18","19","20","21","22","23"]
    return hours
        
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

def dataset_for_scatter(stop_times):
    df_analytics = pd.DataFrame(columns=['time', 'distance', 'speed'])
    list_of_trip_id = list(dict.fromkeys(stop_times['trip_id'].to_list()))
    for trip_id in list_of_trip_id:
        df = stop_times.loc[(stop_times['trip_id'] == trip_id)];
        time = df['time_diff'].sum()
        distance = df['dist_diff'].sum()
        speed = (df['speed'].sum())/(df['stop_sequence'].max() - 1)
        new_row = {'time': time, 'distance':distance, 'speed':speed}
        df_analytics = pd.concat([df_analytics, pd.DataFrame([new_row])], ignore_index=True)
    return df_analytics
    
def dataset_for_scatter_year(stop_times_year):
    df_analytics = pd.DataFrame(columns=['time', 'distance', 'speed'])
    list_of_trip_id = list(dict.fromkeys(stop_times_year['trip_id'].to_list()))
    for trip_id in list_of_trip_id:
        df = stop_times_year.loc[(stop_times_year['trip_id'] == trip_id)];
        time = round(df['time_diff'].sum(),1)
        distance = df['dist_diff'].sum()
        speed =  round(distance/time)  # (df['speed'].sum())/(df['stop_sequence'].max() - 1)
        new_row = {'time': time, 'distance':distance, 'speed':speed}
        df_analytics = pd.concat([df_analytics, pd.DataFrame([new_row])], ignore_index=True)
    return df_analytics
    
def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    total = (int(h) * 3600)+ (int(m) * 60) + int(s)
    return total

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

def calendar_2021():
    array_calendar=['20210104','20210111','20210118','20210125','20210201',
                    '20210208','20210215','20210222','20210301','20210308',
                    '20210315','20210322','20210329','20210405','20210412',
                    '20210419','20210426','20210503','20210510','20210517',
                    '20210524','20210531','20210607','20210614','20210621',
                    '20210628','20210705','20210712','20210719','20210726',
                    '20210802','20210809','20210816','20210823','20210830',
                    '20210906','20210913','20210920','20210927','20211004',
                    '20211011','20211018','20211025','20211101','20211108',
                    '20211115','20211122','20211129','20211206','20211213',
                    '20211220','20211227','20220103']

    return array_calendar



def calculate_stops(df_analytics):
    max_stop = df_analytics['stop_sequence'].max()
    min_stop = df_analytics['stop_sequence'].min()
    dataset_settings = {'last_stop_sequence': range(min_stop, max_stop + 2) , 'value': 0}
    result = pd.DataFrame(data = dataset_settings).set_index('last_stop_sequence')
    df = df_analytics.groupby(['trip_id']).max('stop_sequence').reset_index()
    for index, row  in df.iterrows():
        result.loc[row['stop_sequence'] ,'value'] = result.loc[row['stop_sequence'] ,'value'] + 1
    result = result.reset_index()
    return result 

def aggregated_number_stops(result, input_value):
    max_value = result['last_stop_sequence'].max()
    df = result.groupby(pd.cut(result['last_stop_sequence'], np.arange(0, max_value + 5, input_value)))['value'].sum()
    df = df.reset_index()
    print(df.head(max_value))


def scatter_speed_distance(df_analytics):
    plt.scatter(df_analytics['distance'],df_analytics['speed'] )
    plt.title('Correlation between Speed and Distance')
    plt.ylabel('Average Speed')
    plt.xlabel('Distance Difference Between Stops')
    #plt.savefig('scatter_speed_distance_plot.png')
    plt.show()

def scatter_time_distance(df_analytics):
    plt.scatter( df_analytics['time'],df_analytics['distance'])
    plt.xlabel('Time Difference')
    plt.ylabel('Distance Difference Between Stops')
    plt.title('Correlation between Time and Distance')
    #plt.savefig('scatter_time_distance_plot.png')
    plt.show()

def scatter_time_speed(df_analytics):
    plt.scatter(df_analytics['time'],df_analytics['speed'])
    plt.xlabel('Time Difference between Stops')
    plt.ylabel('Average Speed')
    plt.title('Correlation between Time and Speed')
    #plt.savefig('scatter_time_speed_plot.png')
    plt.show()
    
def correlogram_time_distance_speed(df_analytics):
    sns.pairplot(df_analytics)
    plt.savefig('../images/correlation_speed_time_distance.png')
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


def select_year_df(start,end):
    #Read entire Dataset
    feed = gk.feed.read_feed('../processed_files/preprocessing_gtfs_static.zip',dist_units="km")
    routes = gk.routes.get_routes(feed)
    stop_times = feed.get_stop_times()
    trips = feed.get_trips()
    stops = feed.get_stops()
    shapes = feed.shapes
    calendar_dates = feed.calendar_dates
    calendar = feed.calendar
    ## Collecting all service date of trips on those days
    year_calendar_dates = calendar_dates.loc[(calendar_dates['date'] >= start) & 
                                    (calendar_dates['date'] <= end) ]
    
    # Removing data outside the selected year 
    ## Creating new calendar and collect service date from 
    ## previous new calendar_dates with drop duplicates
    year_calendar = calendar.iloc[0:0]
    service_id_list = list(dict.fromkeys(year_calendar_dates['service_id']))

    for service_id in service_id_list:
        row  = calendar.loc[calendar['service_id'] == service_id]
        year_calendar = pd.concat([year_calendar, row],
                          ignore_index = True)

    ## Creating new trips dataframe and collect trips using the list of service id
    year_trips = trips.iloc[0:0]

    for service_id in service_id_list:
        row  = trips.loc[trips['service_id'] == service_id]
        year_trips = pd.concat([year_trips, row],
                          ignore_index = True)

    ## Creating list of shapes_id,route_id,trips_id from sw_trips
    route_id_list = list(dict.fromkeys(year_trips['route_id']))
    shape_id_list = list(dict.fromkeys(year_trips['shape_id']))
    trip_id_list = list(dict.fromkeys(year_trips['trip_id']))

    ## Creating new route dataframe
    year_routes = routes.iloc[0:0]

    for route_id in route_id_list:
        row = routes.loc[routes['route_id']==route_id]
        year_routes = pd.concat([year_routes,row],ignore_index=True)

    ## Creating new shape dataframe
    year_shapes = shapes.iloc[0:0]

    for shape_id in shape_id_list:
        row = shapes.loc[shapes['shape_id']==shape_id]
        year_shapes = pd.concat([year_shapes, row],ignore_index = True)

    ## Creating new stop_times dataframe
    year_stop_times = stop_times.iloc[0:0]

    for trip_id in trip_id_list:
        row = stop_times.loc[stop_times['trip_id'] == trip_id]
        year_stop_times = pd.concat([year_stop_times,row],ignore_index = True)
    stop_id_list = list(dict.fromkeys(year_stop_times['stop_id']))

    ## Creating new stop dataframe, should be equal at this point 
    ## but we do it for safe reasons
    year_stops = stops.iloc[0:0]

    for stop_id in stop_id_list:
        row = stops.loc[stops['stop_id']==stop_id]
        year_stops = pd.concat([year_stops,row],ignore_index = True)
    
    # Join the dataset for easy at use
    year_analytics = year_trips
    year_analytics = pd.merge(year_analytics, year_calendar_dates, on=['service_id','service_id'])
    year_analytics = pd.merge(year_analytics, year_stop_times, on=['trip_id','trip_id'])
    year_analytics = year_analytics.drop(['trip_headsign','direction_id','shape_id',
                                     'arrival_time', 'departure_time','shape_dist_traveled',
                                     'time_diff', 'speed', 'dist_diff','route_id'
                                     ], axis='columns')
    
    return year_analytics

def regressor_metrics(y_test, y_pred, regressor, statistics):
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    display = pd.DataFrame(columns=["regressor", "mse", "rmse", "mae", "r2"])
    
    new_row = {'regressor': regressor,'mse': mse,'rmse': rmse,'mae': mae,'r2': r2}
    
    display = pd.concat([display, pd.DataFrame([new_row])], ignore_index=True)
    print(display.head())
    del display
    statistics = pd.concat([statistics, pd.DataFrame([new_row])], ignore_index=True)
    return statistics

    
def period_stop_based_data(df_analytics,list_of_range_time):
    # Needed information to process
    trip_ids = df_analytics['trip_id'].drop_duplicates().to_list()
    # counters
    counter = [0] * len(list_of_range_time)
    # Creation of resulting dataframe
    result = pd.DataFrame(columns=['time_period_index', 'time_period', 'stop_sequence', 'total_trains'])
    for i in range(len(counter)):
        for j in range(2,df_analytics['stop_sequence'].max()+1):
            new_row = {'time_period_index': i , 'time_period': list_of_range_time[i] ,
                       'stop_sequence': j, 'total_trains':0}
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
                result.loc[(result['time_period_index'] == i) & 
                           (result['stop_sequence'] == data['stop_sequence'].max()),
                           'total_trains'] += 1            
    
    for i in range(len(counter)):
        print('the number of trains in transit during ' + 
              str(list_of_range_time[i]) + ' is ' + str(counter[i]))

    print(counter)
    return result

def get_lista_fermate():
    lista_fermate = ['PISA CENTRALE','PISA SAN ROSSORE',
                     'S.GIULIANO TERME','RIGOLI','RIPAFRATTA',
                     'LUCCA','S. PIETRO A VICO',
                     'PONTE A MORIANO','DIECIMO - PESCAGLIA',
                     'BORGO A MOZZANO','BAGNI DI LUCCA','GHIVIZZANO - COREGLIA',
                     'FORNACI DI BARGA','BARGA GALLICANO','CASTELVECCHIO PASCOLI',
                     'FOSCIANDORA - CESERANA','CASTELNUOVO DI GARFAGNANA',
                     'VILLETTA S. ROMANO','POGGIO - CAREGGINE - VAGLI',
                     'CAMPORGIANO','PIAZZA AL SERCHIO','MINUCCIANO - PIEVE - CASOLA',
                     'EQUI TERME','MONZONE-M.DEI BANCHI-ISOLANO','GRAGNOLA',
                     'FIVIZZANO - GASSANO','FIVIZZANO ROMETTA - SOLIERA','AULLA LUNIGIANA']
    return lista_fermate

def get_nome_codice_loc():
    mappa_location_codice = {
                  'PISA CENTRALE':'S06500_1',
                  'PISA SAN ROSSORE':'S06501_1',
                  'S.GIULIANO TERME':'S06400_1',
                  'RIGOLI':'S06401_1',
                  'RIPAFRATTA':'S06402_1',
                  'LUCCA':'S06404_1',
                  'S. PIETRO A VICO':'S06313_1',
                  'PONTE A MORIANO':'S06312_1',
                  'DIECIMO - PESCAGLIA':'S06310_1',
                  'BORGO A MOZZANO':'S06309_1',
                  'BAGNI DI LUCCA':'S06308_1',
                  'GHIVIZZANO - COREGLIA':'S06306_1',
                  'FORNACI DI BARGA':'S06304_1',
                  'BARGA GALLICANO':'S06303_1',
                  'CASTELVECCHIO PASCOLI':'S06302_1',
                  'FOSCIANDORA - CESERANA':'S06301_1',
                  'CASTELNUOVO DI GARFAGNANA':'S06300_1',
                  'VILLETTA S. ROMANO':'S06322_1',
                  'POGGIO - CAREGGINE - VAGLI':'S06323_1',
                  'CAMPORGIANO':'S06324_1',
                  'PIAZZA AL SERCHIO':'S06325_1',
                  'MINUCCIANO - PIEVE - CASOLA':'S06227_1',
                  'EQUI TERME':'S06226_1',
                  'MONZONE-M.DEI BANCHI-ISOLANO':  'S06225_1',
                  'GRAGNOLA':'S06224_1',
                  'FIVIZZANO - GASSANO':'S06223_1',
                  'FIVIZZANO ROMETTA - SOLIERA':'S06222_1',
                  'AULLA LUNIGIANA':'S06013_1'}
    return mappa_location_codice