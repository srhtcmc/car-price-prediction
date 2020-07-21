#main
import crawler
import page_parser as ps
import pickle

rfr_model = pickle.load(open("/home/serhat/Desktop/dacia/finalized_RFR_model.sav", 'rb'))

crawler = crawler.GetNewPageUrl("https://www.sahibinden.com/ilan/vasita-otomobil-dacia-1.4-tuplu-1bucuk-parca-boyali-degisensiz-180.000km-de-842618254/detay")

informations = ps.Url2Df(crawler.page_source)

print("Predicted price :",rfr_model.predict(informations.parsed), " TL")