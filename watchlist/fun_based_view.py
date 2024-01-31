from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Watchlist
from company.models import Company
from watchlist.utils import update_watchlist, delete_watchlist


# GET watchlists/ : Render a create new watchlist form
# POST watchlists/ : create a new watchlist
def create_watchlist(request):

    # Render CREATE a new watchlist form
    if request.method == 'GET':
        return render(request, 'company_management/create_watchlist.html')

    # CREATE a new watchlist
    elif request.method == 'POST':
        try:
            new_watchlist_name = request.POST['watchlist_name']
            Watchlist.objects.create(name=new_watchlist_name)
            return redirect('watchlist',)
        except:
            redirect('create_watchlist')


# GET watchlist/<wlname>/ Details on specific watchlist detail

def watchlist_detail(request, watchlist_name):
    watchlist = get_object_or_404(Watchlist, name=watchlist_name)
    companies = watchlist.companies.all()
    return render(request, 'company_management/new_watchlist_detail.html', {'watchlist': watchlist, 'companies': companies})

# GET /watchlists/<int:watchlist_id>/update/
# PUT /watchlists/<int:watchlist_id>/update/


def update_watchlist(request, watchlist_name):
    if request.method == 'GET':
        pass
        # # UPDATE a watchlist
    elif request.method == 'PUT':
        # Call utility function to update watchlist name
        updated = update_watchlist(watchlist_name, data=request.POST)
        if updated:
            return redirect('watchlist')
        else:
            return HttpResponse(status=404)  # Not Found

# /watchlists/<int:watchlist_id>/delete/


def delete_watchlist(request, watchlist_name):
    # DELETE a watchlist
    if request.method == 'DELETE':
        # Call utility function to delete watchlist
        deleted = delete_watchlist(watchlist_name)
        if deleted:
            return redirect('watchlist')
        else:
            return HttpResponse(status=404)  # Not Found


# /watchlists/<int:watchlist_id>/add-company/
def watchlist_edit(request, watchlist_name, company_id=None):

    # render form to ADD A COMPANY to watchlist
    if request.method == 'GET':
        watchlist = Watchlist.objects.get(name=watchlist_name)
        companies = Company.objects.exclude(watchlist=watchlist)
        return render(request, 'watchlist/watchlist_add_company.html', {'companies': companies, 'watchlist': watchlist})

  # ADD A COMPANY to watchlist & edit watchlist
    elif request.method == 'POST':
        if company_id is None:
            return JsonResponse({'error': 'Invalid request.'}, status=400)
        # Get list of selected company from form
        company_ids = request.POST.getlist('company_ids')

        # check list is empty
        if not company_ids:
            # No checkboxes were selected, handle the error here
            error_message = "Please select at least one company."
            return render(request, 'watchlist/watchlist_add_company.html', {'companies': Company.objects.all(), 'error_message': error_message})

        watchlist = Watchlist.objects.get(name=watchlist_name)

        # add all the companies to watchlist
        for company_id in company_ids:
            try:
                company = Company.objects.get(id=company_id)
                if company not in watchlist.companies.all():
                    watchlist.companies.add(company)
            except Company.DoesNotExist:
                # Handle the error here if the company doesn't exist
                error_message = f"Company with ID {company_id} does not exist."
                return render(request, 'company_management/add_companies.html', {'companies': Company.objects.all(), 'error_message': error_message})
        return redirect('watchlist')

      # REMOVE A COMPANY from watchlist
    elif request.method == 'DELETE':
        if company_id is None:
            return JsonResponse({'error': 'Invalid request.'}, status=400)
        try:
            watchlist = get_object_or_404(Watchlist, name=watchlist_name)
            company = get_object_or_404(Company, id=company_id)
            watchlist.companies.remove(company)
            return JsonResponse({'message': 'Company removed from watchlist.'})
        except Watchlist.DoesNotExist:
            return JsonResponse({'error': 'Watchlist does not exist.'}, status=404)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company does not exist.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
