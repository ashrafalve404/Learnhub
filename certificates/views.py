from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
import uuid
from .models import Certificate
from enrollments.models import Enrollment


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).select_related('course')
    return render(request, 'certificates/my_certificates.html', {'certificates': certificates})


def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    return render(request, 'certificates/certificate_detail.html', {'certificate': certificate})


def generate_certificate(enrollment):
    certificate_id = f"CERT-{uuid.uuid4().hex[:10].upper()}"
    certificate, created = Certificate.objects.get_or_create(
        user=enrollment.user,
        course=enrollment.course,
        defaults={'certificate_id': certificate_id}
    )
    return certificate
