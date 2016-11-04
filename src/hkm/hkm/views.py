
# -*- coding: utf-8 -*-

import logging
from django import http
from django.views.generic import TemplateView, RedirectView, View
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from finna import DEFAULT_CLIENT as FINNA
from hkm.hkm_client import DEFAULT_CLIENT as HKM
from hkm.models import Collection, Record
from hkm import forms
from hkm import tasks
from hkm import settings

LOG = logging.getLogger(__name__)


class BaseView(TemplateView):
  url_name = None
  permissions = {}

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

  def handle_invalid_post_action(self, request, *args, **kwargs):
    LOG.error('Invalid POST action', extra={'data': {'POST': repr(request.POST),
      'permissions': self.permissions}})
    return http.HttpResponseBadRequest()

  def get_empty_forms(self, request):
    return {}

  def get(self, request, *args, **kwargs):
    _kwargs = self.get_empty_forms(request)
    _kwargs.update(kwargs)
    return self.render_to_response(self.get_context_data(**_kwargs))

  def get_context_data(self, **kwargs):
    context = super(BaseView, self).get_context_data(**kwargs)
    context['language'] = self.request.session.get(LANGUAGE_SESSION_KEY, settings.DEFAULT_LANGUAGE)
    context['current_url'] = self.get_url()
    return context


class InfoView(BaseView):
  template_name = 'hkm/views/info.html'
  url_name = 'hkm_info'

  def get_empty_forms(self, request):
    if request.user.is_authenticated():
      user = request.user
    else:
      user = None
    return {
      'feedback_form': forms.FeedbackForm(prefix='feedback-form', user=user)
    }

  def post(self, request, *args, **kwargs):
    action = request.POST.get('action', None)
    if action == 'feedback':
      return self.handle_feedback(request, *args, **kwargs)
    return self.handle_invalid_post_action(request, *args, **kwargs)

  def handle_feedback(self, request, *args, **kwargs):
    if request.user.is_authenticated():
      user = request.user
    else:
      user = None
    form = forms.FeedbackForm(request.POST, prefix='feedback-form', user=user)
    if form.is_valid():
      feedback = form.save()
      tasks.send_feedback_notification.apply_async(args=(feedback.id,), countdown=5)
      # TODO: redirect to success page?
      return redirect(self.url_name)
    kwargs['feedback_form'] = form
    return self.get(request, *args, **kwargs)


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
  permissions = {
    'can_edit': False,
  }

  def get_template_names(self):
    if self.record:
      return 'hkm/views/collection_record.html'
    else:
      return self.template_name

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

    self.permissions = {
      'can_edit': self.request.user == self.collection.owner or self.request.user.profile.is_admin
    }

    return True

  def get_empty_forms(self, request):
    return {
      'collection_form': forms.CollectionForm(prefix='collection-form', instance=self.collection),
    }

  def post(self, request, *args, **kwargs):
    action = request.POST.get('action', None)
    if self.permissions['can_edit']:
      if action == 'edit':
        return self.handle_edit(request, *args, **kwargs)
      if action == 'remove-record':
        return self.ajax_handle_remove_record(request, *args, **kwargs)
    return self.handle_invalid_post_action(request, *args, **kwargs)

  def handle_edit(self, request, *args, **kwargs):
    form = forms.CollectionForm(request.POST, prefix='collection-form', instance=self.collection)
    if form.is_valid():
      form.save()
      return redirect(self.get_url())
    else:
      kwargs['collection_form'] = form
      return self.get(request, *args, **kwargs)

  def ajax_handle_remove_record(self, request, *args, **kwargs):
    record_id = request.POST.get('record_id', None)
    if record_id:
      try:
        record = self.collection.records.get(id=record_id)
      except Record.DoesNotExist:
        return http.HttpResponseNotFound()
      else:
        record.delete()
        return http.HttpResponse()
    return http.HttpResponseBadRequest()

  def get_context_data(self, **kwargs):
    context = super(CollectionDetailView, self).get_context_data(**kwargs)
    context['collection'] = self.collection
    context['permissions'] = self.permissions
    context['record'] = self.record
    if self.record:
      context['next_record'] = self.collection.get_next_record(self.record)
      context['previous_record'] = self.collection.get_previous_record(self.record)
    return context


class IndexView(CollectionDetailView):
  template_name = 'hkm/views/index.html'
  url_name = 'hkm_index'

  def get_url(self):
    return reverse(self.url_name)

  def setup(self, request, *args, **kwargs):
    collections = Collection.objects.filter(show_in_landing_page=True)
    if collections.exists():
      self.collection = collections[0]
    else:
      LOG.warning('Co collections to show in landing page')

    record_id = request.GET.get('rid', None)
    if record_id:
      try:
        self.record = self.collection.records.get(id=record_id)
      except Record.DoesNotExist:
        LOG.warning('Record does not exist or does not belong to this collection')
    if not self.record and self.collection:
      self.record = self.collection.records.first()

    self.permissions = {
      'can_edit': False
    }

    return True


class SearchView(BaseView):
  template_name = 'hkm/views/search.html'
  url_name = 'hkm_search'

  page_size = 40
  use_detailed_query = False

  facet_result = None
  search_result = None

  search_term = None
  facet_type = None
  facet_value = None
  page = 1

  def get(self, request, *args, **kwargs):
    if self.search_term:
      self.handle_search(request, *args, **kwargs)
    return super(SearchView, self).get(request, *args, **kwargs)

  def get_template_names(self):
    if self.request.is_ajax():
      return 'hkm/snippets/search_records_grid.html'
    else:
      return self.template_name

  def setup(self, request, *args, **kwargs):
    self.search_term = request.GET.get('search', None)
    self.facet_type = request.GET.get('ft', None)
    self.facet_value = request.GET.get('fv', None)
    self.page = int(request.GET.get('page', 1))
    return True

  def handle_search(self, request, *args, **kwargs):
    LOG.debug('Search', extra={'data': {'search_term': self.search_term, 'facet_type': self.facet_type,
      'facet_value': self.facet_value, 'page': self.page}})
    self.facet_result = self.get_facet_result(self.search_term)
    self.search_result = self.get_search_result(self.search_term, self.facet_type, self.facet_value,
        self.page, self.page_size)

    # calculate global index for the record, this is used to form links to search detail view
    # which is technically same view as this, it only shows one image per page
    if not self.search_result['resultCount'] == 0:
      i = 1 # record's index in current page
      for record in self.search_result['records']:
        p = self.search_result['page'] - 1 # zero indexed page
        record['index'] = p * self.search_result['limit'] + i
        i += 1
        # Check also if this record is in user's favorite collection
        if request.user.is_authenticated():
          try:
            favorites_collection = Collection.objects.get(owner=request.user, collection_type=Collection.TYPE_FAVORITE)
          except Collection.DoesNotExist:
            pass
          else:
            record['is_favorite'] = favorites_collection.records.filter(record_id=record['id']).exists()

  def get_facet_result(self, search_term):
    if self.request.is_ajax():
      return None
    else:
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

    url = reverse('hkm_search_record')
    url += '?search=%s&ft=%s&fv=%s&page=%d' % (self.search_term, self.facet_type, self.facet_value,
        self.page)
    return redirect(url)

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
    self.record_finna_id = kwargs.get('finna_id', None)
    if self.record_finna_id:
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


class FinnaRecordFeedbackView(BaseFinnaRecordDetailView):
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


class AjaxUserFavoriteRecordView(View):
  def post(self, request, *args, **kwargs):
    record_id = request.POST.get('record_id', None)
    action = request.POST.get('action', 'add')
    favorites_collection, created = Collection.objects.get_or_create(owner=request.user, collection_type=Collection.TYPE_FAVORITE,
        defaults={'title': _(u'Favorites'), 'description': _(u'Your favorite images are collected here')})

    if record_id:
      if action == 'add':
        record = Record(creator=request.user, collection=favorites_collection, record_id=record_id)
        record.save()
      elif action == 'remove':
        # There shouldn't be multiple rows for same record, but if there is, delete all
        records = favorites_collection.records.filter(record_id=record_id)
        records.delete()
      return http.HttpResponse()
    return http.HttpResponseBadRequest()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
