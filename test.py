from bs4 import BeautifulSoup

html = """
<div class="byrV5b"><cite class="tjvcx GvPZzd dTxz9 cHaqb" role="text"><span dir="ltr">https://developers.instagram.com</span></cite></div>
<div class="byrV5b"><cite class="tjvcx GvPZzd dTxz9 cHaqb" role="text"><span dir="ltr">https://ai.instagram.com/</span></cite></div>
<div class="byrV5b"><cite class="tjvcx GvPZzd dTxz9 cHaqb" role="text"><span dir="ltr">https://api.instagram.com</span></cite></div>
<div class="byrV5b"><cite class="tjvcx GvPZzd dTxz9 cHaqb" role="text"><span dir="ltr">https://facebook.com/developers</span></cite></div>
"""

soup = BeautifulSoup(html, "html.parser")

# استخراج كل النصوص داخل <cite>

