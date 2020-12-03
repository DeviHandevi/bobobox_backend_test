from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Index Page
@api_view(['GET'])
def index(request):
	project_info = {
		'project_name': 'Bobobox Backend Engineer Test',
		'author': 'Devi Handevi',
  }
	return Response(project_info)
  