from ocrapi import recognize_captcha
import time,DrissionPage

Api_proxy="http://localhost:8000/recognize"
Api_key="bd215ccaebeaa5a26c1ed29414f34944"

def ocr(image : bytes):
    res=recognize_captcha(image,Api_proxy,Api_key)
    print(res)
    return res["result"]

co = DrissionPage.ChromiumOptions()
co.set_local_port(9222)
co.headless(True)

page=DrissionPage.ChromiumPage(addr_or_opts=co)

page.get("https://vjudge.net/util/luogu/captcha")
while True:
    page.refresh()
    page.wait.doc_loaded()
    page.wait(1.2,1.4)

    image_ele = page.ele("@id=captcha_img")

    if image_ele.link == "https://vjudge.net/util/luogu/captcha":
        page.wait(0.7,1)
        continue
    print("det:"+image_ele.link)
    ocr_res = ocr(image_ele.src(base64_to_bytes=True))
    if ocr_res==None:
        continue
    if len(ocr_res)!=4:
        ocr_res="mmmm"
    print("ocr:"+ocr_res)
    page.wait(0.5,0.7)
    captcha_input = page.ele("@name=captcha_code")
    captcha_input.input(ocr_res,clear=True)

    author_input = page.ele("@name=captcha_contributor")
    author_input.input("petyr",clear=True)

    submit = page.ele('@type=submit')
    submit.click()
    page.wait(1.5,1.8)
