from django import template
import math
register = template.Library()

@register.simple_tag
def cal_sellprice(price, Discount):
    if Discount is None or Discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * Discount/100)
    return math.floor(sellprice)
        
@register.simple_tag
def progress_bar(total_quantity, availability):
    progress_bar = availability
    progress_bar = availability * (100 / total_quantity)
    return math.floor(progress_bar)
    
    