from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from safety_database.settings import Settings


class YearIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "year-index"
        projection = AllProjection()

    year = NumberAttribute(hash_key=True)
    event_id = UnicodeAttribute(range_key=True)


class AccidentRecord(Model):
    class Meta:
        table_name = Settings().table_name
        region = Settings().aws_region
        host = Settings().dynamodb_endpoint_url
        aws_access_key_id = Settings().aws_access_key_id
        aws_secret_access_key = Settings().aws_secret_access_key

    event_id = UnicodeAttribute(hash_key=True)
    year = NumberAttribute()

    year_index = YearIndex()
    location_key = UnicodeAttribute()
    latitude = NumberAttribute(null=True)
    longitude = NumberAttribute(null=True)

    event_date = UnicodeAttribute()
    location = UnicodeAttribute(null=True)

    country = UnicodeAttribute(null=True)
    injury_severity = UnicodeAttribute(null=True)
    aircraft_category = UnicodeAttribute(null=True)
    make = UnicodeAttribute(null=True)
    model = UnicodeAttribute(null=True)
    investigation_type = UnicodeAttribute(null=True)
    accident_number = UnicodeAttribute(null=True)
