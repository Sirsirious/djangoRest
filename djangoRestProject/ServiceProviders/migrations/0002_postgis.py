from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ServiceProviders", "0001_initial"),
    ]

    operations = [
        # Use a GIST index for the ServiceArea model - these are optimized for fast geometry searches
        # We'll use this with GEOJson to search for ServiceAreas that contain a given point faster.
        # This increases
        migrations.RunSQL(
            sql='CREATE INDEX servicearea_area_gist ON "ServiceProviders_servicearea" USING GIST (area);',
            reverse_sql="DROP INDEX servicearea_area_gist;",
        ),
    ]
