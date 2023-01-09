from typing import Any, Optional, Mapping
from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

import jwt
import datetime

class User(auth_models.AbstractUser):

    def to_dict(self) -> Mapping[str, Any]:
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class UserService():

    def get_user(self, email: str) -> User:
        user = User.objects.filter(email=email).first()
        return user 


    def create_user(self, username: str, first_name: str, last_name: str, email: str, password: Optional[str] = None) -> User:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    

    def create_token(self, user_id:int) -> str:
        payload = dict(
            id=user_id,
            exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24), #delais d'expiration
            iat=datetime.datetime.utcnow()
        )
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        return token