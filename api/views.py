from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response


class BaseListCreateAPIView(ListAPIView, CreateAPIView):
    serializer_class = None
    create_form, list_form = None, None
    message_success = "success"
    message_failed = "error"

    def list(self, request, *args, **kwargs):
        form = self.list_form(request.GET)
        if form.is_valid():
            serializer = self.get_serializer(form.get_queryset(), many=True)
            return Response(dict(status=200, data=serializer.data, message=self.message_success))
        return Response(dict(status=400, message=form.errors))

    def create(self, request, *args, **kwargs):
        form = self.create_form(request.data)
        if form.is_valid():
            form.save()
            return Response(dict(status=200, message=self.message_success))
        return Response(dict(status=400, message=form.errors))