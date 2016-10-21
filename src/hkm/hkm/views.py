
# -*- coding: utf-8 -*-

import logging
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.core.urlresolvers import reverse
from finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)


class BaseView(TemplateView):
  url_name = None

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


class ImageDetailView(BaseView):
  template_name = 'hkm/views/image.html'


class ImageFeedbackView(BaseView):
  template_name = 'hkm/views/image_feedback.html'


class ImageEditBaseView(BaseView):
  pass


class ImageEditAddToCollectionView(BaseView):
  template_name = 'hkm/views/image_edit_add_to_collection.html'


class ImageEditDownloadView(BaseView):
  template_name = 'hkm/views/image_edit_download.html'


class ImageEditOrderView(BaseView):
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
      # LanguageMiddleware will automatically set the profile language for logged in users
      # so no need to set session value here
    else:
      request.session[LANGUAGE_SESSION_KEY] = lang
    return super(LanguageView, self).get(request, *args, **kwargs)

  def get_redirect_url(self, *args, **kwargs):
    return self.request.GET.get('next', '/')


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
