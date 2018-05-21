import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from django.shortcuts import render
from django.http import JsonResponse

from subway.secrets import MTA_API_KEY
MTA_BASE_URL = "http://datamine.mta.info/mta_esi.php"

A_TRAIN_FEED_ID = "26"
G_TRAIN_FEED_ID = "31"

A_NOSTRAND_MANHATTAN_BOUND_STATION_ID = "A46N"
A_NOSTRAND_QUEENS_BOUND_STATION_ID = "A46S"

G_BEDFORD_NOSTRAND_QUEENS_BOUND_STATION_ID = "G33N"
G_BEDFORD_NOSTRAND_CHURCH_AVE_BOUND_STATION_ID = "G33S"

def test(request):
    test_data = {'hello': 'world'}
    return JsonResponse(test_data)

def arrival_time_lookup(train_data, station):
    arrival_times = []
    if(train_data.get('entity', False) != False):
        for trains in train_data['entity']: # trains are dictionaries
            if trains.get('trip_update', False) != False:
                unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip and stop_time_update
                unique_arrival_times = unique_train_schedule['stop_time_update'] # arrival_times is a list of arrivals
                for scheduled_arrivals in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                    if scheduled_arrivals.get('stop_id', False) == station:
                        time_data = scheduled_arrivals['arrival']
                        unique_time = time_data['time']
                        if unique_time != None:
                            arrival_times.append(unique_time)
    return arrival_times

def train_query(feed_id, station_id):
    feed = gtfs_realtime_pb2.FeedMessage()
    # TODO: Make this modular so that feed id is passed via requests or whatevs
    train_payload = {'key': MTA_API_KEY, 'feed_id': feed_id}
    response = requests.get(MTA_BASE_URL, params=train_payload)
    feed.ParseFromString(response.content)
    subway_feed = protobuf_to_dict(feed)
    feed.ParseFromString(response.content)
    subway_feed = protobuf_to_dict(feed)
    train_arrival_times = arrival_time_lookup(subway_feed, A_NOSTRAND_MANHATTAN_BOUND_STATION_ID)
    return train_arrival_times

def seconds_to_datetime(seconds):
    return datetime.fromtimestamp(seconds)

def train(request):
    a_train_arrivals = train_query(A_TRAIN_FEED_ID, A_NOSTRAND_MANHATTAN_BOUND_STATION_ID)
    # g_train_arrivals = train_query(G_TRAIN_FEED_ID, G_BEDFORD_NOSTRAND_QUEENS_BOUND_STATION_ID)
    resp = {
        'a': [seconds_to_datetime(a) for a in a_train_arrivals],
        # 'g': [seconds_to_datetime(g) for g in g_train_arrivals],
    }

    return JsonResponse(resp, safe=False)
