from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class DictBase(models.Model):  # базовый класс для справочников
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:  # указываем, что таблицу создавать не надо
        abstract = True

    def __str__(self):
        return self.name


class OperationType(DictBase):  # тип операции, наследуемся от базового
    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'
        # гарантируем уникальность имен и слагов по таблице
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_type_name'),
            models.UniqueConstraint(fields=['slug'], name='unique_type_slug'),
        ]


class Status(DictBase):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_status_name'),
            models.UniqueConstraint(
                fields=['slug'], name='unique_status_slug'),
        ]


class Category(DictBase):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_category_name'),
            models.UniqueConstraint(
                fields=['slug'], name='unique_category_slug'),
        ]
# привязка к типу
    operation_type = models.ForeignKey(
        OperationType, on_delete=models.RESTRICT, related_name='categories', null=False, blank=False)


class SubCategory(DictBase):
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_subcategory_name'),
            models.UniqueConstraint(
                fields=['slug'], name='unique_subcategory_slug'),
        ]
# привязка к категории
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name='subcategories', null=False, blank=False)


class CashFlow(models.Model):
    created_at = models.DateField(default=timezone.now)
    status = models.ForeignKey(
        Status, on_delete=models.RESTRICT, related_name='records')
    operation_type = models.ForeignKey(
        OperationType, on_delete=models.RESTRICT, related_name='records', null=False, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name='records', null=False, blank=False)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.RESTRICT, related_name='records', null=False, blank=False)
    # проверяем, что сумма корректна
    amount = models.DecimalField(validators=[MinValueValidator(0)],
                                 max_digits=10, decimal_places=2, help_text='Сумма в рублях', null=False, blank=False)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'
        # создаем индексы для быстрого поиска и фильтрации
        indexes = [
            models.Index(fields=['created_at'], name='created_at_idx'),
            models.Index(fields=['status'], name='status_idx'),
            models.Index(fields=['operation_type'], name='operation_type_idx'),
            models.Index(fields=['category'], name='category_idx'),
            models.Index(fields=['subcategory'], name='subcategory_idx'),
        ]

# функция для валидации
    def clean(self):
        errors = {}
        if self.category and self.operation_type and self.category.operation_type_id != self.operation_type_id:
            errors["category"] = "Категория принадлежит другому типу операции"
            errors["operation_type"] = "Тип операции не соответствует категории"
        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            errors["subcategory"] = "Подкатегория принадлежит другой категории"
            errors["category"] = "Категория не соответствует подкатегории"
        if self.amount is not None and self.amount < 0:
            errors["amount"] = "Сумма не может быть отрицательной"
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.created_at} | {self.status} | {self.operation_type} | {self.category} | {self.subcategory} | {self.amount} | {self.comment}"
