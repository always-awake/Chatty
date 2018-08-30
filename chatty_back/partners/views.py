from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from chatty_back.diary.views import check_user


def get_partner(self, partner_id, creator):

    try:
        found_partner = models.Partner.objects.get(id=partner_id, creator=creator)
        return found_partner
    except models.Partner.DoesNotExist:
        return None


class PartnerList(APIView):

    @method_decorator(check_user())
    def get(selg, request, user, format=None):

        partners = models.Partner.objects.filter(creator=user)

        serializer = serializers.PartnerListSerializer(partners, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Partner(APIView):

    @method_decorator(check_user())
    def post(self, request, user, format=None):

        new_partner_name = request.data.get('name', None)
        
        try:
            found_partner = models.Partner.objects.get(name=new_partner_name, creator=user)
            
        except models.Partner.DoesNotExist:
        
            serializer = serializers.CreatePartnerSerializer(data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save(creator=user)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                
            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PartnerProfile(APIView):

    #@method_decorator(check_user())
    def get(self, request, partner_id, format=None):

        #found_partner = get_partner(self, partner_id)

        found_partner = models.Partner.objects.get(id=partner_id)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else: 

            serializer = serializers.PartnerProfileSerializer(found_partner)

            return Response(data=serializer.data, status=status.HTTP_200_OK)


    @method_decorator(check_user())
    def put(self, request, user, partner_id, format=None):

        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.PartnerProfileSerializer(
                found_partner, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            else:
                
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePartner(APIView):
    
    @method_decorator(check_user())
    def delete(self, request, user, partner_id, format=None):
        
        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            found_partner.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


class SetPartner(APIView):

    @method_decorator(check_user())
    def put(self, request, user, partner_id, format=None):

        found_partner = get_partner(self, partner_id, user)
        
        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            user.partner = found_partner

            user.save()

            return Response(status=status.HTTP_200_OK)


# Main 화면에 있는 Partner 부분(Main 화면의 module화를 위한 API)
class MainPartner(APIView):

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.MainPartnerSerializer(found_partner)

            return Response(data=serializer.data, status=status.HTTP_200_OK)