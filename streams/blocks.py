"""Streamfields live in here."""

from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailmarkdown.blocks import MarkdownBlock

from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name 


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:  # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
        
        
        
class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="If the button page above is selected, that will be used first.")),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"
        


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"
        
class CTABlock(blocks.StructBlock):
    """A simple call to action section."""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action" 
        
        
class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue  
        
        
class BlockQuoteBlock(blocks.TextBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html(
                '<blockquote>{0}</blockquote>', mark_safe(value))
        else:
            return ''

    class Meta:
        icon = "openquote"
        
class InlineVideoBlock(blocks.StructBlock):
    video = EmbedBlock(label=_("Video"))
    caption = CharBlock(required=False, label=_("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', _("Right")), ('left', _("Left")), ('center', _("Center"))],
        default='right',
        label=_("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', _("Small")), ('medium', _("Medium")), ('large', _("Large"))],
        default='small',
        label=_("Size"),
    )

    class Meta:
        template = 'streams/video_block.html'
        icon = 'media' 
        
        


# class CodeBlock(blocks.StructBlock):
#     """
#     Code Highlighting Block
#     """
#     LANGUAGE_CHOICES = (
#         ('python', 'Python'),
#         ('bash', 'Bash/Shell'),
#         ('html', 'HTML'),
#         ('css', 'CSS'),
#         ('scss', 'SCSS'),
#         ('json', 'JSON'),
#     )

#     STYLE_CHOICES = (
#         ('syntax', 'syntax'),
#         ('emacs', 'emacs'),
#         ('monokai', 'monokai'),
#         ('vim', 'vim'),
#         ('xcode', 'xcode'),
#     )

#     language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES)
#     style = blocks.ChoiceBlock(choices=STYLE_CHOICES, default='xcode')
#     code = blocks.TextBlock()

#     def render(self, value, context=None):
#         src = value['code'].strip('\n')
#         lang = value['language']
#         lexer = get_lexer_by_name(lang)
#         #css_classes = ['code', value['style']]

#         formatter = get_formatter_by_name(
#             'html',
#             linenos=None,
#             #cssclass=' '.join(css_classes),
#             style='xcode',
#             #cssclass = 'codehilite',
#             noclasses=False,
#         )
#         return mark_safe(highlight(src, lexer, formatter))

#     class Meta:
#         icon = 'code'
        
        
class MarkDownBlock(MarkdownBlock):
    h1 = CharBlock()
    h2 = CharBlock()
    
    paragrah = RichtextBlock()
    markdown = MarkdownBlock(icon = "placeholder")       
                 
                                 
