from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_abouttabs'),  # Adjust this dependency to match the last migration in your project
    ]

    operations = [
        # Create AboutCategory model
        migrations.CreateModel(
            name='AboutCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, null=False)),
            ],
        ),
    ]
