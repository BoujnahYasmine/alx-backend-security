from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_count = {}
    for log in logs:
        ip_count[log.ip_address] = ip_count.get(log.ip_address, 0) + 1
        if log.path in ["/admin", "/login"]:
            SuspiciousIP.objects.get_or_create(ip_address=log.ip_address, reason=f"Accessed sensitive path {log.path}")

    for ip, count in ip_count.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(ip_address=ip, reason="More than 100 requests in last hour")