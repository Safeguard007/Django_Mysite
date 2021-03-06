from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeRecord, LikeCount


def SuccessResponse(like_num):
    data = dict()
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = dict()
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    user = request.user
    object_id = int(request.GET.get('object_id'))
    if not user.is_authenticated:
        return ErrorResponse(400, '你还未登录')

    try:
        content_type = ContentType.objects.get(model=request.GET.get('content_type'))
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '对象不存在')

    if request.GET.get('is_like') == 'true':                   # 点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:                         # 未点赞过，可以点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:                               # 已点赞过，不可以点赞
            return ErrorResponse(402, '已经点赞，不能重复点赞')
    else:                                   # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return ErrorResponse(404, '数据错误')
        else:
            return ErrorResponse(403, '没有点赞，不能取消点赞')