# from django.shortcuts import render
# from django.http import HttpResponse
import json
from django.contrib.auth.hashers import make_password

from todoproject.response import Response
from . import transformer
from .models import Users

def index(request):
	if request.method == 'GET':
		user = Users.objects.all()
		user = transformer.transform(user)
		return Response.ok(values=user)
	elif request.method == 'POST':
		json_data = json.loads(request.body)

		user = Users()
		user.name = json_data['name']
		user.email = json_data['email']
		user.password = make_password(password=json_data['password'])
		user.save()

		return Response.ok(
			values=transformer.singleTransform(user),
			message="Added!"
		)

def show(request, id):
	if request.method == 'GET':
		user = Users.objects.filter(id=id).first()

		if not user:
			return Response.badRequest(message='Pengguna tidak ditemukan!')

		user = transformer.singleTransform(user)
		return Response.badRequest(values=user)
	elif request.method == 'PUT':
		json_data = json.loads(request.body)

		user = Users.objects.filter(id=id).first()
		if not user:
			return Response.badRequest(message="Pengguna tidak ditemukan")
		user.name = json_data['name']
		user.email = json_data['email']
		user.password = make_password(password=json_data['password'])
		user.save()

		return Response.ok(
			values=transformer.singleTransform(user),
			message="Updated!"
		)
	elif request.method == 'DELETE':
		user = Users.objects.filter(id=id).first()
		if not user:
			return Response.badRequest(message="Pengguna tidak ditemukan")

		user.delete()
		return Response.ok(message="Deleted!")
	else:
		return Response.badRequest(message="Invalid method!")