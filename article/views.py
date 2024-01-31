from django.shortcuts import redirect, render
from watchlist.models import Watchlist
from .utils import get_news, get_current_price, search_news, get_companies

# Get the gold, usd price
price = get_current_price()


# /home
# GET: Show Price cards, Updates on Watchlist 'portfolio'
def home(request):
    watchlist_name = "portfolio"
    try:
        company_list, watchlist = get_companies(watchlist_name)
        news = get_news(company_list, 1)

        return render(
            request,
            "article/index.html",
            {
                "watchlist": watchlist,
                "news": news,
                "price": price,
            },
        )

    except Watchlist.DoesNotExist:
        # Or handle non-existing watchlist error
        watchlist = {"name": watchlist_name}
        return render(
            request,
            "article/index.html",
            {"watchlist": watchlist},
        )


# /search
# GET: Fetch updates on single company or keyword
def search(request):
    query = request.GET.get("q")
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
            },
        )
    else:
        # Redirect back to the same page if an empty query is submitted
        return redirect("home")


# /<str:watchlist>
# GET: Fetch Updates on Watchlist passed in url parameter
def feed(request, watchlist_name):
    if request.method == "GET":
        try:
            company_list, watchlist = get_companies(watchlist_name)
            news = get_news(company_list, 2)
            return render(
                request,
                "article/index.html",
                {
                    "watchlist": watchlist,
                    "news": news,
                },
            )

        except Watchlist.DoesNotExist:
            # Or handle non-existing watchlist error
            watchlist = {"name": watchlist_name}
            return render(
                request,
                "article/index.html",
                {
                    "watchlist": watchlist,
                    "price": price,
                },
            )
