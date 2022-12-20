from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pickle
from .inference import DF_TRAIN_PATH, PICKLE_PATH
from .tasks import train


ALLOWED_SPECIES = ['Bream', 'Roach', 'Whitefish', 'Parkki', 'Perch', 'Pike', 'Smelt']


def parse_request(request):
    species = request.get('species').capitalize()
    length1 = float(request.get('length1'))
    length2 = float(request.get('length2'))
    length3 = float(request.get('length3'))
    height = float(request.get('height'))
    width = float(request.get('width'))
    if species not in ALLOWED_SPECIES:
        raise Exception('Species must be one of {}'.format(', '.join(ALLOWED_SPECIES)))
    return species, length1, length2, length3, height, width


@api_view(['GET'])
def predict(request):
    try:
        species, length1, length2, length3, height, width = parse_request(request.GET)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    model = pickle.load(open(PICKLE_PATH, 'rb'))
    prediction = model.predict(species, length1, length2, length3, height, width)
    return JsonResponse({'predicted weight': prediction[0],
                         'species': species,
                         'length1': length1,
                         'length2': length2,
                         'length3': length3,
                         'height': height,
                         'width': width
                         })


@api_view(['POST'])
def add(request):
    try:
        species, length1, length2, length3, height, width = parse_request(request.POST)
        weight = int(request.POST.get('weight'))
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    file = open(DF_TRAIN_PATH, 'a')
    file.write(f'{species},{weight},{length1},{length2},{length3},{height},{width}\n')
    file.close()
    return Response('Added to dataset', status=status.HTTP_201_CREATED)


@api_view(['POST'])
def trigger_training(request):
    train()
    return Response('Training complete, model saved', status=status.HTTP_201_CREATED)
