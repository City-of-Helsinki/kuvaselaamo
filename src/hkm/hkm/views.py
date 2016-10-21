
# -*- coding: utf-8 -*-

import logging
from django import http
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.core.urlresolvers import reverse
from finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)


class BaseView(TemplateView):
  url_name = None

  def dispatch(self, request, *args, **kwargs):
    result = self.setup(request, *args, **kwargs)
    if result:
      if isinstance(result, http.HttpResponse):
        return result
      else:
        return super(BaseView, self).dispatch(request, *args, **kwargs)
    return http.HttpResponseBadRequest()

  def setup(self, request, *args, **kwargs):
    return True

  def get_url(self):
    if self.url_name == None:
      raise Exception('Subview must define url_name or overwrire get_url method')
    return reverse(self.url_name)

  def get_context_data(self, **kwargs):
    context = super(BaseView, self).get_context_data(**kwargs)
    context['language'] = self.request.session[LANGUAGE_SESSION_KEY]
    context['current_url'] = self.get_url()
    return context


class IndexView(BaseView):
  template_name = 'hkm/views/index.html'
  url_name = 'hkm_index'


class InfoView(BaseView):
  template_name = 'hkm/views/info.html'
  url_name = 'hkm_info'


class BaseCollectionListView(BaseView):
  pass


class PublicCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/public_collections.html'
  url_name = 'hkm_public_collections'


class MyCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/my_collections.html'
  url_name = 'hkm_my_collections'


class CollectionDetailView(BaseView):
  template_name = 'hkm/views/collection.html'


class BaseFinnaRecordDetailView(BaseView):
  record_finna_id = None
  url_name = 'hkm_record'
  record = None

  def get_url(self):
    return reverse(self.url_name, kwargs={'finna_id': self.record_finna_id})

  def setup(self, request, *args, **kwargs):
    self.record_finna_id = kwargs['finna_id']
    record_data = FINNA.get_record(self.record_finna_id)
    if record_data:
      self.record = record_data['records'][0]
    return True

  def get_context_data(self, **kwargs):
    context = super(BaseFinnaRecordDetailView, self).get_context_data(**kwargs)
    context['record'] = self.record
    return context


class FinnaRecordDetailView(BaseFinnaRecordDetailView):
  template_name = 'hkm/views/image.html'


class FinnaRecordFeedbackView(BaseView):
  template_name = 'hkm/views/image_feedback.html'


class FinnaRecordEditBaseView(BaseView):
  pass


class FinnaRecordEditAddToCollectionView(BaseView):
  template_name = 'hkm/views/image_edit_add_to_collection.html'


class FinnaRecordEditDownloadView(BaseView):
  template_name = 'hkm/views/image_edit_download.html'


class FinnaRecordEditOrderView(BaseView):
  template_name = 'hkm/views/image_edit_order.html'


class SearchView(BaseView):
  template_name = 'hkm/views/search.html'
  url_name = 'hkm_search'

  facet_result = None
  search_result = None

  search_term = None
  facet_type = None
  facet_value = None

  def get(self, request, *args, **kwargs):
    search_term = request.GET.get('search', None)
    if search_term:
      self.handle_search(request, search_term, *args, **kwargs)
    return super(SearchView, self).get(request, *args, **kwargs)

  def handle_search(self, request, search_term, *args, **kwargs):
    self.search_term = search_term
    self.facet_type = request.GET.get('ft', None)
    self.facet_value = request.GET.get('fv', None)
    LOG.debug('Search', extra={'data': {'search_term': self.search_term, 'facet_type': self.facet_type,
      'facet_value': self.facet_value}})
    self.facet_result = FINNA.get_facets(self.search_term)
    self.search_result = FINNA.search(self.search_term, facet_type=self.facet_type,
        facet_value=self.facet_value, page=1)

  def get_context_data(self, **kwargs):
    context = super(SearchView, self).get_context_data(**kwargs)
    context['facet_result'] = self.facet_result
    context['search_result'] = self.search_result
    context['search_term'] = self.search_term
    return context

class SignUpView(BaseView):
  template_name = 'hkm/views/signup.html'
  url_name = 'hkm_signup'

class LanguageView(RedirectView):
  def get(self, request, *args, **kwargs):
    lang = request.GET.get('lang', 'fi')
    if not lang in ('fi', 'en', 'sv'):
      lang = 'fi'
    if request.user.is_authenticated():
      profile = request.user.profile
      profile.language = lang
      profile.save()
    request.session[LANGUAGE_SESSION_KEY] = lang
    return super(LanguageView, self).get(request, *args, **kwargs)

  def get_redirect_url(self, *args, **kwargs):
    return self.request.GET.get('next', '/')


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
