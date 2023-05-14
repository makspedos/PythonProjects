from itertools import product

from django.db import models
from django.contrib import admin
from django.db.models.signals import post_save


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MeasuredUnit(models.Model):
    measured_unit_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'measured_unit'


class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'product_category'
        verbose_name_plural = 'product_category'

    def __str__(self):
        return self.name


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=24, null=False, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.status_name


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, null=True, default=None)
    address = models.CharField(max_length=20, null=True, default=None)
    number = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'customers'
        verbose_name_plural = 'customers'


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_id = models.AutoField(primary_key=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=None)
    payment_type = models.CharField(max_length=25, default='Cash')
    order_timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    delivery_type = models.CharField(max_length=50)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        managed = True
        db_table = 'orders'
        verbose_name_plural = 'orders'



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    size = models.IntegerField()
    brand = models.CharField(max_length=20)
    amount = models.IntegerField()
    product_info = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    product_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, default=None)
    measured_unit = models.ForeignKey(MeasuredUnit, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.product_name)
    class Meta:
        managed = True
        db_table = 'product'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    product_image = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'product_image'

    def __str__(self):
        return str(self.id)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    count = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.product.product_name

    class Meta:
        managed = True
        db_table = 'ProductInOrder'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        total_price = price_per_item * int(self.count)
        self.total_price = total_price

        return super(ProductInOrder, self).save(*args, **kwargs)


class Basket(models.Model):
    session_key = models.CharField(max_length=128,blank=True, null=True, default=None)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    count = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.product.product_name

    class Meta:
        managed = True
        db_table = 'Basket'

    def save(self, is_active=None, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        total_price = price_per_item * int(self.count)
        self.total_price = total_price
        if is_active is not None:
            self.is_active=False
        return super(Basket, self).save(*args, **kwargs)


def product_in_order_post_save(instance, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)
