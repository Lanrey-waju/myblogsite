from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom User Manager where Email is the unque identifier"""

    def create_user(self, email, password, **extra_fields):
        """Create a normal user with a given email and password"""
        if not email:
            raise ValueError("You must provide an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser with a given email and password"""

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)
