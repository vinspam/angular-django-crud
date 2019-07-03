from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

# class EmployeeAPIview(generics.CreateAPIView):
#     serializer_class = EmployeeSerializer

#     def get_queryset(self):
#         return Employee.objects.all()


class EmployeeAPIview(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        qs = Employee.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(first_name__icontains=query) | Q(email__icontains=query)
            ).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)


class EmployeeRUDview(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"  # instead of pk, can use id
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()


class EmployeeRetrieveview(generics.ListAPIView):
    lookup_field = "companyId"
    serializer_class = EmployeeSerializer

    def get_queryset(self, **kwargs):
        # queryset = Employee.objects.all()
        # queryset = queryset.filter(companyId=companyId)
        companyId = self.request.parser_context["kwargs"]["companyId"]
        return Employee.objects.filter(companyId=companyId)



