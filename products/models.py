import datetime
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.utils.timezone import utc

class AvatarP(models.Model):

    producte = models.ForeignKey("Producte", verbose_name=_("producte"), on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(_("avatar"), upload_to='product_avatar/')

    def __str__(self):
        return self.avatar.name

    class Meta:
        managed = True
        verbose_name = 'AvatarP'
        verbose_name_plural = 'AvatarP'

class AvatarC(models.Model):

    category = models.ForeignKey("category", verbose_name=_("category"), on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(_("avatar"), upload_to='category_avatar/')

    def __str__(self):
        return self.category.title

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'AvatarC'
        verbose_name_plural = 'AvatarC'

class Comment(models.Model):

    user = models.ForeignKey("accounts.Account", verbose_name=_("user"), on_delete=models.CASCADE, related_name='comment')
    producte = models.ForeignKey("Producte", verbose_name=_("product"), on_delete=models.CASCADE, related_name='comment')
    describtion = models.TextField(_("describtion"))
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)

    def __str__(self):
        return self.describtion

    class Meta:
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Producte(models.Model):

    category = models.ForeignKey("category", verbose_name=_("category"), on_delete=models.CASCADE, related_name='product')
    title = models.CharField(_("title"), max_length=150)
    describtion = models.TextField(_("describtion"), blank=True, null=True)
    price = models.PositiveIntegerField(_("price"))
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    user = models.ForeignKey("accounts.Account", verbose_name=_("user"), on_delete=models.CASCADE, related_name='product', null=True, blank=True)
    off = models.PositiveSmallIntegerField(_("off"), default=0)
    count = models.PositiveSmallIntegerField(_("count"))

    @property
    def t(self):
        return self.category.title

    def time_diff(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created_time
        return timediff.days
        
    def master_price(self):
        return int(round(self.price - self.price*self.off/100))

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Producte'
        verbose_name_plural = 'Productes'

class Category(models.Model):

    parent = models.ForeignKey("self", verbose_name=_("category"), on_delete=models.CASCADE, related_name='category', blank=True, null=True)
    title = models.CharField(_("title"), max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Buy(models.Model):

    product = models.ForeignKey("producte", verbose_name=_("product"), on_delete=models.CASCADE, related_name='buy')
    user = models.ForeignKey("accounts.Account", verbose_name=_("user"), on_delete=models.CASCADE, related_name='buy')
    is_purchase = models.BooleanField(_("purchase"))

    def __str__(self):
        return self.product.title

    class Meta:
        managed = True
        verbose_name = 'Buy'
        verbose_name_plural = 'Buies'