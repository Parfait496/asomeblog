python manage.py collectstatic --noinput
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'Admin1234!')" | python manage.py shell