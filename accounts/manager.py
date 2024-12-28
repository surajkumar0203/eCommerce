from django.contrib.auth.models import BaseUserManager



class MyUserManager(BaseUserManager):
    def create_user(self,username,email,first_name,last_name,password=None):
        if not username:
            raise ValueError("username cant't be empty")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            
        )
        
        
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,first_name,last_name,password=None):
        user = self.create_user(
            username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            
        )
        user.is_admin = True
        user.is_active= True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user