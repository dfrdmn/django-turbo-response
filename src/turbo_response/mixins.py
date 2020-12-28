# Local
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TurboTemplatePartialResolverMixin:

    """Attempts to guess name of template based on prefix.
    For example, if your template is "todos/todo_form.html"
    then `get_partial_template_names()` will return
    "todos/_todo_form.html".
    """

    partial_template_prefix = "_"
    turbo_stream_template_name = None

    def get_partial_template_names(self):
        def resolve_name(name):
            start, part, end = name.rpartition("/")
            return "".join([start, part, self.partial_template_prefix, end])

        return [resolve_name(name) for name in self.get_template_names()]

    def get_turbo_stream_template_names(self):
        return [self.turbo_stream_template] or self.get_partial_template_names()


class TurboStreamResponseMixin:
    turbo_stream_action = None
    turbo_stream_target = None

    content_type = "text/html; turbo-stream; charset=utf-8"

    def get_turbo_stream_action(self):
        return self.turbo_stream_action

    def get_turbo_stream_target(self):
        return self.turbo_stream_target

    def get_response_content(self):
        return ""

    def render_turbo_stream_response(self):

        return TurboStreamResponse(
            action=self.get_turbo_stream_action(),
            target=self.get_turbo_stream_target(),
            content=self.get_response_content(),
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Use with ContextMixin subclass"""

    def render_turbo_stream_response(self, **context):
        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            target=self.get_turbo_stream_target(),
            action=self.get_turbo_stream_action(),
            context=self.get_context_data(**context),
            using=self.template_engine,
        )


class TurboStreamFormMixin(TurboTemplatePartialResolverMixin):
    def form_invalid(self, form):
        return self.render_turbo_stream_response(form=form)


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self):
        return self.turbo_frame_dom_id

    def get_response_content(self):
        return ""

    def render_turbo_frame_response(self):
        return TurboFrameResponse(
            self.get_response_content(), dom_id=self.get_turbo_frame_dom_id(),
        )


class TurboFrameTemplateResponseMixin:
    """Use with ContextMixin subclass"""

    def render_turbo_frame_response(self, **context):
        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=self.get_turbo_frame_params(),
            context=self.get_context_data(context),
            using=self.template_engine,
        )
