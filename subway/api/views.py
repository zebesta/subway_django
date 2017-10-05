import requests
from google.transit import gtfs_realtime_pb2
from django.shortcuts import render
from django.http import JsonResponse

from subway.secrets import MTA_API_KEY


def test(request):
    test_data = {'hello': 'world'}
    return JsonResponse(test_data)


def ltrain(request):
    feed = gtfs_realtime_pb2.FeedMessage()
    mta_base_url = "http://datamine.mta.info/mta_esi.php"
    # Feed ID 2 is the L train feed id
    # TODO: Make this modular so that feed id is passed via resusts or whatevs
    payload = {'key': MTA_API_KEY, 'feed_id': '2'}
    response = requests.get(mta_base_url, params=payload)
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            print(entity.trip_update)
            return JsonResponse(entity.trip_update, safe=False)
