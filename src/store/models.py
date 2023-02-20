from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    in_store = models.BooleanField(default=True)
    img = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    rating = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='review')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    time_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000)

    def __str__(self):
        return f'user - {self.user} product - {self.product}'


class ProductInfo(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_info')

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'


class RatingProductStar(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'product - {self.product} star - {self.star} count - {self.count}'


class RatingUserProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)

    def __str__(self):
        return f'user - {self.user} product - {self.product}'


class Basket(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'user - {self.user}'


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'basket - {self.basket} product - {self.product} count - {self.count}'


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name
