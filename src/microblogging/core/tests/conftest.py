from datetime import datetime

import pytest
from core.models import Profiles, Tags, Twits


@pytest.fixture(autouse=True)
def populate_db() -> None:
    profile_1 = Profiles.objects.create(
        first_name="John",
        last_name="Doe",
        username="testuser1",
        password="123456",
        email="testuser1@gmail.com",
        country="Poland",
        description="test text user1",
        date_of_birth=datetime(2000, 1, 1),
    )
    profile_2 = Profiles.objects.create(
        first_name="Donald",
        last_name="Perkins",
        username="testuser2",
        password="qwerty",
        email="testuser2@gmail.com",
        country="USA",
        description="test text user2",
        date_of_birth=datetime(1985, 12, 1),
    )
    profile_3 = Profiles.objects.create(
        first_name="Michael",
        last_name="Hughes",
        username="testuser3",
        password="password",
        email="testuser3@gmail.com",
        country="Belarus",
        description="test text user3",
        date_of_birth=datetime(2002, 7, 3),
        is_active=False,
    )
    profile_1.followers.set([profile_2, profile_3])
    profile_2.followers.set([profile_1])

    tag_1 = Tags.objects.create(tag="python")
    tag_2 = Tags.objects.create(tag="sql")
    tag_3 = Tags.objects.create(tag="postresql")
    tag_4 = Tags.objects.create(tag="sport")

    twit_1 = Twits.objects.create(
        text="test text twit_1",
        profile=profile_1,
    )
    twit_1.tag.set([tag_1, tag_2, tag_3])
    twit_1.like.set([profile_2, profile_3])
    twit_1.repost.set([profile_2, profile_3])

    twit_2 = Twits.objects.create(
        text="test text twit_2",
        profile=profile_1,
    )
    twit_2.tag.set([tag_2, tag_3])
    twit_2.like.set([profile_2])
    twit_2.repost.set([profile_2, profile_3])

    twit_3 = Twits.objects.create(
        text="test text twit_3",
        profile=profile_1,
    )
    twit_3.tag.set([tag_1, tag_3, tag_4])
    twit_3.like.set([profile_2, profile_3])

    twit_4 = Twits.objects.create(
        text="test text twit_4",
        profile=profile_2,
    )
    twit_4.tag.set([tag_1])
    twit_4.like.set([profile_1, profile_3])
    twit_4.repost.set([profile_1, profile_3])

    twit_5 = Twits.objects.create(
        text="test text twit_5", profile=profile_3, answer_to_twit=twit_2
    )
    twit_5.tag.set([tag_2, tag_3])
    twit_5.like.set([profile_2])
    twit_5.repost.set([profile_2, profile_1])

    twit_6 = Twits.objects.create(
        text="test text twit_6", profile=profile_2, answer_to_twit=twit_1
    )
    twit_6.tag.set([tag_4])
    twit_6.like.set([profile_1])
    twit_6.repost.set([profile_1])

    profile_1.notification.set([twit_6, twit_5])
    profile_2.notification.set([twit_1])
    profile_3.notification.set([twit_6, twit_1])
