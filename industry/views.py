from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.db.models import Count
from article.utils import search_news

from industry.utils import delete_industry, update_industry
from .models import Industry


# /industry
# GET : List of all industries
def industry_list(request):
    try:
        # Fetch all industries, add num of industries in db as a count variable
        industries = Industry.objects.annotate(num_companies=Count("company"))
    except Industry.DoesNotExist as e:
        return HttpResponse(e)
    return render(request, "industry/industry_list.html", {"industries": industries})


# /industry/<str:industry_name>/feed
# GET: updates on specific industry
def industry_feed(request, industry_name):
    query = industry_name
    is_search = True
    watchlist = {"name": f"Updates on {query}"}
    if query:
        results = search_news(query, 10)
        return render(
            request,
            "article/search.html",
            {
                "news": results,
                "query": query,
                "watchlist": watchlist,
                "is_search": is_search,
            },
        )
    else:
        # Redirect back to the same page if an empty query is submitted
        return redirect("industry_list")


# /industry/create
class CreateIndustryView(View):
    """
    View for creating a new watchlist.
    GET: Render a create new industry form.
    POST: Create a new industry.
    """

    def get(self, request):
        return render(request, "industry/industry_create.html")

    def post(self, request):
        try:
            industry_name = request.POST.get("industry_name")
            Industry.objects.create(name=industry_name)
            return redirect("industry_list")
        except Industry.DoesNotExist as e:
            redirect("create_industry")


# /industry/<int:industry_id>/
class UpdateIndustryView(View):
    """
    View for creating a new industry.
    GET: Render a create new industry form.
    POST: Create a new industry.
    """

    def get(self, request, industry_id):
        industry = Industry.objects.get(id=industry_id)
        return render(request, "industry/industry_update.html", {"industry": industry})

    def post(self, request, industry_id):
        updated = update_industry(industry_id, data=request.POST["new_name"])
        if updated:
            return redirect("industry_list")
        else:
            return redirect("update_industry")


# /industry/delete/
class DeleteIndustryView(View):
    """
    View for deleting an industry.
    POST: Delete the industry.
    """

    def post(self, request):
        print(request.POST.get("industry_id"))
        deleted = delete_industry(request.POST.get("industry_id"))

        if deleted:
            return redirect("industry_list")
        else:
            print("delete is false")
            return HttpResponse(status=404)
