from .models import Industry


def update_industry(industry_id, data):
    try:
        industry = Industry.objects.get(id=industry_id)
        industry.name = data
        industry.save()
        return True
    except Industry.DoesNotExist:
        return False


def delete_industry(industry_id):
    try:
        industry = Industry.objects.get(id=industry_id)
        industry.delete()
        return True
    except Industry.DoesNotExist:
        return False
