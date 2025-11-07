# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]



