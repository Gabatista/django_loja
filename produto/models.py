from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(default='V',max_length=1,choices=(('V', 'Variação'),('S', 'Simples'),))
    
    def __str__(self):
        return self.nome

    @staticmethod
    def resize_image(img, new_width=800):
        img_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pill = Image.open(img_path)
        original_width, original_height = img_pill.size

        if original_width <= new_width:
            img_pill.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pill.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_path,
            optimized=True,
            quality=50
        )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)



class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promo = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

