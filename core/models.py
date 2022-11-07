from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'


class Pedido(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.id




class Cajero(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title


#Bowls

class ProteinaBowl(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(null=True)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class BaseBowl(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class SalsaBowl(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ExtraBowl(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(null=True,default=0)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Bowl(models.Model):
    proteina = models.ForeignKey(ProteinaBowl, on_delete=models.CASCADE, null=True, blank=True)
    base = models.ForeignKey(BaseBowl, on_delete=models.CASCADE,null=True, blank=True)
    salsa1 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.salsa1+')
    salsa2 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.salsa2+')
    extra1 = models.ForeignKey(ExtraBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra1+')
    extra2 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra2+')
    extra3 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra3+')
    extra4 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra4+')
    extra5 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra5+')
    extra6 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra6+')
    extra7 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra7+')
    extra8 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra8+')
    extra9 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra9+')
    extra10 = models.ForeignKey(SalsaBowl, on_delete=models.CASCADE,null=True, blank=True,related_name='Kai.extra10+')
    state = models.BooleanField(default=True)    
    typ = models.CharField(max_length=50,default='b')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return str(self.id)
    

#Handrolls
class ProteinaHandroll(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class VegetalesHandroll(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Handroll(models.Model):
    proteina1 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.proteina1+')
    proteina2 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.proteina2+')
    proteina3 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.proteina3+')
    vegetal1 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.vegetal1+')
    vegetal2 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.vegetal2+')
    vegetal3 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='Handroll.vegetal3+')
    state = models.BooleanField(default=True)    
    typ = models.CharField(max_length=50,default='h')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return str(self.id)+typ


class HandrollReady(models.Model):
    name = models.CharField(max_length=50)
    proteina1 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.proteina1+')
    proteina2 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.proteina2+')
    proteina3 = models.ForeignKey(ProteinaHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.proteina3+')
    vegetal1 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.vegetal1+')
    vegetal2 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.vegatal2+')
    vegetal3 =models.ForeignKey(VegetalesHandroll, on_delete=models.CASCADE, null=True, blank=True,related_name='HandrollReady.vegetal3+')
    state = models.BooleanField(default=True)    
    price = models.PositiveIntegerField(default=0,null=True, blank=True)
    typ = models.CharField(max_length=50,default='hc')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.name

#Almuerzo/Lunch
class ProteinaAlmuerzo(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class AgregadoAlmuerzo(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Almuerzo(models.Model):
    proteina = models.ForeignKey(ProteinaAlmuerzo, on_delete=models.CASCADE)
    agregado = models.ForeignKey(AgregadoAlmuerzo, on_delete=models.CASCADE)
    typ = models.CharField(max_length=50,default='al')
    time = models.FloatField(null=True,default=0)
    price = models.PositiveIntegerField(null=True,default=0)
    state = models.BooleanField(default=True)


    def __str__(self):
        return str(self.proteina.name)+' c/ '+str(self.agregado.name)


#Desayuno/Breakfast
class QuesoDesayuno(models.Model):
    name = models.CharField(max_length=50)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ProteinaDesayuno(models.Model):
    name = models.CharField(max_length=50)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class VegetalesDesayuno(models.Model):
    name = models.CharField(max_length=50)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Desayuno(models.Model):
    queso = models.ForeignKey(QuesoDesayuno, on_delete=models.CASCADE)
    proteina = models.ForeignKey(ProteinaDesayuno, on_delete=models.CASCADE)
    vegetal1 = models.ForeignKey(VegetalesDesayuno, on_delete=models.CASCADE,related_name='Desayuno.vegetal1+')
    vegetal2 = models.ForeignKey(VegetalesDesayuno, on_delete=models.CASCADE,related_name='Desayuno.vegetal2+')
    state = models.BooleanField(default=True)
    typ = models.CharField(max_length=50,default='des')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return 'des '+str(self.id)

#Selladitas
class Selladitas(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(null=True,default=0)
    state = models.BooleanField(default=True)
    typ = models.CharField(max_length=50,default='sell')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.name


#PromoKai
class CorteKai(models.Model):
    num = models.PositiveIntegerField()
    envoltorio = models.CharField(max_length=50)

    def __str__(self):
        return str(self.num)+' cortes de '+self.envoltorio

class ExtraKai(models.Model):
    num = models.PositiveIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.num)+' '+self.name


class Kai(models.Model):
    name = models.CharField(max_length=50)
    corte1 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte1+')
    corte2 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte2+')
    corte3 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte3+')
    corte4 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte4+')
    corte5 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte5+')
    corte6 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte6+')
    corte7 = models.ForeignKey(CorteKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.corte7+')
    extra1 = models.ForeignKey(ExtraKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.extra1+')
    extra2 = models.ForeignKey(ExtraKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.extra2+')
    extra3 = models.ForeignKey(ExtraKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.extra3+')
    extra4 = models.ForeignKey(ExtraKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.extra4+')
    extra5 = models.ForeignKey(ExtraKai, on_delete=models.CASCADE,blank=True,null=True,related_name='Kai.extra5+')
    price = models.PositiveIntegerField(null=True,default=0)
    typ = models.CharField(max_length=50,default='kai')
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.name


class Article(models.Model):
    cod = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    total = models.CharField(max_length=50)
    cantidad = models.CharField(max_length=50)
    time = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.cod


class Comanda(models.Model):
    cod = models.IntegerField(null=True, blank=True)
    article = models.ManyToManyField(Article)
    cooking = models.BooleanField(default=False)
    time_to_kitchen = models.DateTimeField(null=True,blank=True)
    finished = models.BooleanField(default=False)
    time_finished = models.DateTimeField(null=True,blank=True)
    author = models.CharField(max_length=50,null=True,blank=True)
    time = models.FloatField(null=True,default=0)
    
    coments = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return str(self.id)

    def toScns(self):
        start = self.time_to_kitchen
        end = self.time_finished
        if start is None or end is None:
            
            a = 'Pedido no finalizado'
            return a
        else:
            dif = end-start
            res = dif
            return 