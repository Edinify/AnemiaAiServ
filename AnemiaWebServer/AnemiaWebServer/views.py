from django.http import JsonResponse
from .models import Test
from .serializers import TestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer
from .models import Post
# geini Ai and lang chain ================

import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyBS1SuSV0kBHIW64EujGA-sWM4PSmnU_X4"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')


plt.figure()
plt.title('Colour Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
colors = ('r','g','b')

hist_data = []
color_count_array_r = []
color_count_array_g = []
color_count_array_b = []
# max_number_r, max_number_g, max_number_b =[]
bin_Data = []

def Check_image(file):
    print(file,"asa")
    img = cv.imread(f'../{file['image']}')
    os.remove(f'../{file['image']}')
    blank = np.zeros(img.shape[:2], dtype='uint8')
    mask = cv.circle(blank, (img.shape[1]//2,img.shape[0]//2), 100, 255, -1)
    for i, col in enumerate(colors):
            hist = cv.calcHist([img], [i], mask, [256], [0, 256])
            hist_data.append(hist)
        # print(hist_data)
        
    for i, col in enumerate(colors):
        for bin_value, count in enumerate(hist_data[i]):
            if col == 'r':
                color_count_array_r.append(count[0])
            elif col == 'g':
                color_count_array_g.append(count[0])
            elif col == 'b':
                color_count_array_b.append(count[0])
            bin_Data.append(bin_value)
    sclera_color = f'({max(color_count_array_r)}, {max(color_count_array_g)}, {max(color_count_array_b)})'
    promt = (f'Typical Healthy Sclera: A healthy sclera is typically very close to white,  Small deviations from these values arent unusual but are generally still in the high range.Anemic Sclera: An anemic sclera might show a pale blue or pale pink tint. The RGB values might slightly decrease in intensity, particularly in the blue channel, or increase in the red channel, indicating paleness or a bluish tint respectively. this is a RGB colors: {sclera_color} please shortly explain if this person only has anemia or not okay? ')

    response = model.generate_content(promt)
    print(response.text)
    return response.text
    
    # for i,col in enumerate(colors):
    #         hist = cv.calcHist([img], [i], mask, [256], [0,256])
    # plt.plot(hist, color=col)
    # plt.xlim([0,256])

    # sds

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        
        # print(posts_serializer.data)
        if posts_serializer.is_valid():
            # 
            posts_serializer.save()
            print(posts_serializer.data)
            AiRes = Check_image(posts_serializer.data)
            return Response(AiRes, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
@api_view(['GET', 'POST'])
def test_serializers(request):

    if request.method == 'GET':
        test = Test.objects.all()
        serializer =  TestSerializer(test, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        serializer = TestSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(["GET", 'PUT','DELETE'])
def test_details(request,id):
 
    try:
       test =  Test.objects.get(pk=id)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TestSerializer(test)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = TestSerializer(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

