import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from hkm.basket.order_creator import OrderCreator
from hkm.forms import OrderContactInformationForm
from hkm.models.models import ProductOrder, ProductOrderCollection

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

# Payment Provider GETs this route after payment has been processed to notify of success/failure
# In testing API there is never time lag with this, but in real system
# there can be


class OrderPBWNotify(View):
    template_name = ''
    url_name = 'hkm_order_pbw_notify'
    result = {}

    def get(self, request, *args, **kwargs):

        self.result['authcode'] = request.GET.get('AUTHCODE', None)
        self.result['return_code'] = request.GET.get('RETURN_CODE', None)
        self.result['order_hash'] = request.GET.get('ORDER_NUMBER', None)
        self.result['settled'] = request.GET.get('SETTLED', None)
        self.result['incident_id'] = request.GET.get('INCIDENT_ID', None)
        order_collection = ProductOrderCollection.objects.get(pk=self.result['order_hash'])

        if order_collection.authcode_valid(self.result):
            order_collection.handle_confirmation(self.result)
        else:
            LOG.error('AUTHCODE MISMATCH! ', extra={
                    'data': {'order_hash': order_collection.pk}})

        return HttpResponse()


# User is redirected to this route from Payment Provider after payment
# With a success return code, the user is displayed a success message
# If and only if the request parameter 'settled' is true, the order will
# be sent to print


class OrderConfirmation(TemplateView):
    template_name = 'hkm/views/order_show_result.html'
    url_name = 'hkm_order_confirmation'
    result = {}

    def get(self, request, *args, **kwargs):

        self.result['authcode'] = request.GET.get('AUTHCODE', None)
        self.result['return_code'] = request.GET.get('RETURN_CODE', None)
        self.result['order_hash'] = request.GET.get('ORDER_NUMBER', None)
        self.result['settled'] = request.GET.get('SETTLED', None)
        self.result['incident_id'] = request.GET.get('INCIDENT_ID', None)
        try:
            self.order_collection = ProductOrderCollection.objects.get(pk=self.result['order_hash'])
        except ObjectDoesNotExist:
            return HttpResponseForbidden()

        if self.order_collection.authcode_valid(self.result):
            self.order_collection.handle_confirmation(self.result)
            request.basket.clear_all()
        else:
            LOG.error('AUTHCODE MISMATCH! ', extra={
                    'data': {'order_hash': self.order_collection.pk}})
            return HttpResponseForbidden()
        return super(OrderConfirmation, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderConfirmation, self).get_context_data(**kwargs)
        context['order_collection'] = self.order_collection
        context['order'] = self.order_collection.product_orders.first()
        return context
