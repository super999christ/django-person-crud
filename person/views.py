from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from person.serializers import PersonalInfoSerializer
from person.models import PersonalInfo
import re


def check_field(data):
    """ check field name """
    for key in data.keys():
        if not key in ('first_name', 'last_name', 'birth_date', 'address1', 'address2', 
                        'city', 'county', 'state', 'zipcode', 'email', 'phone'):
            return False
    return True


def check_name(data):
    """ check existence of first name and last name """
    is_firstname = True if 'first_name' in data.keys() and data['first_name'] != None else False
    is_lastname = True if 'last_name' in data.keys() and data['last_name'] != None else False
    return is_firstname + is_lastname == 2


def check_email(data):
    """ check existence """
    return True if 'email' in data.keys() and data['email'] != None else False


def check_phone(data):
    """ check existence"""
    return True if 'phone' in data.keys() and data['phone'] != None else False


def validate_email_address(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    print(email)
    return re.fullmatch(regex, email)


def validate_phone_number(phone):
    regex=re.compile(r'^\+?1?\d{9,15}$')
    return re.fullmatch(regex, phone)
            

# Create your views here.
@api_view(['POST'])
def add_items(request):
    # validating for correct field name
    if not check_field(request.data):
        raise serializers.ValidationError(f'Invalid field.')
    print(request.data)

    # validating for existence of first name and last name, email and phone
    if check_name(request.data) + check_email(request.data) + check_phone(request.data) == 0:
        raise serializers.ValidationError('At least input first and last name or email address or phone number.')
    print(request.data)
    
    # validating for email address
    if 'email' in request.data.keys() and not validate_email_address(request.data['email']):
        raise serializers.ValidationError('Invalid email address')
    print(request.data)
    
    # validating for phone number
    if 'phone' in request.data.keys() and not validate_phone_number(request.data['phone']):
        raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    print(request.data)
    

    item = PersonalInfoSerializer(data=request.data)
  
    # validating for already existing data
    if PersonalInfo.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
    
    # checking for the parameters from the URL
    items = PersonalInfo.objects.all()
  
    # if there is something in items else raise error
    if items:
        data = PersonalInfoSerializer(items, many=True).data
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_items(request, pk):
    # validating for correct field name
    if not check_field(request.data):
        raise serializers.ValidationError(f'Invalid field.')
    
    # validating for email address
    if 'email' in request.data.keys() and not validate_email_address(request.data['email']):
        raise serializers.ValidationError('Invalid email address')
    
    # validating for phone number
    if 'phone' in request.data.keys() and not validate_phone_number(request.data['phone']):
        raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    # update item
    item = PersonalInfo.objects.get(pk=pk)
    data = PersonalInfoSerializer(instance=item, data=request.data)
  
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(PersonalInfo, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
