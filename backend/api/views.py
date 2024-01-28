from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserSerializer, ProfileSerializer, ItemsSerializer, toSellSerializer, PurchasedSerializer, LostSerializer, SoldSerializer
from .models import Items, Lost, Purchased, toSell, Sold, User
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from .validators import custom_validation, validate_id, validate_password
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['group'] = user.groups.first().name
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/admin',
        '/api/token',
        '/api/token/refresh',
        '/api/userAll',
        '/api/register',
        '/api/user',
        '/api/profile',
        '/api/updateProfile',
        '/api/items',
        '/api/itemsAll',
        '/api/toSell',
        '/api/purchased',
        '/api/sold',
        '/api/lost',
        '/api/lostAll',
        '/api/toSellAll',
        '/api/addItem',
        '/api/addToSell',
        '/api/addSold',
        '/api/addLost',
        '/api/remToSell',
        '/api/remItem',
        '/api/remLost',
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserAll(request):
    users = User.objects.all();
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItems(request):
    user = request.user
    items = Items.objects.filter(user=user)
    serializer = ItemsSerializer(items, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItemsAll(request):
    items = Items.objects.all()
    serializer = ItemsSerializer(items, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLost(request):
    user = request.user
    lost = Lost.objects.filter(user=user)
    serializer = LostSerializer(lost, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSold(request):
    user = request.user
    sold = Sold.objects.filter(user = user)
    serializer = SoldSerializer(sold, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def getLostAll(request):
    lost = Lost.objects.all()
    serializer = LostSerializer(lost, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getToSell(request):
    user = request.user
    tosell = toSell.objects.filter(user=user)
    serializer = toSellSerializer(tosell, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getToSellAll(request):
    tosell = toSell.objects.all()
    serializer = toSellSerializer(tosell, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPurchased(request):
    user = request.user
    purchased = Purchased.objects.filter(user=user)
    serializer = PurchasedSerializer(purchased, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSold(request):
    user = request.user
    sold = Sold.objects.filter(user = user)
    serializer = SoldSerializer(sold, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addSold(request):
    clean_data = request.data
    request.user.sold_set.create(item_id = clean_data['item_id'], price = clean_data['price'], sold_to = clean_data['sold_to'])
    purchased = User.objects.get(id = clean_data['sold_to']).purchased_set.create(item_id = clean_data['item_id'], price = clean_data['price'], purchased_from = request.user.id)
    item = request.user.items_set.get(id = clean_data['item_id'])
    request.user.items_set.get(id = clean_data['item_id']).delete()
    item2 = User.objects.get(id = clean_data['sold_to']).items_set.create(id = item.id, name = item.name, description = item.description, image = item.image)
    toSell.objects.get(item_id = clean_data['item_id']).delete()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addToSell(request):
    data = request.data
    request.user.tosell_set.create(item_id = data['item_id'], price = data['price'])
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLost(request):
    clean_data = request.data
    request.user.lost_set.create(item_id = clean_data['item_id'], description = clean_data['description'])
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addItem(request):
    clean_data = request.data
    image = request.FILES.get('image')
    if image:
        item = request.user.items_set.create(
            name=clean_data['name'],
            description=clean_data['description'],
            image=image
        )
    else:
        item = request.user.items_set.create(
            name=clean_data['name'],
            description=clean_data['description']
        )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    data = request.data
    user.profile.name = data['name']
    user.profile.dob = data['dob']
    user.profile.hostel = data['hostel']
    user.profile.branch = data['branch']
    image = request.FILES.get('image')
    if image:
        user.profile.image = image
    user.profile.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remLost(request):
    clean_data = request.data
    request.user.lost_set.filter(item_id = clean_data['item_id']).delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remToSell(request):
    clean_data = request.data
    request.user.tosell_set.filter(item_id = clean_data['item_id']).delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remItem(request):
    clean_data = request.data
    request.user.items_set.filter(id = clean_data['item_id']).delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def UserRegister(request):
    clean_data = custom_validation(request.data)
    serializer = UserRegisterSerializer(data = clean_data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(status.HTTP_400_BAD_REQUEST)

# class UserView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response({'user':serializer.data}, status=status.HTTP_200_OK)