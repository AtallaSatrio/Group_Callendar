from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_user(
        self,
        email,
        username,
        password,
        is_staff=True,
        is_team_lead=False,
        is_superuser=False,
    ):
        if not email:
            raise ValueError(_("User must submit a email"))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base user account : an email address is required"))

        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_team_lead=is_team_lead,
            is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password,
        username,
        is_staff=True,
        is_team_lead=False,
        is_superuser=True,
    ):
        if not email:
            raise ValueError(_("Superusers must have a email"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin Account: An email address is required"))

        if not password:
            raise ValueError(_("Superusers must have a password"))

        user = self.create_user(
            email, username, password, is_staff=is_staff, is_superuser=is_superuser
        )

        user.save(using=self._db)

        return user
