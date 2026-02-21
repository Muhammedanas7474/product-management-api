from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
import redis
from celery import current_app


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

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

        return Response({
            "status": overall_status,
            "services": services
        })
