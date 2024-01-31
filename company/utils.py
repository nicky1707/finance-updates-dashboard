from .models import Company
from industry.models import Industry


def update_company(company_id, company_name, industry_id):
    try:
        company = Company.objects.get(id=company_id)
        industry = Industry.objects.get(id=industry_id)
        company.name = company_name
        company.industries.set([industry])
        company.save()
        return True
    except Company.DoesNotExist:
        return False


def delete_company(company_id):
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        return True
    except Company.DoesNotExist:
        return False
