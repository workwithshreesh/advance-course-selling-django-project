# 0005_merge_20240917_0102

# Example migration file
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_merge_20240917_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('thumbnail', models.ImageField(upload_to='customImage/thumbnail')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.aboutcategory')),
            ],
        ),
    ]
