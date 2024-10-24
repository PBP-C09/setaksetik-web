from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from review.forms import ReviewEntryForm
from review.models import ReviewEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.contrib import messages
from explore.models import Menu
from explore.forms import MenuFilterForm
from main.models import UserProfile

# batasan
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

@login_required(login_url='/login')
def show_review(request):

    context = {
        'nama' : 'steak',
        'lokasi' : 'jaksel',
        'rating' : '5'
    }
    return render(request, 'review.html', context)



def show_xml(request):
    data = ReviewEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ReviewEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_review_entry_ajax(request):
    menu = strip_tags(request.POST.get("menu"))
    place = strip_tags(request.POST.get("place"))
    rating = strip_tags(request.POST.get("rating"))
    description = request.POST.get("description")
    user = request.user

    new_review = ReviewEntry(
        menu=menu, place=place,
        rating=rating,
        user=user, description=description
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)


def create_review_entry(request):
    # Retrieve all menu entries without filtering
    menus = Menu.objects.all()
    
    # Print menus to check in console/logs
    print("Menus: ", menus)
    
    # Context data for rendering the template
    context = {
        'menus': menus,  # Pass the query result
    }

    return render(request, 'create_review_entry.html', context)

def edit_review(request, id):
    # Get the review entry based on id
    review = ReviewEntry.objects.get(pk=id)
    user_profile = UserProfile.objects.get(user=request.user)

    # Allow only admins to edit
    if user_profile.role != "admin":
        messages.error(request, "You do not have permission to edit this review.")
        return redirect('review:show_review')

    # Set review entry as an instance of the form
    form = ReviewEntryForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:show_review'))

    context = {'form': form}
    return render(request, "edit_review.html", context)

def delete_product(request, id):
    # Get the review based on id
    review = ReviewEntry.objects.get(pk=id)
    user_profile = UserProfile.objects.get(user=request.user)

    # Allow only admins to delete
    if user_profile.role != "admin":
        messages.error(request, "You do not have permission to delete this review.")
        return redirect('review:show_review')

    review.delete()
    return HttpResponseRedirect(reverse('review:show_review'))

# def create_review_entry(request):
#     form = ReviewEntryForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         review_entry = form.save(commit=False)
#         review_entry.user = request.user
#         review_entry.save()
#         return redirect('review:show_review')

#     context = {'form': form}
#     return render(request, "create_review_entry.html", context)