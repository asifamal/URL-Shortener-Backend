from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import URL
import sys

class ShortenURL(APIView):
    def post(self, request):
        try:
            original_url = request.data.get('original_url')

            if not original_url:
                return Response({
                    "status": 0,
                    "message": "original_url is required."
                }, status=400)

            # Create new shortened URL
            url_obj = URL.objects.create(original_url=original_url)

            return Response({
                "status": 1,
                "message": "Short URL created successfully.",
                "data": {
                    "id": url_obj.id,
                    "original_url": url_obj.original_url,
                    "short_code": url_obj.short_code,
                    "created_at": url_obj.created_at
                }
            }, status=201)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return Response({
                "status": 0,
                "reason": str(e),
                "line_num": str(exc_tb.tb_lineno)
            }, status=500)


class RedirectURL(APIView):
    def get(self, request, short_code):
        try:
            url_obj = URL.objects.filter(short_code=short_code).first()

            if url_obj:
                # Optional: Add click counting in the future
                return redirect(url_obj.original_url)
            else:
                return Response({
                    "status": 0,
                    "message": "Short URL not found."
                }, status=404)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return Response({
                "status": 0,
                "reason": str(e),
                "line_num": str(exc_tb.tb_lineno)
            }, status=500)


class URLListView(APIView):
    def get(self, request):
        try:
            urls = URL.objects.all().order_by('-created_at')  # latest first
            data = []
            for url in urls:
                data.append({
                    "id": url.id,
                    "original_url": url.original_url,
                    "short_code": url.short_code,
                    "created_at": url.created_at,
                })
            return Response({"status": 1, "data": data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return Response({
                "status": 0,
                "reason": str(e),
                "line_num": str(exc_tb.tb_lineno)
            }, status=500)
        

class DeleteURL(APIView):
    def delete(self, request, pk):
        try:
            url = URL.objects.filter(id=pk).first()
            if not url:
                return Response({"status": 0, "message": "URL not found"}, status=404)
            url.delete()
            return Response({"status": 1, "message": "URL deleted successfully"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return Response({
                "status": 0,
                "reason": str(e),
                "line_num": str(exc_tb.tb_lineno)
            }, status=500)
