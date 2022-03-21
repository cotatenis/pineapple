from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from pineapple.items import PineappleItem
from w3lib.html import remove_tags
import re
class AdidasSpider(CrawlSpider):
    name = 'pineapple-adidas'
    settings = get_project_settings()
    version = settings.get("VERSION")
    allowed_domains = ['shop-pineapple.co']
    start_urls = ['https://www.shop-pineapple.co/calcados-tenis?fq=Marca:317288']
    brand = 'adidas'
    product_details = LinkExtractor(restrict_xpaths="//a[contains(@title, 'NOVO')]")
    pagination = LinkExtractor(restrict_xpaths=("//div[@class='pagination']//li//a[contains(@href, 'pagina=')]"))
    rules = [Rule(product_details, callback='parse_products'), Rule(pagination, follow=True)]
    stock_mapping = {
        'http://schema.org/InStock' : True,
        'http://schema.org/OutOfStock' : False
    }
    condition_mapping = {
        'http://schema.org/NewCondition' : True,
        'http://schema.org/UsedCondition' : False
    }
    sku_pattern_match = r"Fabricante:(\s+)?\w+(-\w+)?|fabricante:(\s+)?\w+(-\w+)?"
    def parse_products(self, response):
        if response.url not in self.start_urls:
            # product
            product = response.xpath("//h1[contains(@class, 'nome-produto')]/text()").get()
            if product:
                product = product.split("-NOVO-")[0]
                product = product.replace("NIKE - ","Nike ")\
                .replace("ADIDAS - ","adidas ")\
                .replace("ADIDAS", "adidas")\
                .replace("!adidas", "adidas")\
                .replace("!NIKE", "Nike")\
                .replace("!Nike", "Nike")\
                .replace("NIKE", "Nike")
            description = response.xpath("//div[@id='descricao']//p[2]/span[@style='color:#000000;']//text()").get()
            if not description:
                description = response.xpath("//div[@id='descricao']//p[2]/span[@style='font-size:14px;']//text()").get()
            sku = self.parse_sku(response=response)
            #prices
            prices = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='price']/@content").getall()
            currencies = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='price']/@content").getall()
            stock_info = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='availability']/@content").getall()
            item_conditions = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='itemCondition']/@content").getall()
            sizes = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='sku']/@content").getall()
            urls = response.xpath("//div[@itemtype='http://schema.org/Offer']/meta[@itemprop='url']/@content").getall()
            brand = self.brand
            if 'Jordan' in product:
                brand = 'Jordan'
            for price, currency, in_stock, size, item_condition, url in zip(prices, currencies, stock_info, sizes, item_conditions, urls):
                if isinstance(sku, str):
                    sku = remove_tags(sku).strip()
                if price != "":
                    yield PineappleItem(**{
                        'product' : product,
                        'url' : url,
                        'description' : description,
                        'sku' : sku,
                        'price' : float(price),
                        'currency' : currency,
                        'in_stock' : self.stock_mapping.get(in_stock, False),
                        'size' : size.split("-")[-1],
                        'is_new' : self.condition_mapping.get(item_condition, False),
                        'brand' : brand,
                        'spider' : self.name,
                        'spider_version' : self.version
                    })
    
    def parse_sku(self, response):
        sku = None
        sku = response.xpath("//span[contains(text(), 'Código do Fabricante')]/text()|//span[contains(text(), 'Fabricante:')]").get()
        if sku:
            sku = sku.split(":")[-1].strip()
        else:
            sku = response.xpath("//span[contains(text(), 'Ano')]").re(self.sku_pattern_match)
            if sku:
                if ":" in sku[0]:
                    sku = sku[0].split(":")[-1].strip()
                else:
                    raw_sku = [d for d in response.xpath("//span").getall() if 'Fabricante' in d]
                    if raw_sku:
                        raw_sku = raw_sku[-1]
                        raw_sku = re.search(self.sku_pattern_match, raw_sku)
                        if raw_sku:
                            raw_sku = raw_sku.group(0)
                            sku = raw_sku.split(":")[-1].strip()
                    else:
                        raw_sku = [d for d in response.xpath("//span").getall() if 'fabricante' in d]
                        if raw_sku:
                            raw_sku = raw_sku[-1]
                            raw_sku = re.search(self.sku_pattern_match, raw_sku)
                            if raw_sku:
                                raw_sku = raw_sku.group(0)
                                sku = raw_sku.split(":")[-1].strip()
            else:
                raw_sku = [d for d in response.xpath("//span").getall() if 'Fabricante' in d]
                if raw_sku:
                    raw_sku = raw_sku[-1]
                    raw_sku = re.search(self.sku_pattern_match, raw_sku)
                    if raw_sku:
                        raw_sku = raw_sku.group(0)
                        sku = raw_sku.split(":")[-1].strip()
                else:
                    raw_sku = [d for d in response.xpath("//span").getall() if 'fabricante' in d]
                    if raw_sku:
                        raw_sku = raw_sku[-1]
                        raw_sku = re.search(self.sku_pattern_match, raw_sku)
                        if raw_sku:
                            raw_sku = raw_sku.group(0)
                            sku = raw_sku.split(":")[-1].strip()
                    else:
                        #não está em um tag span e sim numa tag p
                        raw_sku = [d for d in response.xpath("//p").getall() if 'Fabricante' in d]
                        if raw_sku:
                            raw_sku = raw_sku[-1]
                            raw_sku = re.search(self.sku_pattern_match, raw_sku)
                            if raw_sku:
                                raw_sku = raw_sku.group(0)
                                sku = raw_sku.split(":")[-1].strip()
                        else:
                            raw_sku = [d for d in response.xpath("//p").getall() if 'fabricante' in d]
                            if raw_sku:
                                raw_sku = raw_sku[-1]
                                raw_sku = re.search(self.sku_pattern_match, raw_sku)
                                if raw_sku:
                                    raw_sku = raw_sku.group(0)
                                    sku = raw_sku.split(":")[-1].strip()
        return sku