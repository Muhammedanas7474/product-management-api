import redis
from celery import current_app
from django.conf import settings
from django.db import connection
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="System Health Check",
        responses={
            200: inline_serializer(
                name="HealthCheckResponse",
                fields={
                    "status": serializers.CharField(),
                    "services": serializers.DictField(child=serializers.CharField()),
                },
            )
        },
    )
    def get(self, request):
        services = {}

        # ------------------
        # Database Check
        # ------------------
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            services["database"] = "healthy"
        except Exception:
            services["database"] = "unhealthy"

        # ------------------
        # Redis Check
        # ------------------
        try:
            r = redis.from_url(settings.CELERY_BROKER_URL)
            r.ping()
            services["redis"] = "healthy"
        except Exception:
            services["redis"] = "unhealthy"

        # ------------------
        # Celery Worker Check
        # ------------------
        try:
            inspect = current_app.control.inspect(timeout=1)
            ping = inspect.ping()

            if ping:
                services["celery_worker"] = "healthy"
            else:
                services["celery_worker"] = "unhealthy"

        except Exception:
            services["celery_worker"] = "unhealthy"

        # ------------------
        # Overall Status
        # ------------------
        if all(status == "healthy" for status in services.values()):
            overall_status = "ok"
        elif any(status == "healthy" for status in services.values()):
            overall_status = "degraded"
        else:
            overall_status = "error"

        return Response({"status": overall_status, "services": services})
