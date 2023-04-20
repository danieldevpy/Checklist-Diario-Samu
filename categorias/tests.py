from django.test import TestCase, Client
from categorias import models
from django.urls import reverse



# Create your tests here.
class ModelTestCase(TestCase):
    name = "TestCase"
    category = "CategoryTestCase"
    unity = "UnityTestCase"
    placa = "PlacaTestCase"

    def setUp(self) -> None:
    
        models.Categoria.objects.create(
            name=self.category
        )
        models.Insumo.objects.create(
            name=self.name,
            category=models.Categoria.objects.get(
                name=self.category
            )
        )
        models.Unidade.objects.create(
            name=self.unity
        )
        models.Viatura.objects.create(
            name=self.name,
            placa=self.placa,
            unidade=models.Unidade.objects.get(
                name=self.unity
            )
        )
    
    def test_create_category(self):
        category = models.Categoria.objects.get(
            name=self.category
        )
        self.assertEquals(category.__str__(), self.category)
    
    def test_create_insumo(self):
        insumo = models.Insumo.objects.get(
            name=self.name
        )
        self.assertEquals(insumo.__str__(), self.name)
    
    def test_create_unity(self):
        unity = models.Unidade.objects.get(
            name=self.unity
        )
        self.assertEquals(unity.__str__(), self.unity)
    
    def test_create_vtr(self):
        vtr = models.Viatura.objects.get(
            name=self.name
        )
        self.assertEquals(vtr.__str__(), self.name)
        self.assertEqual(vtr.placa, self.placa)
        self.assertEquals(vtr.unidade.name, self.unity)

    def test_verific_charge(self):
        insumos = models.Insumo.objects.count()
        charges = models.Carga.objects.filter(
            unity=models.Unidade.objects.get(name=self.unity)
        ).count()
        self.assertEquals(insumos, charges)


