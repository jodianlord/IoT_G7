from api.views import BaseListCreateAPIView
from rest_framework.response import Response
from facility.models import FacilityReading, Facility
from api.facility.forms import FacilityReadingForm, FacilityReadingListForm
from api.facility.serializers import FacilityReadingSerializer, FacilityReadingSerializer2


class FacilityReadingLCView(BaseListCreateAPIView):
    serializer_class = FacilityReadingSerializer
    create_form = FacilityReadingForm
    list_form = FacilityReadingListForm
    queryset = FacilityReading.objects.all()

    def list(self, request, *args, **kwargs):
        form = self.list_form(request.GET, request=request)
        if form.is_valid():
            serializer = FacilityReadingSerializer2(form.get_queryset(), many=True)
            return Response(dict(status=200, data=dict(items=serializer.data), message=self.message_success))
        return Response(dict(status=400, message=form.errors))

    def create(self, request, *args, **kwargs):
        form = self.create_form(request.data, request.FILES, request=request)
        if form.is_valid():
            return Response(dict(status=200, data=dict(items=form.save()), message=self.message_success))
        return Response(dict(status=400, message=form.errors))

