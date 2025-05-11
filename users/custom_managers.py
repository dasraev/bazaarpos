from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,login,password,**extra_fields):
        if not login:
            raise ValueError('username is required')
        user = self.model(login = login,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,login,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        return self.create_user(login,password,**extra_fields)

