from datetime import datetime
from django.db import models


# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    usa = models.BooleanField(default=True, verbose_name='USA')
    usb = models.BooleanField(default=True, verbose_name='USB')

    def __str__(self):
        return self.name


class Unidade(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')

    def save(self, *args, **kwargs):
        verification = False
        # este if serve para que a condição só seja executada em create
        if not self.id:
            verification = True
        # este if serve para que a condição só seja executada em create
        super().save(*args, **kwargs)
        if verification:
            insumos = Insumo.objects.all()
            for insumo in insumos:
                create = Carga(unity=self, item=insumo, charge=0)
                create.save()

    def __str__(self):
        return self.name



class Insumo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    usa = models.BooleanField(default=True, verbose_name='USA')
    usb = models.BooleanField(default=True, verbose_name='USB')
    unitys = models.ManyToManyField(Unidade, default=Unidade.objects.all)


    def save(self, *args, **kwargs):
        verification = False
        # este if serve para que a condição só seja executada em create
        if not self.id:
            verification = True
        # este if serve para que a condição só seja executada em create
        super().save(*args, **kwargs)
        if verification:
            item = Insumo.objects.filter(name=self.name).last()
            unitys = Unidade.objects.all()
            for unity in unitys:
                new = Carga(unity=unity, item=item, charge=0)
                new.save()
        




    def __str__(self):
        return self.name



class Carga(models.Model):
    unity = models.ForeignKey(Unidade, on_delete=models.CASCADE, verbose_name='Unidade')
    item = models.ForeignKey(Insumo, on_delete=models.CASCADE, verbose_name='Insumo')
    charge = models.IntegerField(verbose_name='Carga')

    def __str__(self):
        return f'{self.item}  ({self.unity})'


class Viatura(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    placa = models.CharField(max_length=200)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True, verbose_name='Viatura ativa')

    def __str__(self):
        return self.name


class RegistrosDiario(models.Model):
    name = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    unity = models.ForeignKey(Unidade, on_delete=models.CASCADE, verbose_name='Unidade')
    acesso = models.CharField(max_length=200)
    viatura = models.ForeignKey(Viatura, on_delete=models.SET_NULL, null=True)
    km = models.CharField(max_length=200)
    pdf = models.URLField(max_length=200, null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    pub_date = models.DateTimeField(default=datetime.now, null=True, verbose_name="Data")

    

    def __str__(self):
        return f'{self.name}'
    