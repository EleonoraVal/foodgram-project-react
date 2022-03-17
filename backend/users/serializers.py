from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id',
            'firstname',
            'lastname',
            'username',
            'email',
            'password'
        )
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )]

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationaError(
                'This username is impossible to be used.'
            )
        return username
