from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Company
from industry.models import Industry
from .utils import update_company, delete_company


# /company
# GET : List of all companies
def company_list(request):
    try:
        companies = Company.objects.all()
    except Company.DoesNotExist as e:
        return HttpResponse(e)
    return render(request, "company/company_list.html", {"companies": companies})


# /company/create
class CreateCompanyView(View):
    """
    View for creating a new watchlist.
    GET: Render a create new company form.
    POST: Create a new company.
    """

    def get(self, request):
        industries = Industry.objects.all()
        return render(
            request, "company/company_create.html", {"industries": industries}
        )

    def post(self, request):

        # fetch company name & its industry from form
        company_name = request.POST.get("company_name")
        industry_id = request.POST.get("company_industry")

        try:
            industry = Industry.objects.get(id=industry_id)
            # Check if the company name already exists in the database
            existing_company = Company.objects.filter(name=company_name).first()
            if existing_company:
                # Redirect if company already exists
                return redirect("create_company")

            # create & save a company instance then redirect to companies list page
            company = Company.objects.create(name=company_name)
            company.industries.set([industry])
            return redirect("company_list")

        except Industry.DoesNotExist:
            return HttpResponse("Invalid industry ID", status=400)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


# company/<int:company_id>/
class UpdateCompanyView(View):
    """
    View for creating a new watchlist.
    GET: Render a create new company form.
    POST: Create a new company.
    """

    def get(self, request, company_id):
        # fetch the company & all industries from db for update form
        company = Company.objects.get(id=company_id)
        industries = Industry.objects.all()
        return render(
            request,
            "company/company_update.html",
            {"company": company, "industries": industries},
        )

    def post(self, request, company_id):
        # fetch company name, industry id from form posted
        company_name = request.POST.get("new_name")
        industry_id = request.POST.get("company_industry")
        # update the new data to corresponding company object
        updated = update_company(company_id, company_name, industry_id)
        if updated:
            return redirect("company_list")
        else:
            return HttpResponse(status=404)


# /company/delete
class DeleteCompanyView(View):
    """
    View for deleting a watchlist.
    POST: Delete the watchlist.
    """

    def post(self, request):
        # return true if successfully deletes the company object
        deleted = delete_company(request.POST.get("company_id"))
        if deleted:
            return redirect("company_list")
        else:
            return HttpResponse(status=404)
