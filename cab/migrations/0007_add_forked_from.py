# Generated manually for adding forked_from field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0006_alter_snippet_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='forked_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forks', to='cab.snippet'),
        ),
    ]