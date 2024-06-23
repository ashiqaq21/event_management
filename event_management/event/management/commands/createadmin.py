from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a default admin user if it does not exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            uname = input("Enter Username: ")
            pwd = input("Enter Password: ")

            user = User.objects.create(
                username=uname,
                email='admin@example.com',
                role='admin'
            )
            user.set_password(pwd)  
            user.save()

            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            user = User.objects.get(username='admin')
            change_pwd = input("Admin user already exists. Do you want to change the password? (yes/no): ")
            
            if change_pwd.lower() == 'yes':
                new_pwd = input("Enter new Password: ")
                user.set_password(new_pwd)  
                user.save()
                self.stdout.write(self.style.SUCCESS('Successfully changed admin password'))
            else:
                self.stdout.write(self.style.WARNING('Admin password was not changed'))
