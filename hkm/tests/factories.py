import factory

from hkm.models.models import Feedback, TmpImage, ProductOrder, User, Collection, Record


class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback


class TmpImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TmpImage


class ProductOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductOrder


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')

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
