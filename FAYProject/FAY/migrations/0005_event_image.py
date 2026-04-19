from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FAY", "0004_eventtype_remove_event_event_type_profile_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="events/images/"),
        ),
    ]
