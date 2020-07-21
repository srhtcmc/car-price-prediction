import re
from bs4 import BeautifulSoup
import pandas as pd



class Url2Df:
    
    def __init__(self,page_source):
        self.parsed = self.dict_to_df(self.content_to_dic(page_source))
        
        
    
    def unique_list(self,l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist
    
    def title_split(self,string):
        string = string.replace("sahibinden.comda","")
        baslık_bilgiler = list(re.split('/ |- ',string))
        baslık_bilgiler = list(map(str.strip, baslık_bilgiler))
        return  baslık_bilgiler[0],baslık_bilgiler[1],baslık_bilgiler[2],baslık_bilgiler[3],baslık_bilgiler[4],int(baslık_bilgiler[-1])
   
    def get_fiyat(self,fiyat):
        fiyat =' '.join(fiyat.split())
        fiyat_bilgiler = list(fiyat.split(" "))
        return fiyat_bilgiler[0]
        
    def get_sehir(self,sehir):
        sehir =' '.join(sehir.split())
        sehir_bilgiler = list(sehir.split("/"))
        return sehir_bilgiler[0]
    
    def ozellik_cıkar(self,ozellikler):
        ozellik_list = []
        for ozel in ozellikler:
            ozel = ozel.text.strip()
            ozel = ' '.join(self.unique_list(ozel.split()))
            ozellik_list.append(ozel)
        return ozellik_list
    
    def is_selected(self,features,selected):
        feature_dict = dict.fromkeys(features, 0)
        for feature in features:
            if feature in selected:
                feature_dict[feature] = 1
        return feature_dict     
    
    def content_to_dic(self,content):
    
        soup = BeautifulSoup(content)
    
        title = soup.find("title").text
        
        marka,seri,model_1,model_2,baslik,ilan_no = self.title_split(title)
        
        bilgiler = soup.find("div",attrs={"class":"classifiedInfo"})
        
        fiyat = bilgiler.h3.text
        fiyat = self.get_fiyat(fiyat)
        
        sehir = bilgiler.h2.text
        sehir = self.get_sehir(sehir)
        
        ilan_tarihi = bilgiler.select("li:nth-of-type(2) > span")[0].text.strip()
        
        yıl = int(bilgiler.select("li:nth-of-type(6) > span")[0].text.strip())
        
        yakıt = bilgiler.select("li:nth-of-type(7) > span")[0].text.strip()
        
        vites = bilgiler.select("li:nth-of-type(8) > span")[0].text.strip()
        
        km = int(bilgiler.select("li:nth-of-type(9) > span")[0].text.strip().replace(".",""))
        
        kasa_tipi = bilgiler.select("li:nth-of-type(10) > span")[0].text.strip()
        
        motor_gucu = bilgiler.select("li:nth-of-type(11) > span")[0].text.strip()
        
        motor_hacmi = bilgiler.select("li:nth-of-type(12) > span")[0].text.strip()
        
        cekis = bilgiler.select("li:nth-of-type(13) > span")[0].text.strip()
        
        renk = bilgiler.select("li:nth-of-type(14) > span")[0].text.strip()
        
        garanti =bilgiler.select("li:nth-of-type(15) > span")[0].text.strip()
        
        plaka = bilgiler.select("li:nth-of-type(16) > span")[0].text.strip()
        
        kimden = bilgiler.select("li:nth-of-type(17) > span")[0].text.strip()
        
        takas = bilgiler.select("li:nth-of-type(19) > span")[0].text.strip()
        
        durum =bilgiler.select("li:nth-of-type(20) > span")[0].text.strip()
        
        aciklama = soup.find("div",attrs={"class":"uiBoxContainer"}).text.strip()
        
        ozellik = soup.find("div",attrs={"class":"uiBoxContainer classifiedDescription"})
        ozellikler = ozellik.select("li")
        ozellikler_list = self.ozellik_cıkar(ozellikler)
        
        ozellikler_selected =soup.find_all("li",attrs={"class":"selected"})
        ozellikler_selected_list = self.ozellik_cıkar(ozellikler_selected)
        
        ozellikler_son = self.is_selected(ozellikler_list,ozellikler_selected_list)
        
        datas = [ilan_no,marka,seri,model_1,model_2,baslik,sehir,ilan_tarihi,yıl,yakıt,vites,
                 km,kasa_tipi,motor_gucu,motor_hacmi,cekis,renk,garanti,plaka,kimden,takas,durum,aciklama,fiyat]
        
        datas_main_dict = {"ilan_no":[ilan_no],
                           "marka":[marka],
                           "seri":[seri],
                           "model_1":[model_1],
                           "model_2":[model_2],
                           "baslik":[baslik],
                           "sehir":[sehir],
                           "ilan_tarihi":[ilan_tarihi],
                           "yıl":[yıl],
                           "yakıt":[yakıt],
                           "vites":[vites],
                           "km":[km],
                           "kasa_tipi":[kasa_tipi],
                           "motor_gucu":[motor_gucu],
                           "motor_hacmi":[motor_hacmi],
                           "cekis":[cekis],
                           "renk":[renk],
                           "garanti":[garanti],
                           "plaka":[plaka],
                           "kimden":[kimden],
                           "takas":[takas],
                           "durum":[durum],
                           "aciklama":[aciklama],
                           "fiyat":[fiyat]
                            }
        datas_main_dict.update(ozellikler_son)
        
        return datas_main_dict
    
    def dict_to_df(self,dicti):
        df = pd.DataFrame.from_dict(dicti)
        df = pd.get_dummies(data=df, columns=['seri','model_1',"model_2","sehir","yakıt","kasa_tipi","motor_gucu",
                                          "motor_hacmi","renk","vites"])
        empty_dacia_df = pd.read_pickle("/home/serhat/Desktop/Project/sahinden/py_folders/empty_dacia_df")
        car_informations_df = empty_dacia_df.append(df,ignore_index=True)
        __unnecessary_columns = ['marka', 'Unnamed: 0', 'ilan_no', 'aciklama', 'ilan_tarihi', 'cekis', 'plaka', 
                   'kimden', 'durum', 'baslik', 'ABC', 'AEB', 'EBP', 'Airmatic', 'EDL', 'EBA', 'TCS', 
                   'BAS', 'Distronic', 'Zırhlı Araç', 'Gece Görüş', 'Şeritten Ayrılma İkazı', 
                   'Şerit Değiştirme Yardımcısı', 'Hava Yastığı (Diz)', 'Hava Yastığı (Perde)', 
                   'Hava Yastığı (Tavan)', 'Kör Nokta Uyarı Sistemi', 'Yorgunluk Tespit Sistemi', 
                   'Alarm', 'Deri Koltuk', 'Deri / Kumaş Koltuk', 'Otm.Kararan Dikiz Aynası', 
                   'Arka Kol Dayama', 'Anahtarsız Giriş ve Çalıştırma', '6 İleri Vites', 
                   '7 İleri Vites', 'Fonksiyonel Direksiyon', 'Deri Direksiyon', 'Ahşap Direksiyon',
                   'Isıtmalı Direksiyon', 'Koltuklar (Elektrikli)', 'Koltuklar (Hafızalı)',
                   'Koltuklar (Ön Isıtmalı)', 'Koltuklar (Arka Isıtmalı)', 'Koltuklar (Soğutmalı)',
                   'Adaptive Cruise Control', 'Soğutmalı Torpido', 'Ahşap Kaplama', 'Head-up Display', 
                   'Start / Stop', 'Ön Görüş Kamerası', '3. Sıra Koltuk', 'Hardtop', 'Far (LED)', 'Far (Halojen)',
                   'Far (Xenon)', 'Far (Bi Xenon)', 'Far (Adaptif)', 'Far Gece Sensörü', 'Far Yıkama', 
                   'Aynalar (Otom.Katlanır)', 'Aynalar (Hafızalı)', 'Park Sensörü (Ön)', 'Park Asistanı',
                   'Sunroof', 'Panoramik Cam Tavan', 'Panoramik Ön Cam', 'Romörk Çeki Demiri', 'Akıllı Bagaj Kapağı',
                   'TV', 'iPod Bağlantısı', '6+ Hoparlör', 'CD Değiştirici', 'Arka Eğlence Paketi', 
                   'DVD Değiştirici', 'Boyalı Parçalar', 
                   'Aracın boyası orijinaldir, sonradan boyanan parçası yoktur', 'Değişen Parçalar',
                   'Motor Kaputu', 'Sol Ön Çamurluk', 'Sol Arka Çamurluk', 'Arka Kaput', 
                   'Aracın parçaları orijinaldir, sonradan değişen parçası yoktur', 'Sol Arka Kapı', 
                   'Sağ Ön Kapı', 'Sağ Arka Kapı', 'Sağ Arka Çamurluk', 'Arka Tampon', 'Sol Ön Kapı', 
                   'Ön Tampon', 'Tavan',"fiyat"]
        for col in __unnecessary_columns:
            try:
                car_informations_df = car_informations_df.drop(str(col),axis = 1)
            except:
                pass
            
        car_informations_df = car_informations_df.replace(to_replace=["Evet","Hayır"],value=[1,0])
        car_informations_df = car_informations_df.fillna(0)
        
        return car_informations_df

