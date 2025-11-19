from django.db import models


class City(models.Model):
    """
    Город отправления/прибытия.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Код города"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название города"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Order(models.Model):
    """
    Заказ пользователя.
    """
    route_id = models.CharField(
        max_length=100,
        verbose_name="ID маршрута"
    )
    passenger_name = models.CharField(
        max_length=255,
        verbose_name="Пассажир"
    )
    status = models.CharField(
        max_length=32,
        default="created",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заказ #{self.id} ({self.passenger_name})"


class Ticket(models.Model):
    """
    Билет, привязанный к заказу.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="ticket",
        verbose_name="Заказ"
    )
    qr_data = models.CharField(
        max_length=255,
        verbose_name="Данные QR"
    )
    status = models.CharField(
        max_length=32,
        default="active",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Билет #{self.id} для заказа #{self.order_id}"


class GarsRawEntity(models.Model):
    """
    Универсальный кэш записей из ГАРС.
    """
    entity_type = models.CharField(
        max_length=255,
        verbose_name="Тип сущности (коллекция OData)"
    )
    ref_key = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Ключ записи (Ref_Key)"
    )
    payload = models.JSONField(
        verbose_name="Полный JSON записи OData"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Сырая запись ГАРС"
        verbose_name_plural = "Сырые записи ГАРС"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.entity_type} / {self.ref_key}"
