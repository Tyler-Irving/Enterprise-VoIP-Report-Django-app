from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import View
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import  Response
from .utils.imdatabase import IMDatabase
from rest_framework import status
from .forms import InitialInfoForm, FilterRateCentersForm
from .models import ServiceLocationModel, QueryInfoModel, FilteredRateCentersModel, DisplayModel, NumberStatusModel
from .serializers import ServiceLocationSerializer, NumberStatusSerializer
from .rate_center_info import us_state_abbrev
from io import BytesIO
from pandas import ExcelWriter, DataFrame
import pandas

pandas.set_option('display.max_rows', None)
options = {}
options['strings_to_formulas'] = False
options['strings_to_urls'] = False
db = IMDatabase()

class ServiceLocationViewSet(ModelViewSet):
    queryset = ServiceLocationModel.objects.all().order_by('id')
    serializer_class = ServiceLocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serv_location_info = db.fetchall("""Deleted the SQL query that was here""")
        ServiceLocationModel.objects.all().delete()
        for local in serv_location_info:
            ServiceLocationModel.objects.create(service_location_value=local[0], service_location_description=local[1])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BuildNumberStatusViewSet(ModelViewSet):
    queryset = NumberStatusModel.objects.all().order_by('id')
    serializer_class = NumberStatusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        num_status = [['WK', 'Working'],
                      ['RD', 'Returned'],
                      ['RT', 'Restricted'],
                      ['RE', 'Reserved'],
                      ['QT', 'Quarantined'],
                      ['PT', 'Ported'],
                      ['PD', 'Pending Deactivation'],
                      ['PA', 'Pending Activation'],
                      ['EN', 'Entered'],
                      ['AV', 'Available']]
        NumberStatusModel.objects.all().delete()
        for stat in num_status:
            NumberStatusModel.objects.create(value=stat[0], description=stat[1])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class Home(View):
    def get(self, request):
        QueryInfoModel.objects.filter(user=request.user).delete()
        form = InitialInfoForm()
        return render(request, "ent_voip_home.html", {"form": form})

    def post(self, request):
        form = InitialInfoForm(request.POST)

        if form.is_valid():
            num_status = form.cleaned_data['number_status']
            location = form.cleaned_data['location']
            QueryInfoModel.objects.create(number_status=num_status, location=location, user=request.user)
            rate_centers = db.fetchall("""Deleted the SQL query that was here""")
            FilteredRateCentersModel.objects.all().delete()
            for row in rate_centers:
                if row[1][-2:] == us_state_abbrev[str(location).title()]:
                    FilteredRateCentersModel.objects.create(value=row[0], description=row[1], user=request.user)

            return redirect('enterprise_voip_report/filter_data')

class FilterData(View):
    def get(self, request):
        form = FilterRateCentersForm(request.user)
        return render(request, 'filter_data.html', {'form': form})

    def post(self, request):
        DisplayModel.objects.all().delete()
        form = FilterRateCentersForm(request.user, request.POST)

        if form.is_valid():
            query_info = QueryInfoModel.objects.filter(user=request.user).get()

            if form.cleaned_data["port_in"] == '2':
                    query = db.fetchall(f"""Deleted the SQL query that was here""")

                    for row in query:
                        DisplayModel.objects.create(service_location=f'{row[0]} - {row[1]}',
                                                    rate_center=row[2],
                                                    number_status=row[6],
                                                    phone_number=row[4],
                                                    port_in=row[5],
                                                    act_date=row[7],
                                                    deact_date=row[8],
                                                    returned_date=row[9])

                    query_info.port_in = form.cleaned_data["port_in"]
                    query_info.rate_center = form.cleaned_data["rate_centers"]
                    query_info.save()

            else:
                    query = db.fetchall(f"""Deleted the SQL query that was here""")

                    for row in query:
                        DisplayModel.objects.create(service_location=f'{row[0]} - {row[1]}',
                                                    rate_center=row[2],
                                                    number_status=row[6],
                                                    phone_number=row[4],
                                                    port_in=row[5],
                                                    act_date=row[7],
                                                    deact_date=row[8],
                                                    returned_date=row[9])

                    query_info.port_in = form.cleaned_data["port_in"]
                    query_info.rate_center = form.cleaned_data["rate_centers"]
                    query_info.save()

        results = DisplayModel.objects.all()

        return render(request, 'filter_data.html', {'form': form, 'results': results})


def cms_im_audit_report(request):
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        query_info = QueryInfoModel.objects.filter(user=request.user).get()
        if query_info.port_in == '2':
            query = """Deleted the SQL query that was here""".format(query_info.location, query_info.rate_center, query_info.number_status)

            df = DataFrame(db.fetchall(query))
            df.columns = ['Service Location ID', 'Service Location', 'Rate Center Value',
                          'Rate Center Description', 'Phone Number', 'Port In',
                          'Number Status', 'Activation Date', 'Deactivation Date',
                          'Returned State', 'Returned Date']
            writer = ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer)
            writer.save()
            # Set up the Http response.
            filename = 'IM_Report_for_{}_{}_{}_Numbers.xlsx'.format(query_info.rate_center, query_info.location,
                                                                    query_info.number_status)
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response

        query = """Deleted the SQL query that was here""".format(query_info.location, query_info.rate_center, query_info.number_status, query_info.port_in)

        df = DataFrame(db.fetchall(query))
        df.columns = ['Service Location ID', 'Service Location', 'Rate Center Value',
                      'Rate Center Description', 'Phone Number', 'Port In',
                      'Number Status', 'Activation Date', 'Deactivation Date',
                      'Returned State', 'Returned Date']
        writer = ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()
        # Set up the Http response.
        filename = 'IM_Report_for_{}_{}_{}_Numbers.xlsx'.format(query_info.rate_center, query_info.location, query_info.number_status)
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
