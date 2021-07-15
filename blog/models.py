
"""Blog listing and blog detail pages."""
from django import forms

from django.utils.translation import gettext_lazy as _
#from django.core.cache import cache
#from django.core.cache.utils import make_template_fragment_key

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from rest_framework.fields import Field
from taggit.models import TaggedItemBase
from wagtail.api import APIField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.snippets.models import register_snippet
from wagtailcodeblock.blocks import CodeBlock 
from wagtail.images.blocks import ImageChooserBlock
#from wagtail_blocks.blocks import  ChartBlock, MapBlock

from streams import blocks
from streams.blocks import InlineVideoBlock, MarkDownBlock, ImageBlock, RawTextBlock, BlockQuoteBlock, ExternalLinkWithChildrenBlock, PageLinkWithChildrenBlock
 



class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]
    
    @property
    def author_name(self):
        return self.author.name

    @property
    def author_website(self):
        return self.author.website
    
    @property
    def author_biographie(self):
        return self.author.biographie
    
    @property
    def author_image(self):
        return self.author.image
    
    
    
    

    api_fields = [
        APIField("author_name"),
        APIField("author_website"),
        APIField("author_biographie"),
        # This is using a custom django rest framework serializer
        APIField("author_image", serializer=ImageSerializedField()), 
        # The below APIField is using a Wagtail-built DRF Serializer that supports
        # custom image rendition sizes
        APIField(
            "image",
            serializer=ImageRenditionField(
                'fill-200x250',
                source="author_image"
            )
        ),
         
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets."""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    biographie = models.TextField(max_length=255, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
                FieldPanel('biographie'),
            ],
            heading="Name, Image and Biographie ",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog catgory for a snippet."""

    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        ImageChooserPanel("icon"),
        
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


register_snippet(BlogCategory)




class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"
    ajax_template = "blog/blog_listing_page_ajax.html"
    
    max_count = 1
    subpage_types = ['blog.VideoBlogPage', 'blog.ArticleBlogPage']

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        
        paginator = Paginator(all_posts, 6)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        
        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()
        # context["author"]=posts.author
        return context
    
    @route(r"^february-2021/$", name="february-2021")
    @route(r"^year/(\d+)/(\d+)/$", name="blogs_by_year")
    def blogs_by_year(self, request, year=None, month=None):
        context = self.get_context(request)
        # Implement your BlogDetailPage filter. Maybe something like this:
        # if year is not None and month is not None:
        #     posts = BlogDetailPage.objects.live().public().filter(year=year, month=month)
        # else:
        #     # No year and no month were set, assume this is july-2019 only posts
        #     posts = BlogDetailPage.objects.live().public().filter(year=2019, month=07)
        # print(year)
        # print(month)
        # context["posts"] = posts

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/latest_posts.html", context)

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            # Look for the blog category by its slug.
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            # Redirect to self.url, return a 404.. that's up to you!
            category = None

        if category is None:
            # This is an additional check.
            # If the category is None, do something. Maybe default to a particular category.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass

        context["posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/latest_posts.html", context)

    
    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)
    
    def get_sitemap_urls(self, request):
        # Uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )    


class BlogDetailPage(Page):
    """Parental blog detail page."""
    
    subpage_types = []
    parent_page_types = ['blog.BlogListingPage']
    
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date",blank=False, null=True)
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    chapo = models.TextField(
        blank=True,
        null=True,
        help_text="A short summary of your article",
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    author_name = models.CharField(
        max_length=100, 
        blank=False, 
        null=True,
        help_text= "Name of the writer of the article for home page"
        
        )
    
    
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)


    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code','embed', 'blockquote', 'superscript', 'subscript', 'strikethrough'])),
            ("code", CodeBlock(label=_("Code"))),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ('video', InlineVideoBlock()),
            ("markdown", MarkDownBlock(icon="placeholder")),
            ("picture", ImageChooserBlock(icon="photo")),
            ("photo", blocks.ImageBlock(icon="photo", label="photo",)),
            ("RawTextBlock",RawTextBlock(label = "Raw Html", icon= "code")),
            #("chart", ChartBlock()),
            #("map", MapBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("chapo"),
        FieldPanel("tags"),
        FieldPanel("date"),
        FieldPanel("author_name"),
        ImageChooserPanel("banner_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        
        StreamFieldPanel("content"),
    ]
    
    api_fields = [
        APIField("blog_authors"),
        APIField("content"),
    ]
    
    # def save(self, *args, **kwargs):
    #     """Create a template fragment key.
    #     Then delete the key."""
    #     key = make_template_fragment_key(
    #         "blog_post_preview",
    #         [self.id]
    #     )
    #     cache.delete(key)
    #     return super().save(*args, **kwargs)

# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Subject of article in CAPITALS"

    )
    
    # article_summary=models.TextField(
    #     blank=False,
    #     null=False,
    #     help_text="A short summary of your article"
    # )
    
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )
    caption_intro_image = models.TextField(
        max_length=100,
        blank=False,
        null=True,
        help_text = "photo caption with  your © copyright",
        
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        FieldPanel("chapo"),
        FieldPanel("tags"),
        FieldPanel("date"),
        FieldPanel("author_name"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        FieldPanel("caption_intro_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]
    
        


# Second subclassed page
class VideoBlogPage(BlogDetailPage):
    """A video subclassed page."""

    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("chapo"),
        FieldPanel("tags"),
        FieldPanel('date'),
        ImageChooserPanel("banner_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("content"),
    ]     
    
# NavBar model  
class Navbar(models.Model):
    """
    Model that represents website navigation bars.  Can be modified through the
    snippets UI. 
    """
    name = models.CharField(max_length=255)
    menu_items = StreamField([
        ('external_link', ExternalLinkWithChildrenBlock()),
        ('page_link', PageLinkWithChildrenBlock()),
        ],)

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('menu_items')
    ]

    def __str__(self):
        return self.name

register_snippet(Navbar)


class PageWithNavbar(Page):
    navbar = models.ForeignKey(
        Navbar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels=[
        FieldPanel('title'),
        SnippetChooserPanel('navbar')
    ]

