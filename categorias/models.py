from datetime import datetime
from django.db import models



# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    usa = models.BooleanField(default=True, verbose_name='USA')
    usb = models.BooleanField(default=True, verbose_name='USB')

    def __str__(self):
        return self.name



class Insumo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')

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


# Create your models here.
class Unidade(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')

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


class RegistroItemDiario(models.Model):
    item = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    carga = models.IntegerField()
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE)
    vtr = models.ForeignKey(Viatura, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, null=True, verbose_name='Data')

    def __str__(self):
        return self.item.name


class RegistrosDiario(models.Model):
    name = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    unity = models.ForeignKey(Unidade, on_delete=models.PROTECT, verbose_name='Unidade')
    acesso = models.CharField(max_length=200)
    viatura = models.ForeignKey(Viatura, on_delete=models.CASCADE)
    km = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'pdf/%d-%m-%Y', blank=True, null=True, verbose_name='Pdf')
    pub_date = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return f'{self.name}'
    
