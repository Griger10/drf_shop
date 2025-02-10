from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils import set_dict_attr
from apps.profiles.serializers import ProfileSerializer

tags = ['Profiles']


class ProfileView(APIView):
    serializer_class = ProfileSerializer

    @extend_schema(
        summary="Retrieve profile",
        description="""
                This endpoint allows a user to retrieve his/her profile.
            """,
        tags=tags,
    )
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Update profile",
        description="""
            This endpoint allows to update changeable profile info.
        """,
        tags=tags
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Delete profile",
        description="""
            This endpoint allows to do "safe" deletion of profile
        """,
        tags=tags
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={"message": "User account have been deactivated"})
