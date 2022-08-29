from rest_framework import serializers
from person.models import PersonalInfo


class PersonalInfoSerializer(serializers.ModelSerializer):
    """
    Serializer of PersonalInfo model
    """
    class Meta:
        model = PersonalInfo
        fields = ('first_name', 'last_name', 'birth_date', 'address1', 'address2', 
                  'city', 'county', 'state', 'zipcode', 'email', 'phone')
