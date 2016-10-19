
# -*- coding: utf-8 -*-

import logging
from django.views.generic import TemplateView
from finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)


class BaseView(TemplateView):
  pass


class IndexView(BaseView):
  template_name = 'hkm/views/index.html'


class InfoView(BaseView):
  template_name = 'hkm/views/info.html'


class BaseCollectionListView(BaseView):
  pass


class PublicCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/public_collections.html'


class MyCollectionsView(BaseCollectionListView):
  template_name = 'hkm/views/my_collections.html'


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
  search_result = None

  def get(self, request, *args, **kwargs):
    search_term = request.GET.get('search', None)
    page = request.GET.get('page', 1)
    if search_term:
      self.search_result = FINNA.search(search_term, page=page)
    return super(SearchView, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(SearchView, self).get_context_data(**kwargs)
    context['search_result'] = self.search_result
    return context

class SignUpView(BaseView):
  template_name = 'hkm/views/signup.html'


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
