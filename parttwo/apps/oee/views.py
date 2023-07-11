import logging
import pytz
from datetime import datetime
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.oee.models import DashboardProcess
from utils import json 
logger = logging.getLogger( __name__ )

now = datetime.now(pytz.timezone('UTC'))
current_date = now.date()
current_time = now.time()

class MyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            params = request.query_params
            if 'machine' in params:
                machine_list = [params.get('machine')]
            else:
                machine_list = list(DashboardProcess.objects.values_list('cam_name', flat=True).distinct())

            q = Q()
            if 'start_date' in params and 'end_date' in params:
                strt_date = params.get('start_date')
                end_date = params.get('end_date')
                date = True
                q = Q(start_time__gte=strt_date) & Q(end_time__lte=end_date)
            # if 'oee_thrs' in params:
            #     oee_thers = int(params.get('oee_thrs'))
            # else:
            #     oee_thers = 0
            thrhold_list = []

            Process = DashboardProcess.objects

            for machine in machine_list:
                # if date:
                downtime = Process.filter(q, downtime_category='Unplanned', downtime=1).aggregate(total_downtime=Sum('down_ptime'))['total_downtime']
                available_time = Process.filter(q).aggregate(total_duration=Sum('duration'))['total_duration']
                ideal_cycle_time = Process.filter(q, process_name='Idle').aggregate(total_ideal_cycle_time=Sum('duration'))['total_ideal_cycle_time']
                actual_output = Process.filter(q).aggregate(total_actual=Sum('alert_actual'))['total_actual']

                #OEE calculation
                available_operating_time = available_time - downtime
                availability = available_time - downtime * 100 / available_time
                performance = ideal_cycle_time * actual_output * 100 / available_operating_time
                quality_rate = 100
                oee_thershold = availability * performance * quality_rate
                # if oee_thers != 0 and oee_thershold >= oee_thers:
                result = {
                    "machine": machine,
                    "oee_thrlhold": oee_thershold
                }
                thrhold_list.append(result)
            logger.info(f"{current_date} {current_time} : OEE threshold successfully get")
            return json.Response(
                    {'data': thrhold_list},'OEE threshold successfully get',200,True)
        except Exception as err_msg:
            logger.info(f"{current_date} {current_time} : {err_msg} : Failed to retrieve Oee data")
            return json.Response({"data":[]},"Failed to get the OEE threshold value", 400,False)
