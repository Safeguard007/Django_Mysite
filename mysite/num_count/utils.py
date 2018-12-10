import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadNumDate


def read_cookie(request, obj):
        ct = ContentType.objects.get_for_model(obj)
        key = "%s_%s_read" % (ct.model, obj.pk)
        if not request.COOKIES.get(key):
            readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()
            date = timezone.now().date()
            readdetail, created = ReadNumDate.objects.get_or_create(content_type=ct, object_id=obj.pk, read_date=date)
            readdetail.read_num += 1
            readdetail.save()
        return key


def read_num_by_days(obj, days):
    date_list = []
    num_list = []
    today = timezone.now().date()
    ct = ContentType.objects.get_for_model(obj)
    for i in range(days, 0, -1):
        date = today - datetime.timedelta(days=i)
        date_list.append(date.strftime('%m/%d'))
        readdetail = ReadNumDate.objects.filter(content_type=ct, object_id=obj.pk, read_date=date)
        num = readdetail.aggregate(read_num_sum=Sum('read_num'))
        num_list.append(num['read_num_sum'] or 0)

    return date_list, num_list


def get_hot_blog(content_type, days):
    date = timezone.now().date() - datetime.timedelta(days=days)
    readdetail = ReadNumDate.objects.filter(content_type=content_type, read_date=date).order_by('-read_num')
    return readdetail
