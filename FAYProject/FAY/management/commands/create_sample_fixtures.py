from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Dict

from FAY.models.model_event_type import EventType
from FAY.models.model_profile import Profile
from FAY.models.model_event import Event


class Command(BaseCommand):
    help = (
        "Create sample data: 3 users (1 USER, 2 CREATORS), some event types and events"
    )

    def handle(self, *args, **options):
        # Create some event types
        type_names = ["Music", "Art", "Tech"]
        et_objs = []
        for name in type_names:
            et, created = EventType.objects.get_or_create(name=name)
            et_objs.append(et)

        # Users to create
        accounts = [
            {"username": "user1", "email": "user1@example.com", "password": "password123", "role": "USER", "name": "Standard User"},
            {"username": "creator1", "email": "creator1@example.com", "password": "password123", "role": "CREATOR", "name": "Alice Creator"},
            {"username": "creator2", "email": "creator2@example.com", "password": "password123", "role": "CREATOR", "name": "Bob Creator"},
        ]

        created_users: Dict[str, User] = {}
        for acc in accounts:
            user, created = User.objects.get_or_create(username=acc["username"], defaults={"email": acc["email"]})
            # Ensure password and email are set/updated
            user.set_password(acc["password"])  # set a known password
            user.email = acc["email"]
            user.save()

            # Profile is auto-created by signal; update it
            profile = Profile.objects.get(user=user)
            profile.role = acc["role"]
            profile.name = acc.get("name") or user.username
            if profile.role == "CREATOR":
                # customize creator profiles
                profile.description = f"Profile de {profile.name} - créateur d'événements"
                # give each creator different event types
                if user.username == "creator1":
                    profile.event_types.set([et_objs[0], et_objs[1]])
                else:
                    profile.event_types.set([et_objs[1], et_objs[2]])
            profile.save()
            created_users[user.username] = user

        # Create some events linked to creators
        events_to_create = [
            {
                "creator": "creator1",
                "name": "Concert Night",
                "date": timezone.now(),
                "location": "Paris",
                "price": 25.0,
                "link": "https://example.com/concert",
                "description": "Soirée musicale exceptionnelle",
                "capacity": 120,
                "types": [et_objs[0]],
            },
            {
                "creator": "creator1",
                "name": "Art & Wine",
                "date": timezone.now(),
                "location": "Lyon",
                "price": 15.0,
                "link": "https://example.com/art",
                "description": "Exposition d'art accompagnée d'un bar à vin",
                "capacity": 60,
                "types": [et_objs[1]],
            },
            {
                "creator": "creator2",
                "name": "Tech Meetup",
                "date": timezone.now(),
                "location": "Marseille",
                "price": 0.0,
                "link": "https://example.com/tech",
                "description": "Rencontre autour des nouvelles techs",
                "capacity": 200,
                "types": [et_objs[2]],
            },
        ]

        for ev in events_to_create:
            # use explicit, typed local variables to avoid static analysis issues
            creator_username = str(ev["creator"])
            creator = created_users.get(creator_username)
            if not creator:
                continue

            ev_name = ev["name"]
            ev_date = ev["date"]
            ev_location = ev["location"]
            ev_price = ev["price"]
            ev_link = ev["link"]
            ev_description = ev["description"]
            ev_capacity = ev["capacity"]
            ev_types = ev.get("types", [])

            defaults = {
                "creator": creator,
                "date": ev_date,
                "location": ev_location,
                "price": ev_price,
                "link": ev_link,
                "description": ev_description,
                "capacity": ev_capacity,
            }

            event, created = Event.objects.get_or_create(name=ev_name, defaults=defaults)

            # (re)assign event types
            event.event_types.set(ev_types)
            event.save()

        self.stdout.write(self.style.SUCCESS("Sample fixtures created/updated successfully."))




