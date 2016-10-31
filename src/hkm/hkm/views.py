
# -*- coding: utf-8 -*-

import logging
from django import http
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from finna import DEFAULT_CLIENT as FINNA
from hkm.hkm_client import DEFAULT_CLIENT as HKM
from hkm.models import Collection, Record
from hkm import settings

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
    context['language'] = self.request.session.get(LANGUAGE_SESSION_KEY, settings.DEFAULT_LANGUAGE)
    context['current_url'] = self.get_url()
    return context


class IndexView(BaseView):
  template_name = 'hkm/views/index.html'
  url_name = 'hkm_index'


class InfoView(BaseView):
  template_name = 'hkm/views/info.html'
  url_name = 'hkm_info'


class BaseCollectionListView(BaseView):
  collection_qs = Collection.objects.none()

  def setup(self, request, *args, **kwargs):
    self.collection_qs = self.get_collection_qs(request, *args, **kwargs)
    return True

  def get_collection_qs(self, request, *args, **kwargs):
    raise NotImplementedError('Subclasses must implement this method')

  def get_context_data(self, **kwargs):
    context = super(BaseCollectionListView, self).get_context_data(**kwargs)
    context['collections'] = self.collection_qs
    return context


class PublicCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/public_collections.html'
  url_name = 'hkm_public_collections'

  def get_collection_qs(self, request, *args, **kwargs):
    return Collection.objects.filter(is_public=True)


class MyCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/my_collections.html'
  url_name = 'hkm_my_collections'

  def get_collection_qs(self, request, *args, **kwargs):
    return Collection.objects.filter(owner=request.user)


class CollectionDetailView(BaseView):
  template_name = 'hkm/views/collection.html'
  url_name = 'hkm_collection'

  collection = None
  record = None

  def get_url(self):
    url = reverse(self.url_name, kwargs={'collection_id': self.collection.id})
    if self.record:
      url += '?rid=%s' % str(self.record.id)
    return url

  def setup(self, request, *args, **kwargs):
    collection_id = kwargs['collection_id']
    try:
      self.collection = Collection.objects.user_can_view(request.user).get(id=collection_id)
    except Collection.DoesNotExist:
      LOG.warning('Collection does not exist or does not belong this user')
      raise http.Http404()

    record_id = request.GET.get('rid', None)
    if record_id:
      try:
        self.record = self.collection.records.get(id=record_id)
      except Record.DoesNotExist:
        LOG.warning('Record does not exist or does not belong to this collection')
    if not self.record:
      self.record = self.collection.records.first()

    return True

  def get_context_data(self, **kwargs):
    context = super(CollectionDetailView, self).get_context_data(**kwargs)
    context['collection'] = self.collection
    context['record'] = self.record
    context['next_record'] = self.collection.get_next_record(self.record)
    context['previous_record'] = self.collection.get_previous_record(self.record)
    return context


class SearchView(BaseView):
  template_name = 'hkm/views/search.html'
  url_name = 'hkm_search'

  page_size = 20
  use_detailed_query = False

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
    page = int(request.GET.get('page', 1))
    LOG.debug('Search', extra={'data': {'search_term': self.search_term, 'facet_type': self.facet_type,
      'facet_value': self.facet_value, 'page': page}})
    self.facet_result = self.get_facet_result(self.search_term)
    self.search_result = self.get_search_result(self.search_term, self.facet_type, self.facet_value,
        page, self.page_size)

    # calculate global index for the record, this is used to form links to search detail view
    # which is technically same view as this, it only shows one image per page
    i = 1 # record's index in current page
    for record in self.search_result['records']:
      p = self.search_result['page'] - 1 # zero indexed page
      record['index'] = p * self.search_result['limit'] + i
      i += 1

  def get_facet_result(self, search_term):
    return FINNA.get_facets(self.search_term)

  def get_search_result(self, search_term, facet_type, facet_value, page, limit):
    return FINNA.search(search_term, facet_type=facet_type,
        facet_value=facet_value, page=page, limit=limit, detailed=self.use_detailed_query)

  def get_context_data(self, **kwargs):
    context = super(SearchView, self).get_context_data(**kwargs)
    context['facet_result'] = self.facet_result
    context['facet_type'] = self.facet_type
    context['facet_value'] = self.facet_value
    context['search_result'] = self.search_result
    context['search_term'] = self.search_term
    return context


class SearchRecordDetailView(SearchView):
  url_name = 'hkm_search_record'
  template_name = 'hkm/views/search_record.html'

  page_size = 1
  use_detailed_query = True

  def get_facet_result(self, search_term):
    return None

  def get_context_data(self, **kwargs):
    context = super(SearchRecordDetailView, self).get_context_data(**kwargs)
    record = self.search_result['records'][0]
    record['full_res_url'] = HKM.get_full_res_image_url(record['rawData']['thumbnail'])
    context['record'] = record
    return context


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
      self.record['full_res_url'] = HKM.get_full_res_image_url(self.record['rawData']['thumbnail'])
    return True

  def get_context_data(self, **kwargs):
    context = super(BaseFinnaRecordDetailView, self).get_context_data(**kwargs)
    context['record'] = self.record
    return context


class FinnaRecordDetailView(BaseFinnaRecordDetailView):
  template_name = 'hkm/views/record.html'

  def post(self, request, *args, **kwargs):
    action = request.POST.get('action', None)
    if request.user.is_authenticated():
      if action == 'add-to-collection':
        return self.handle_add_to_collection(request, *args, **kwargs)
    LOG.error('Invalid POST request', extra={'data': {'POST': repr(request.POST)}})
    return http.HttpResponseBadRequest()

  def handle_add_to_collection(self, request, *args, **kwargs):
    record_id = request.POST.get('record_id', None)
    if not record_id:
      LOG.warning('Record ID missing')
      return http.HttpResponseBadRequest()

    collection_id = request.POST.get('collection_id', None)
    if collection_id:
      try:
        collection = request.user.collections.get(id=collection_id)
      except Collection.DoesNotExist:
        LOG.warning('Invalid collection id', extra={'data': {'collection_id': collection_id}})
        return http.HttpResponseBadRequest()
    else:
      new_collection_name = request.POST.get('new_collection_name', None)
      if not new_collection_name:
        LOG.warning('New collection name missing')
        return http.HttpResponseBadRequest()
      collection = Collection(owner=request.user, title=new_collection_name)
      collection.save()

    record = Record(collection=collection, record_id=record_id, creator=request.user)
    record.save()

    url = reverse('hkm_collection', kwargs={'collection_id': collection.id})
    url += '?rid=%s' % record.id
    return redirect(url)


class FinnaRecordFeedbackView(BaseView):
  template_name = 'hkm/views/record_feedback.html'


class FinnaRecordEditBaseView(BaseView):
  pass


class FinnaRecordEditAddToCollectionView(BaseView):
  template_name = 'hkm/views/record_edit_add_to_collection.html'


class FinnaRecordEditDownloadView(BaseView):
  template_name = 'hkm/views/record_edit_download.html'


class FinnaRecordEditOrderView(BaseView):
  template_name = 'hkm/views/record_edit_order.html'





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
