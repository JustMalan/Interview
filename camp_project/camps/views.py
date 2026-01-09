from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CampForm, ParentRegistrationForm, StudentForm, CampRegistrationForm
from .models import Camp, ParentRegistration, Student


def home(request):
    return redirect("camps:camp_list")


# --- Camps ---


def camp_list(request):
    camps = Camp.objects.annotate(
        total_registrations=Count("registrations", distinct=True),
        missing_students=Count(
            "registrations__parent_registration",
            filter=Q(registrations__parent_registration__student__isnull=True),
            distinct=True,
        ),
    )
    return render(request, "camps/camp_list.html", {"camps": camps})


def camp_create(request):
    if request.method == "POST":
        form = CampForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("camps:camp_list")
    else:
        form = CampForm()

    return render(request, "camps/camp_form.html", {"form": form})


# --- Parent Registrations ---


def registration_list(request):
    regs = ParentRegistration.objects.all().select_related("student")
    return render(request, "camps/registration_list.html", {"regs": regs})


def registration_create(request):
    if request.method == "POST":
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save()
            return redirect("camps:registration_detail", pk=reg.pk)
    else:
        form = ParentRegistrationForm()

    return render(request, "camps/registration_form.html", {"form": form})


def registration_detail(request, pk: int):
    reg = get_object_or_404(ParentRegistration.objects.select_related("student"), pk=pk)
    camp_regs = reg.camp_registrations.select_related("camp")

    camp_reg_form = CampRegistrationForm(parent_registration=reg)

    return render(
        request,
        "camps/registration_detail.html",
        {
            "reg": reg,
            "camp_regs": camp_regs,
            "camp_reg_form": camp_reg_form,
        },
    )


def registration_add_student(request, pk: int):
    reg = get_object_or_404(ParentRegistration, pk=pk)

    # OneToOne: if already exists, redirect
    if hasattr(reg, "student"):
        return redirect("camps:registration_detail", pk=reg.pk)

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.parent_registration = reg
            student.save()
            return redirect("camps:registration_detail", pk=reg.pk)
    else:
        form = StudentForm()

    return render(request, "camps/student_form.html", {"form": form, "reg": reg})


def registration_add_camp(request, pk: int):
    reg = get_object_or_404(ParentRegistration, pk=pk)

    if request.method != "POST":
        return redirect("camps:registration_detail", pk=reg.pk)

    form = CampRegistrationForm(request.POST, parent_registration=reg)
    if form.is_valid():
        try:
            form.save()
        except Exception:
            # Keep it simple for interviews; you can improve this later
            pass

    return redirect("camps:registration_detail", pk=reg.pk)
