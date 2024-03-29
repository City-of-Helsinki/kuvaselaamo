import factory
from django.db.models.signals import post_save

from hkm.models.models import (
    Collection,
    Feedback,
    ProductOrder,
    Record,
    TmpImage,
    User,
    UserProfile,
)


class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback


class TmpImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TmpImage


class ProductOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductOrder


@factory.django.mute_signals(post_save)
class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("hkm.tests.factories.UserFactory", profile=None)

    class Meta:
        model = UserProfile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("email")
    email = factory.LazyAttribute(lambda user: user.username)
    profile = factory.RelatedFactory(UserProfileFactory, factory_related_name="user")

    class Meta:
        model = User

    @factory.post_generation
    def user_data(self, create, extracted, **kwargs):
        if not create:
            return

        CollectionFactory(owner=self)
        TmpImageFactory(creator=self)
        FeedbackFactory(user=self)
        ProductOrderFactory(user=self)


class RecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Record


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    @factory.post_generation
    def records(self, create, extracted, **kwargs):
        if not create:
            return

        RecordFactory(creator=self.owner, collection=self)
