from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from blog.models import Blog
from blog.serializers import BlogSerializer


# Create your views here.


class BlogView(generics.ListCreateAPIView):
	queryset = Blog.objects.all()
	serializer_class = BlogSerializer

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		return JsonResponse(serializer.data, safe=False)
