import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(0)

    def test_kassapaate_luotu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)



    def test_edullisesti_kateisella_maksu_riittava(self):
        takaisin_rahaa = self.kassapaate.syo_edullisesti_kateisella(260)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(takaisin_rahaa, 20)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullisesti_kateisella_maksu_ei_riita(self):
        takaisin_rahaa = self.kassapaate.syo_edullisesti_kateisella(42)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(takaisin_rahaa, 42)
        self.assertEqual(self.kassapaate.edulliset, 0)
 


 
    def test_maukkaasti_kateisella_maksu_riittava(self):
        takaisin_rahaa = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(takaisin_rahaa, 100)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukkaasti_kateisella_maksu_ei_riita(self):
        takaisin_rahaa = self.kassapaate.syo_maukkaasti_kateisella(42)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(takaisin_rahaa, 42)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    


    
    def test_edullisesti_kortilla_maksu_riittava(self):
        self.maksukortti.lataa_rahaa(1000)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(onnistui, True)
        self.assertEqual(self.maksukortti.saldo, 760)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    def test_edullisesti_kortilla_maksu_ei_riita(self):
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(onnistui, False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.maksukortti.saldo, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    
    def test_maukkaasti_kortilla_maksu_riittava(self):
        self.maksukortti.lataa_rahaa(1000)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(onnistui, True)
        self.assertEqual(self.maksukortti.saldo, 600)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)




    def test_maukkaasti_kortilla_maksu_ei_riita(self):
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(onnistui, False)
        self.assertEqual(self.maksukortti.saldo, False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    def test_kortille_rahan_lataus_rahaa_riittavasti(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 42)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100042)
        self.assertEqual(self.maksukortti.saldo, 42)
        

    def test_kortille_rahan_lataus_rahaa_ei_riittavasti(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -5)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.maksukortti.saldo, 0)










