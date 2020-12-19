from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exception_, context):
    response = exception_handler(exception_, context)
    if response is not None:
        return response

    exception_list = str(exception_).split("DETAIL: ")
    return Response(
        {
            "resError": True,
            "error": exception_list[-1]
        }, status=403
    )
