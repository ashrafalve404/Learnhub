from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'certificate_id', 'issued_at']
    list_filter = ['issued_at']
    search_fields = ['user__username', 'course__title', 'certificate_id']
    readonly_fields = ['certificate_id', 'issued_at']
