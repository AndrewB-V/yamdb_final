from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Категория',
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        help_text='Укажите слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def str(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Жанр',
        help_text='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        help_text='Укажите слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def str(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Произведение',
        help_text='Введите название произведения',
        db_index=True
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Введите год выпуска',
        validators=[validate_year],
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание произведения',
        max_length=250,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Укажите категорию'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def str(self):
        return self.name[:15]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        max_length=200,
        related_name='reviews',
        verbose_name='Название',
        help_text='Укажите название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        max_length=50,
        related_name='reviews',
        verbose_name='автор',
        help_text='Укажите автора'
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        help_text='Дата публикации',
        verbose_name='Укажите дату публикации',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Укажите оценку произведения',
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
        ),
        error_messages={'validators': 'Оценка может быть от 1 до 10'}
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='review',
        )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        max_length=200,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Оставьте свой отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        max_length=50,
        related_name='comments',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    text = models.CharField(
        verbose_name='Комментарий',
        help_text='Введите текст комментария',
        max_length=150
    )
    pub_date = models.DateTimeField(
        help_text='Дата публикации',
        verbose_name='Укажите дату публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.review}, {self.text}'
