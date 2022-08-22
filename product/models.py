from django.db import models
from cloudinary.models import CloudinaryField

CATEGORY_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women'),
)

SIZE_CHOICES = ( 
    ('3', 'UK3'),
    ('4', 'UK4'),
    ('5', 'UK5'),
    ('6', 'UK6'),
    ('7', 'UK7'),
    ('8', 'UK8'),
    ('9', 'UK9'),
    ('10', 'UK10'),
    ('11', 'UK11'),
    ('12', 'UK12'),
    ('13', 'UK13'),
    ('14', 'UK14'),
    ('15', 'UK15'),
    ('16', 'UK16')
)

class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    
    def __str__(self):
        return f'{self.id} {self.name}'  
    
    def get_absolute_url(self):
        return f'/{self.category}/{self.slug}/'  

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True, null=True)

    def get_image(self):
        if self.image:
            return self.image.url
        return ''

    def __str__(self):
        return f'{self.id} {self.product.name}'

class ProductStock(models.Model):
    product = models.ForeignKey(Product, related_name="product_stock", 
                                on_delete=models.CASCADE, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=10)
    amount_in_stock = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'],
                name='unique_prod_size_combo'
            )
        ]

    def __str__(self):
        return f'x{self.amount_in_stock} {self.product.name} size: {self.size}'



