from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='SadStudent')
        cls.other_user = User.objects.create_user(username="Someone")
        cls.group = Group.objects.create(
            title='Тестовая',
            slug='test',
            description='Тестовое',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {

            'posts/index.html': reverse('posts:index'),
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/profile.html': reverse('posts:profile',
             kwargs={'username': self.user.username}),
            'posts/group_list.html': reverse('posts:group_list',
             kwargs={'slug': 'test'}),
            'posts/post_detail.html': (reverse('posts:post_detail',
             kwargs={'post_id': self.post.pk})),
            'posts/profile.html': reverse('posts:profile',
             kwargs={'username': self.post.author}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def post_show_on_pages(self, page_context):
        post_author = page_context.author
        post_group = page_context.group
        post_text = page_context.text
        self.assertEqual(post_author, PostPagesTests.post.author)
        self.assertEqual(post_group, PostPagesTests.post.group)
        self.assertEqual(post_text, PostPagesTests.post.text)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(reverse('posts:index'))
        )
        page_cont = response.context['page_obj'][0]
        self.post_show_on_pages(page_cont)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': PostPagesTests.group.slug})
        )
        post_group = response.context['group']
        self.assertEqual(post_group, PostPagesTests.group)
        page_cont = response.context['page_obj'][0]
        self.post_show_on_pages(page_cont)

    def test_profile_page_show_correct_context(self):
        """Шаблон Profile сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': PostPagesTests.user.username})
        )
        profile_context = response.context
        post_profile = profile_context['author']
        self.assertEqual(post_profile, PostPagesTests.user)
        page_cont = response.context['page_obj'][0]
        self.post_show_on_pages(page_cont)

    # Проверка словаря контекста страницы Create Post
    def test_create_post_page_show_correct_context(self):
        """Шаблон Create_Post сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields[value]
                self.assertIsInstance(form_field, expected)

    # Проверка словаря контекста страницы Edit Post
    def test_edit_post_page_show_correct_context(self):
        """Шаблон Edit_Post сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': PostPagesTests.post.pk}
                    )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                forms_field = response.context.get('form').fields[value]
                self.assertIsInstance(forms_field, expected)

    # Проверка словаря контекста страницы Post Detail
    def test_post_detail_page_show_correct_context(self):
        """Шаблон Post_Detail сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': PostPagesTests.post.pk
                            }
                    )
        )
        post_detail_context = response.context
        post_detail = post_detail_context['post']
        self.assertEqual(post_detail, PostPagesTests.post)
        self.post_show_on_pages(post_detail)
