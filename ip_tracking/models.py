from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.core.cache import cache
import requests
from .models import RequestLog, BlockedIP

class IPLoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_ip, is_routable = get_client_ip(request)
        if not client_ip:
            return

        # Blocked IPs
        if BlockedIP.objects.filter(ip_address=client_ip).exists():
            return HttpResponseForbidden("Access denied.")

        # Check cache for geolocation
        geo_data = cache.get(client_ip)
        if not geo_data:
            try:
                response = requests.get(f"https://ipinfo.io/{client_ip}/json")
                if response.status_code == 200:
                    data = response.json()
                    geo_data = {
                        "country": data.get("country"),
                        "city": data.get("city"),
                    }
                    cache.set(client_ip, geo_data, 60*60*24)
                else:
                    geo_data = {"country": None, "city": None}
            except:
                geo_data = {"country": None, "city": None}

        # Log request
        RequestLog.objects.create(
            ip_address=client_ip,
            path=request.path,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            country=geo_data['country'],
            city=geo_data['city']
        )