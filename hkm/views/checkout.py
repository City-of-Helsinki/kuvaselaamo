import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from hkm.basket.order_creator import OrderCreator
from hkm.forms import OrderContactInformationForm
from hkm.models.models import ProductOrder


LOG = logging.getLogger(__name__)


class OrderContactFormView(TemplateView):
    template_name = 'hkm/views/order_contact_information.html'
    url_name = 'hkm_order_contact_information'

    def __init__(self):
        super(OrderContactFormView, self).__init__()

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == 'order-contact-info':
            return self.handle_order_contact_info(request, *args, **kwargs)
        return super(OrderContactFormView, self).post(request, *args, **kwargs)

    def handle_order_contact_info(self, request, *args, **kwargs):
        form = OrderContactInformationForm(request.POST, prefix='order-contact-information-form')

        if form.is_valid():
            form.cleaned_data['form_phase'] = 3
            ProductOrder.objects.filter(
                pk__in=[line.order_pk for line in request.basket.product_lines]
            ).update(**form.cleaned_data)

            return redirect(reverse('hkm_order_summary'))
        kwargs['order_contact_information_form'] = form
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderContactFormView, self).get_context_data(**kwargs)
        context['form_page'] = 2
        order = ProductOrder.objects.filter(
            pk__in=[line.order_pk for line in self.request.basket.product_lines]
        ).first()
        context['order'] = order
        context['order_contact_information_form'] = OrderContactInformationForm(
            prefix='order-contact-information-form',
            instance=order or ProductOrder()
        )
        return context


class OrderSummaryView(TemplateView):
    template_name = 'hkm/views/order_summary.html'
    url_name = 'hkm_order_summary'

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == 'order-submit':
            order_creator = OrderCreator()
            if not order_creator.validate_basket(request.basket):
                raise
            order_collection = order_creator.create_order_from_basket(request.basket)
            order_collection.save()

            datetime_checkout_started = timezone.now()
            LOG.debug('ORDER ATTEMPT STARTED AT: ',
                extra={
                    'data': {
                        'order_hash': order_collection.pk,
                        'time': str(datetime_checkout_started)
                    }
                })
            order_collection.save()
            redirect_url = order_collection.checkout()
            if redirect_url:
                request.basket.clear_all()
                return redirect(redirect_url)

        # TODO error messaging for user in UI
        return redirect(reverse('hkm_order_summary'))

    def get_context_data(self, **kwargs):
        context = super(OrderSummaryView, self).get_context_data(**kwargs)
        context['form_page'] = 3
        order = ProductOrder.objects.filter(
            pk__in=[line.order_pk for line in self.request.basket.product_lines]
        ).first()
        context['order'] = order
        return context