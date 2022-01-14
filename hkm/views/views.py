# -*- coding: utf-8 -*-

import copy
import io
import json
import logging
import math
from urllib.parse import urlencode

from django import http
from django.conf import settings
from django.contrib.auth import forms as django_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.cache import caches
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, render_to_response
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext as _
from django.views.generic import RedirectView, TemplateView, View
from unidecode import unidecode

from hkm import email, forms, image_utils
from hkm.finna import DEFAULT_CLIENT as FINNA
from hkm.models.models import Collection, PageContent, Record, Showcase, TmpImage

MAX_RECORDS_PER_FINNA_QUERY = 200

LOG = logging.getLogger(__name__)

RESULTS_PER_PAGE = 40
DEFAULT_CACHE = caches["default"]


class AuthForm(django_forms.AuthenticationForm):
    username = django_forms.UsernameField(
        max_length=254,
        widget=django_forms.forms.TextInput,
    )


class BaseView(TemplateView):
    url_name = None
    permissions = {}

    def dispatch(self, request, *args, **kwargs):
        result = self.setup(request, *args, **kwargs)
        if result:
            if isinstance(result, http.HttpResponse):
                return result
            else:
                return super().dispatch(request, *args, **kwargs)
        return http.HttpResponseBadRequest()

    def setup(self, request, *args, **kwargs):
        return True

    def get_url(self):
        if not self.url_name:
            raise Exception("Subview must define url_name or overwrire get_url method")
        params = {
            key: unidecode(self.request.GET[key].encode("utf-8").decode("utf-8"))
            for key in ("image_id", "search", "page")
            if key in self.request.GET
        }
        encoded_params = urlencode(params)
        url = reverse(self.url_name)
        if encoded_params:
            url = "{}?{}".format(url, encoded_params)
        return url

    def handle_invalid_post_action(self, request, *args, **kwargs):
        LOG.error(
            "Invalid POST action",
            extra={
                "data": {"POST": repr(request.POST), "permissions": self.permissions}
            },
        )
        return http.HttpResponseBadRequest()

    def get_empty_forms(self, request):
        return {
            "login_form": AuthForm(),
            "sign_up_form": forms.RegistrationForm(),
            "password_reset_form": PasswordResetForm(),
        }

    def get(self, request, *args, **kwargs):
        _kwargs = self.get_empty_forms(request)
        _kwargs.update(kwargs)
        return self.render_to_response(self.get_context_data(**_kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["language"] = self.request.session.get(
            LANGUAGE_SESSION_KEY, settings.LANGUAGE_CODE
        )
        context["my_domain_url"] = settings.HKM_MY_DOMAIN
        context["current_url"] = self.get_url()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "login":
            return self.handle_login(request, *args, **kwargs)
        if action == "signup":
            return self.handle_signup(request, *args, **kwargs)
        if action == "password_reset":
            return self.handle_password_reset(request, *args, **kwargs)
        return self.handle_invalid_post_action(request, *args, **kwargs)

    def handle_login(self, request, *args, **kwargs):
        form = django_forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Redirect museum users to collections page after logging in
            if user.profile.is_museum:
                return redirect("hkm_public_collections")

            # TODO migth wanna do a PRG pattern here also. Returning the rendered template directly
            # is to keep the query string values in place, which otherwise
            # would be lost in redirect phase
            return self.get(request, *args, **kwargs)
        kwargs["login_form"] = form
        return self.get(request, *args, **kwargs)

    def handle_signup(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            auth_login(request, form.save())
            # TODO migth wanna do a PRG pattern here also. Returning the rendered template directly
            # is to keep the query string values in place, which otherwise
            # would be lost in redirect phase
            return self.get(request, *args, **kwargs)
        kwargs["sign_up_form"] = form
        return self.get(request, *args, **kwargs)

    def handle_password_reset(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        language = self.request.session.get(
            LANGUAGE_SESSION_KEY, settings.LANGUAGE_CODE
        )
        template = "registration/password_reset_email_%s.html" % language

        if form.is_valid():
            form.save(
                email_template_name=template,
                request=request,
                use_https=True,
                extra_email_context={"HKM_MY_DOMAIN": settings.HKM_MY_DOMAIN},
            )
            return http.HttpResponse()


class InfoView(BaseView):
    template_name = "hkm/views/info.html"
    url_name = "hkm_info"

    def get_empty_forms(self, request):
        context_forms = super().get_empty_forms(request)
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        context_forms["feedback_form"] = forms.FeedbackForm(
            prefix="feedback-form", user=user
        )
        return context_forms

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "feedback":
            return self.handle_feedback(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def handle_feedback(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        form = forms.FeedbackForm(request.POST, prefix="feedback-form", user=user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sent_from = "".join([request.get_host(), request.get_full_path()])
            feedback.save()
            email.send_feedback_notification(feedback.id)
            # TODO: redirect to success page?
            return redirect(self.url_name)
        kwargs["feedback_form"] = form
        return self.get(request, *args, **kwargs)


class BaseCollectionListView(BaseView):
    collection_qs = Collection.objects.none()

    def setup(self, request, *args, **kwargs):
        self.collection_qs = self.get_collection_qs(request, *args, **kwargs)
        return True

    def get_collection_qs(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = self.collection_qs
        return context


class PublicCollectionsView(BaseCollectionListView):
    template_name = "hkm/views/public_collections.html"
    url_name = "hkm_public_collections"

    def get_collection_qs(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.profile.is_museum:
            return request.user.profile.albums.all()
        return Collection.objects.filter(is_public=True, is_featured=False).order_by(
            "created"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_collections"] = Collection.objects.filter(
            is_featured=True
        ).order_by("created")
        return context


class MyCollectionsView(BaseCollectionListView):
    template_name = "hkm/views/my_collections.html"
    url_name = "hkm_my_collections"

    def get_collection_qs(self, request, *args, **kwargs):
        return Collection.objects.filter(owner=request.user)


def tag_favorites_if_necessary(request, records_to_tag):
    """Fetch the currently authenticated user's favorite records and tag
    them in the given record list."""
    if request.user.is_authenticated():
        try:
            favorite_records = Record.objects.filter(
                collection__owner=request.user,
                collection__collection_type=Collection.TYPE_FAVORITE,
            ).values_list("record_id", flat=True)

            for record in records_to_tag:
                record.is_favorite = record.record_id in favorite_records
        except Record.DoesNotExist:
            pass


def get_records_with_finna_data(request, collection):
    """Fetch the given Collection's Records' matching Finna entries and add
    the entries to the Records, if a matching entry was found from Finna.

    Fetching from Finna is done in multiple calls in case the Collection
    contains a lot of Records. This is done to avoid a 414 error from Finna.
    """
    records = collection.records.all()
    record_ids_in_collection = [r.record_id for r in records]

    finna_entries_by_id = {}
    for chunk in chunks(record_ids_in_collection, MAX_RECORDS_PER_FINNA_QUERY):
        entries_from_finna = FINNA.get_record(chunk)

        if entries_from_finna and "records" in entries_from_finna:
            finna_dict = dict((e["id"], e) for e in entries_from_finna["records"])
            finna_entries_by_id.update(finna_dict)

    records_with_finna_data = []
    if finna_entries_by_id:
        for record in records:
            if record.record_id in finna_entries_by_id:
                record.finna_entry = finna_entries_by_id[record.record_id]
                records_with_finna_data.append(record)

    return records_with_finna_data


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# CODEBASE HAD TWO DIFFERENT USES FOR SAME VARIABLE 'record', RENAMED THEM IN THIS CONTEXT SO THAT
# collection_record REFERS TO RECORD IN A COLLECTION, record TO A RECORD IN FINNA/HKM DATABASE
# STILL NEED TO DO SOME FURTHER RENAMING IN FUTURE TO CLEAR CONFUSION
class CollectionDetailView(BaseView):
    template_name = "hkm/views/collection.html"
    url_name = "hkm_collection"

    collection = None
    collection_record = None
    collections_records_to_display = None
    permissions = {
        "can_edit": False,
    }

    def get_template_names(self):
        if self.collection_record:
            return "hkm/views/collection_record.html"
        else:
            return self.template_name

    def get_url(self):
        url = reverse(self.url_name, kwargs={"collection_id": self.collection.id})
        if self.collection_record:
            url += "?rid=%s" % str(self.collection_record.id)
        return url

    def setup(self, request, *args, **kwargs):
        collection_id = kwargs["collection_id"]
        try:
            self.collection = Collection.objects.user_can_view(request.user).get(
                id=collection_id
            )
        except Collection.DoesNotExist:
            LOG.warning("Collection does not exist or does not belong this user")
            raise http.Http404()

        collection_record_id = request.GET.get("rid", None)
        if collection_record_id:
            try:
                self.collection_record = self.collection.records.get(
                    id=collection_record_id
                )
            except Record.DoesNotExist:
                LOG.warning(
                    "Record does not exist or does not belong to this collection"
                )
        else:
            self.collections_records_to_display = get_records_with_finna_data(
                request, self.collection
            )

            tag_favorites_if_necessary(request, self.collections_records_to_display)

        self.permissions = {
            "can_edit": self.request.user.is_authenticated()
            and (
                self.request.user == self.collection.owner
                or self.request.user.profile.is_admin
            ),
        }

        return True

    def get_empty_forms(self, request):
        context_forms = super().get_empty_forms(request)
        if request.user.is_authenticated():
            user = request.user
            context_forms["collection_form"] = forms.CollectionForm(
                prefix="collection-form", instance=self.collection, user=user
            )
        else:
            user = None
        context_forms["feedback_form"] = forms.FeedbackForm(
            prefix="feedback-form", user=user
        )
        return context_forms

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if self.permissions["can_edit"]:
            if action == "edit":
                return self.handle_edit(request, *args, **kwargs)
            if action == "remove-record":
                return self.ajax_handle_remove_record(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def handle_edit(self, request, *args, **kwargs):
        form = forms.CollectionForm(
            request.POST,
            prefix="collection-form",
            instance=self.collection,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect(
                reverse(self.url_name, kwargs={"collection_id": self.collection.id})
            )
        else:
            kwargs["collection_form"] = form
            return self.get(request, *args, **kwargs)

    def ajax_handle_remove_record(self, request, *args, **kwargs):
        collection_record_id = request.POST.get("record_id", None)
        if collection_record_id:
            try:
                collection_record = self.collection.records.get(id=collection_record_id)
            except Record.DoesNotExist:
                return http.HttpResponseNotFound()
            else:
                collection_record.delete()
                return http.HttpResponse()
        return http.HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["collection"] = self.collection
        context["collection_record_count"] = self.collection.records.all().count()
        context["permissions"] = self.permissions
        context["collections_records_to_display"] = self.collections_records_to_display
        context["collection_record"] = self.collection_record

        if self.collection_record:
            context["hkm_id"] = self.collection_record.record_id
            context["current_record_order_number"] = self.collection_record.order + 1
            context["next_record"] = self.collection.get_next_record(
                self.collection_record
            )
            context["previous_record"] = self.collection.get_previous_record(
                self.collection_record
            )
            context["record_web_url"] = FINNA.get_image_url(
                self.collection_record.record_id
            )

            context["record"] = self.collection_record.get_details()

            # Also check if record is in user's favorite collection
            if self.request.user.is_authenticated():
                try:
                    favorites_collection = Collection.objects.get(
                        owner=self.request.user,
                        collection_type=Collection.TYPE_FAVORITE,
                    )
                except Collection.DoesNotExist:
                    pass
                else:
                    context["is_favorite"] = favorites_collection.records.filter(
                        record_id=self.collection_record.record_id
                    ).exists()

            related_collections_ids = Record.objects.filter(
                record_id=self.collection_record.record_id
            ).values_list("collection", flat=True)
            related_collections = (
                Collection.objects.user_can_view(self.request.user)
                .filter(id__in=related_collections_ids)
                .distinct()
            )
            context["related_collections"] = related_collections

        if self.request.user.is_authenticated():
            context["my_collections"] = Collection.objects.filter(
                owner=self.request.user
            ).order_by("title")
        else:
            context["my_collections"] = Collection.objects.none()

        return context


class HomeView(BaseView):
    template_name = "hkm/views/home_page.html"
    url_name = "hkm_home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["frontpage_image_collection"] = (
            Collection.objects.prefetch_related("records")
            .filter(show_in_landing_page=True)
            .order_by("created")
            .first()
        )
        context["showcases"] = (
            Showcase.objects.prefetch_related("albums")
            .filter(show_on_home_page=True)
            .order_by("-created")
        )
        return context


class SearchView(BaseView):
    template_name = "hkm/views/search.html"
    url_name = "hkm_search"

    page_size = RESULTS_PER_PAGE
    use_detailed_query = True

    facet_result = None
    search_result = None
    previous_record = None
    record = None
    next_record = None
    single_image = False

    url_params = None
    all_dates = None

    def get(self, request, *args, **kwargs):
        result = self.handle_search(request, *args, **kwargs)
        if isinstance(result, http.HttpResponse):
            return result
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.is_ajax():
            return "hkm/snippets/search_records_grid.html"
        else:
            return self.template_name

    def setup(self, request, *args, **kwargs):
        # Session expires after browser is closed
        request.session.set_expiry(0)
        self.url_params = {
            "search": request.GET.get("search", ""),
            "page": int(request.GET.get("page", 1)),
            "date_from": request.GET.get("date_from", ""),
            "date_to": request.GET.get("date_to", ""),
            "author": [a for a in request.GET.getlist("author", None) if a],
            "date": [d for d in request.GET.getlist("date", None) if d],
        }
        return True

    def handle_search(self, request, *args, **kwargs):
        LOG.debug(
            "Search",
            extra={
                "data": {
                    "search_term": self.url_params["search"],
                    "page": self.url_params["page"],
                }
            },
        )

        url_params = request.session.get("url_params", {})

        session_facet_result = request.session.get("facet_result", None)

        if not session_facet_result:
            self.facet_result = self.get_facet_result(self.url_params["search"])
            # date_from & date_to require full list of dates
            self.all_dates = self.facet_result.get("facets", {}).get(
                "main_date_str", []
            )
        # If search term or year to year changed => fetch facets again
        elif self.__url_params_changed(url_params, ["search", "date_from", "date_to"]):
            self.facet_result = self.get_facet_result(
                self.url_params["search"],
                self.url_params["date_from"],
                self.url_params["date_to"],
            )
            self.all_dates = request.session.get("all_dates")
        else:
            self.facet_result = request.session.get("facet_result")
            self.all_dates = request.session.get("all_dates")

        facets = self.__form_facet_object()

        load_all_pages = bool(int(request.GET.get("loadallpages", 1)))

        session_search_result = copy.deepcopy(request.session.get("search_result", {}))
        records = (
            []
            if self.__url_params_changed(
                url_params, ["search", "author", "date", "date_from", "date_to"]
            )
            else session_search_result.get("records", [])
        )

        # If we don't hit any checks below this point search_results end up being empty
        self.search_result = session_search_result

        # This if statement is true when user makes search with new term or parameters in list view
        if load_all_pages and not kwargs.get("record"):
            if self.__url_params_changed(
                url_params, ["search", "author", "date", "date_from", "date_to"]
            ):
                results = self.get_search_result(
                    self.url_params["search"],
                    self.url_params["page"],
                    self.page_size,
                    facets,
                )
                if results:
                    self.search_result = results
                    records += results.get("records", [])
                if records:
                    # its all one big page of records. So set page number as first page
                    self.search_result["records"] = records
                    # Reset search_result session to make sure there is no wrong values stored
                    request.session["search_result"] = None
        else:
            # If record exist we are in "single image view"
            if kwargs.get("record"):
                # Check if user came from list view or from direct link
                finna_id = request.GET.get("image_id")
                LOG.debug(
                    "Displaying image details", extra={"data": {"finna_id": finna_id}}
                )
                # Check if record is found in session, if not, get it from finna
                records = session_search_result.get("records", [])
                record = next((x for x in records if x["id"] == finna_id), None)
                if not record:
                    result = FINNA.get_record(finna_id)
                    if result and result.get("resultCount", 0) == 0:
                        # If image was not found we want to show different 404 page
                        context = self.get_context_data(**kwargs)
                        return render(
                            request, "hkm/views/404_image.html", context, status=404
                        )
                    self.search_result = result
                    self.single_image = True
                    self.record = result.get("records")[0] if result else None
                # If user came from list view, get selected image from session
                else:
                    # Save previous - selected - next records to corresponding variables
                    record_index = records.index(record)
                    if record_index > 0:
                        self.previous_record = records[record_index - 1]
                    if record_index < len(records) - 1:
                        self.next_record = records[record_index + 1]

                    # Use deepcopy for now, otherwise when setting self.search_result session gets overwritten as well
                    self.record = copy.deepcopy(record)
                    self.search_result = copy.deepcopy(session_search_result)

                    # Take search parameters from session.
                    # This is required for "Back to search results" link to work
                    self.url_params = request.session.get("url_params", {})
                    self.all_dates = request.session.get("all_dates")

            # This else statement is executed when "Load more" is pressed
            else:
                results = self.get_search_result(
                    self.url_params["search"],
                    self.url_params["page"],
                    self.page_size,
                    facets,
                )
                self.search_result = results

        if self.search_result:
            favorite_records = None
            if request.user.is_authenticated():
                # Fetch all favorite records once
                try:
                    favorite_records = Record.objects.filter(
                        collection__owner=request.user,
                        collection__collection_type=Collection.TYPE_FAVORITE,
                    ).values_list("record_id", flat=True)
                    if self.record:
                        self.record["is_favorite"] = (
                            self.record["id"] in favorite_records
                        )
                except Record.DoesNotExist:
                    pass

            if (
                not self.search_result.get("resultCount") == 0
                and "records" in self.search_result
                and not kwargs.get("record")
            ):
                # Check also if this record is one of user's favorites
                for record in self.search_result["records"]:
                    if favorite_records is not None:
                        record["is_favorite"] = record["id"] in favorite_records

                # If user is loading more pictures add them to session.
                # Check for page changed, this will prevent session duplicating itself
                # endlessly if search button is pressed over and over again.
                # Otherwise set session to equal self.search_result.
                if request.session.get("search_result") and self.__url_params_changed(
                    url_params, ["page"]
                ):
                    request.session["search_result"]["records"].extend(
                        self.search_result.get("records")
                    )
                else:
                    request.session["search_result"] = self.search_result
                request.session["facet_result"] = self.facet_result
                request.session["all_dates"] = self.all_dates
                request.session["url_params"] = self.url_params
            elif "records" not in self.search_result:
                # No more records available for the next page
                if self.request.is_ajax():
                    return http.HttpResponseBadRequest()

    def __url_params_changed(self, url_params, selected_fields):
        is_changed = {
            "search": self.url_params["search"] != url_params.get("search", ""),
            "page": self.url_params["page"] != url_params.get("page", ""),
            "author": self.url_params["author"] != url_params.get("author", None),
            "date": self.url_params["date"] != url_params.get("date", None),
            "date_from": self.url_params["date_from"]
            != url_params.get("date_from", ""),
            "date_to": self.url_params["date_to"] != url_params.get("date_to", ""),
        }

        re_fetch = False

        for field in selected_fields:
            if is_changed[field]:
                re_fetch = True

        return re_fetch

    def __form_facet_object(self):
        facets = {}
        if self.url_params["author"]:
            facets["author_facet"] = self.url_params["author"]
        if self.url_params["date"]:
            facets["main_date_str"] = self.url_params["date"]
        if self.url_params["date_from"] or self.url_params["date_to"]:
            date_from = (
                self.url_params["date_from"] if self.url_params["date_from"] else "*"
            )
            date_to = self.url_params["date_to"] if self.url_params["date_to"] else "*"
            facets["search_daterange_mv"] = "[%s TO %s]" % (date_from, date_to)
        return facets

    def get_facet_result(self, search_term, date_from=None, date_to=None):
        if self.request.is_ajax():
            return None
        else:
            return FINNA.get_facets(search_term, date_from=date_from, date_to=date_to)

    def get_search_result(self, search_term, page, limit, facets):
        return FINNA.search(
            search_term,
            page=page,
            limit=limit,
            facets=facets,
            detailed=self.use_detailed_query,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["facet_result"] = self.facet_result
        context["author_facets"] = self.url_params["author"]
        context["date_facets"] = self.url_params["date"]
        context["search_result"] = self.search_result
        context["search_term"] = self.url_params["search"]
        context["current_page"] = self.url_params["page"]
        context["date_from"] = self.url_params["date_from"]
        context["date_to"] = self.url_params["date_to"]
        context["all_dates"] = self.all_dates
        context["url_params"] = self.url_params
        return context


class SearchRecordDetailView(SearchView):
    url_name = "hkm_search_record"
    template_name = "hkm/views/search_record.html"

    page_size = 1
    use_detailed_query = True

    def get(self, request, *args, **kwargs):
        return super().get(request, record=True, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if request.user.is_authenticated():
            if action == "add-to-collection":
                return self.handle_add_to_collection(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def handle_add_to_collection(self, request, *args, **kwargs):
        record_id = request.POST.get("record_id", None)
        if not record_id:
            LOG.warning("Record ID missing")
            return http.HttpResponseBadRequest()

        collection_id = request.POST.get("collection_id", None)
        if collection_id:
            try:
                collection = request.user.collections.get(id=collection_id)
            except Collection.DoesNotExist:
                LOG.warning(
                    "Invalid collection id",
                    extra={"data": {"collection_id": collection_id}},
                )
                return http.HttpResponseBadRequest()
        else:
            new_collection_name = request.POST.get("new_collection_name", None)
            if not new_collection_name:
                LOG.warning("New collection name missing")
                return http.HttpResponseBadRequest()
            collection = Collection(owner=request.user, title=new_collection_name)
            collection.save()

        record = Record(
            collection=collection, record_id=record_id, creator=request.user
        )
        record.save()

        url = reverse("hkm_search_record")
        url += "?search=%s&page=%d" % (
            self.url_params["search"],
            self.url_params["page"],
        )
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.record:
            record = self.record
            record["full_res_url"] = FINNA.get_full_res_image_url(record["id"])
            related_collections_ids = Record.objects.filter(
                record_id=record["id"]
            ).values_list("collection", flat=True)
            related_collections = (
                Collection.objects.user_can_view(self.request.user)
                .filter(id__in=related_collections_ids)
                .distinct()
            )

            context["related_collections"] = related_collections
            context["previous_record"] = self.previous_record
            context["record"] = record
            context["next_record"] = self.next_record
            context["hkm_id"] = record["id"]
            context["single_image"] = self.single_image
            LOG.debug("record id", extra={"data": {"finnaid": record["id"]}})
            context["record_web_url"] = FINNA.get_image_url(record["id"])
        if self.request.user.is_authenticated():
            context["my_collections"] = Collection.objects.filter(
                owner=self.request.user
            ).order_by("title")
        else:
            context["my_collections"] = Collection.objects.none()
        # calculate search result page to return to
        if self.record is None:
            context["search_result"] = None
            context["record"] = None
        context["search_result_page"] = int(
            math.ceil(float(self.url_params["page"]) / RESULTS_PER_PAGE)
        )
        return context

    def get_empty_forms(self, request):
        context_forms = super().get_empty_forms(request)
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        context_forms["feedback_form"] = forms.FeedbackForm(
            prefix="feedback-form", user=user
        )
        return context_forms


# This is needed for CreateOrderView
class BaseFinnaRecordDetailView(BaseView):
    record_finna_id = None
    record = None

    def get_url(self):
        return reverse(self.url_name, kwargs={"finna_id": self.record_finna_id})

    def setup(self, request, *args, **kwargs):
        self.record_finna_id = kwargs.get("finna_id", None)
        if self.record_finna_id:
            record_data = FINNA.get_record(self.record_finna_id)
            if record_data and "records" in record_data:
                self.record = record_data["records"][0]
                self.record["full_res_url"] = FINNA.get_full_res_image_url(
                    self.record["id"]
                )
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["record"] = self.record

        if self.request.user.is_authenticated():
            context["my_collections"] = Collection.objects.filter(
                owner=self.request.user
            ).order_by("title")
        else:
            context["my_collections"] = Collection.objects.none()

        return context


class SignUpView(BaseView):
    template_name = "hkm/views/signup.html"
    url_name = "hkm_signup"


class LanguageView(RedirectView):
    def get(self, request, *args, **kwargs):
        lang = request.GET.get("lang", "fi")
        if not lang in ("fi", "en", "sv"):
            lang = "fi"
        if request.user.is_authenticated():
            profile = request.user.profile
            profile.language = lang
            profile.save()
        request.session[LANGUAGE_SESSION_KEY] = lang
        self.request.session["seen_welcome_modal"] = False
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.GET.get("next", "/")


class AjaxUserFavoriteRecordView(View):
    def post(self, request, *args, **kwargs):
        record_id = request.POST.get("record_id", None)
        action = request.POST.get("action", "add")
        favorites_collection, created = Collection.objects.get_or_create(
            owner=request.user,
            collection_type=Collection.TYPE_FAVORITE,
            defaults={
                "title": _("Favorites"),
                "description": _("Your favorite pictures are collected here"),
            },
        )

        if record_id:
            if action == "add":
                record = Record(
                    creator=request.user,
                    collection=favorites_collection,
                    record_id=record_id,
                )
                record.save()
            elif action == "remove":
                # There shouldn't be multiple rows for same record, but if
                # there is, delete all
                records = favorites_collection.records.filter(record_id=record_id)
                records.delete()
            return http.HttpResponse()
        return http.HttpResponseBadRequest()


class AjaxCropRecordView(View):
    record_id = None
    action = None
    crop_x = None
    crop_y = None
    crop_width = None
    crop_height = None
    img_width = None
    img_height = None

    record = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.action = request.POST["action"]
            self.record_id = request.POST["record_id"]
            self.crop_x = float(request.POST["x"])
            self.crop_y = float(request.POST["y"])
            self.crop_width = float(request.POST["width"])
            self.crop_height = float(request.POST["height"])
            self.img_width = float(request.POST["original_width"])
            self.img_height = float(request.POST["original_height"])
        except KeyError:
            LOG.error(
                "Missing POST params", extra={"data": {"POST": repr(request.POST)}}
            )
        else:
            record_data = FINNA.get_record(self.record_id)
            if record_data:
                self.record = record_data["records"][0]
                self.record["full_res_url"] = FINNA.get_full_res_image_url(
                    self.record["id"]
                )
                return super().dispatch(request, *args, **kwargs)
            else:
                LOG.error("Could not get record data")
        return http.HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        if self.action == "download":
            return self.handle_download(request, *args, **kwargs)
        return http.HttpResponseBadRequest()

    def _get_cropped_full_res_file(self):
        try:
            full_res_image = FINNA.download_image(self.record["id"])
        except:
            return None
        cropped_image = image_utils.crop(
            full_res_image,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
            self.img_width,
            self.img_height,
        )
        crop_io = io.BytesIO()
        cropped_image.save(crop_io, format=full_res_image.format)
        crop_io.seek(0)
        filename = "%s.%s" % (self.record["title"], full_res_image.format.lower())
        LOG.debug("Cropped image", extra={"data": {"size": repr(cropped_image.size)}})

        return InMemoryUploadedFile(
            crop_io, None, filename, full_res_image.format, None, None
        )

    def _get_cropped_preview_file(self):
        full_res_image = FINNA.download_image(self.record["id"])
        cropped_image = image_utils.crop(
            full_res_image,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
            self.img_width,
            self.img_height,
        )
        crop_io = io.BytesIO()
        cropped_image.save(crop_io, format=full_res_image.format)
        crop_io.seek(0)
        filename = "%s.%s" % (self.record["title"], full_res_image.format.lower())
        LOG.debug("Cropped image", extra={"data": {"size": repr(cropped_image.size)}})
        return InMemoryUploadedFile(
            crop_io, None, filename, full_res_image.format, None, None
        )

    def handle_download(self, request, *args, **kwargs):
        crop_file = self._get_cropped_full_res_file()
        if not crop_file:
            crop_file = self._get_cropped_preview_file()

        tmp_image = TmpImage(
            record_id=self.record_id, record_title=self.record["title"]
        )

        # Remove non-english letters from file name to prevent a crash when saving to Azure storage

        file_name = unidecode(crop_file.name.encode("utf-8").decode("utf-8"))
        tmp_image.edited_image.save(file_name, crop_file)

        if request.user.is_authenticated():
            tmp_image.creator = request.user

        tmp_image.save()
        LOG.debug("Cropped image", extra={"data": {"url": tmp_image.edited_image.url}})
        return http.JsonResponse({"url": tmp_image.edited_image.url})


class AjaxAddToCollection(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            action = request.POST["action"]
            if action == "add":
                return self.handle_add_to_collection(request, *args, **kwargs)
            elif action == "add-create-collection":
                return self.handle_add_to_new_collection(request, *args, **kwargs)
        return http.HttpResponseBadRequest()

    def handle_add_to_collection(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.filter(owner=request.user).get(
                id=request.POST["collection_id"]
            )
        except (KeyError, Collection.DoesNotExist):
            LOG.error("Could not get collection")
        else:
            record = Record(
                creator=request.user,
                collection=collection,
                record_id=request.POST["record_id"],
            )
            record.save()
            return http.HttpResponse()
        return http.HttpResponseBadRequest()

    def handle_add_to_new_collection(self, request, *args, **kwargs):
        collection = Collection(
            owner=request.user, title=request.POST["collection_title"]
        )
        collection.save()
        record = Record(
            creator=request.user,
            collection=collection,
            record_id=request.POST["record_id"],
        )
        record.save()
        return http.HttpResponse()


# VIEWS THAT SITE FOOTER LINKS TO
class TranslatableContentView(BaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["page_content"] = PageContent.objects.get(identifier=self.url_name)
        except PageContent.DoesNotExist:
            context["page_content"] = None
        return context


class SiteinfoAboutView(TranslatableContentView):
    template_name = "hkm/views/siteinfo_about.html"
    url_name = "hkm_siteinfo_about"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteinfoAccessibilityView(TranslatableContentView):
    template_name = "hkm/views/siteinfo_accessibility.html"
    url_name = "hkm_siteinfo_accessibility"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteinfoPrivacyView(TranslatableContentView):
    template_name = "hkm/views/siteinfo_privacy.html"
    url_name = "hkm_siteinfo_privacy"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteinfoQAView(TranslatableContentView):
    template_name = "hkm/views/siteinfo_QA.html"
    url_name = "hkm_siteinfo_QA"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteinfoTermsView(TranslatableContentView):
    template_name = "hkm/views/siteinfo_terms.html"
    url_name = "hkm_siteinfo_terms"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RecordFeedbackView(View):
    name = "hkm_record_feedback"

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "feedback":
            return self.handle_feedback(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def handle_feedback(self, request, *args, **kwargs):
        response_data = {}
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        form = forms.FeedbackForm(request.POST, user=user)
        if form.is_valid():
            record = request.POST.get("hkm_id", "")
            feedback = form.save(commit=False)
            feedback.record_id = record
            path = "/info/" if not record else "/search/details/?image_id=" + record
            feedback.sent_from = "".join([request.get_host(), path])
            feedback.save()
            email.send_feedback_notification(feedback.id)

            response_data["result"] = "Success"
            return http.HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            response_data["result"] = "Error"
            return http.HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )


class LegacyRecordDetailView(RedirectView):
    """This class provides backward compatibility for links to Finna images written
    as /record/<finna_id>/. It just redirects to the current implementation of the
    details view using a 301 redirect."""

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        base_url = reverse("hkm_search_record")
        query_string = urlencode({"image_id": kwargs["finna_id"]})
        url = "{}?{}".format(base_url, query_string)

        return url


class PasswordResetConfirmViewNew(PasswordResetConfirmView, HomeView):
    url_name = "reset_pwd"
    template_name = "hkm/views/home_page.html"

    def get_empty_forms(self, request, **kwargs):
        return {"password_set_form": self.form_class(user=kwargs.get("user"))}

    def get(self, request, *args, **kwargs):
        _kwargs = self.get_empty_forms(request, **kwargs)
        _kwargs.update(kwargs)
        return self.render_to_response(self.get_context_data(**_kwargs))

    def post(self, request, *args, **kwargs):
        errors = {}

        form = self.form_class(data=request.POST, user=self.user)
        if form.is_valid():
            auth_login(request, form.save())
            return http.HttpResponse()
        else:
            for key in form.errors:
                errors["error_message"] = str(form.errors[key])
            return http.HttpResponseBadRequest(json.dumps(errors), "application/json")


# ERROR HANDLERS


def handler404(request):
    context = {}
    context["language"] = request.session.get(
        LANGUAGE_SESSION_KEY, settings.LANGUAGE_CODE
    )
    response = render_to_response("hkm/views/404.html", context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    context["language"] = request.session.get(
        LANGUAGE_SESSION_KEY, settings.LANGUAGE_CODE
    )
    response = render_to_response("hkm/views/500.html", context)
    response.status_code = 500
    return response
