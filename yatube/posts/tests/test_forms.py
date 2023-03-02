from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostsFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем запись в базе данных для проверки сушествующего slug
        cls.user = User.objects.create_user(username='AnotherSadUser')
        cls.group = Group.objects.create(
            title='Test',
            slug='Test',
            description='Test',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Test',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем создание поста
    def test_create_post_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
            'group': PostsFormTests.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(
            response, reverse('posts:profile',
                              kwargs={
                                  'username': PostsFormTests.user.username}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с нашим слагом
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
            ))

    # Проверяем внесение изменений в пост
    def test_edit_post_form(self):
        new_text = 'Update test'
        post = PostsFormTests.post
        self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id': PostsFormTests.post.pk}),

            data={'text': new_text},
        )
        self.assertEqual(new_text, Post.objects.get(pk=post.pk).text)