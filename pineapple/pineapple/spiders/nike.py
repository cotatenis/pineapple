from pineapple.spiders.adidas import AdidasSpider

class NikeSpider(AdidasSpider):
    name = 'pineapple-nike'
    start_urls = ['https://www.shop-pineapple.co/calcados-tenis?fq=Marca:317285']
    brand = 'Nike'
