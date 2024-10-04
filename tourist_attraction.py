from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re

def main():
    with (sync_playwright() as p):
        page_url = f'https://www.google.com/search?q=%C4%91%E1%BB%8Ba+%C4%91i%E1%BB%83m+du+l%E1%BB%8Bch+%E1%BB%9F+%C4%91%C3%A0+n%E1%BA%B5ng&sca_esv=e36dedb6b3bd1831&sxsrf=ADLYWIJ2jdPHLS8O174dXUPSCMlemmn-5g:1728026343290&udm=15&sa=X&ved=2ahUKEwjjturil_SIAxUDrlYBHWZ6FtwQxN8JegQIVRAz&biw=1912&bih=1000'

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()

        page.goto(page_url, timeout=60000)

        vietnamProvinces = [
            # "An Giang", "Bà Rịa - Vũng Tàu",
            # "Bạc Liêu", "Bắc Kạn", "Bắc Giang",
            # "Bắc Ninh", "Bến Tre", "Bình Dương", "Bình Định", "Bình Phước",
            # "Bình Thuận", "Cà Mau",
            # "Cao Bằng", "Cần Thơ", "Đà Nẵng",
            # "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp",
            # "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh",
            # "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên",
            # "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng",
            # "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An",
            # "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình",
            # "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng",
            # "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa",
            "Thừa Thiên Huế", "Tiền Giang", "TP Hồ Chí Minh", "Trà Vinh", "Tuyên Quang",
            "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]
        attraction_full_dict = []
        # try:
        for i in range(0, len(vietnamProvinces)):
            page.wait_for_load_state('load')
            page.locator('//textarea[@aria-label="Tìm kiếm"]').fill("điểm đến du lịch ở " + vietnamProvinces[i])
            time.sleep(1.5)
            page.press('//textarea[@aria-label="Tìm kiếm"]', 'Enter')
            page.wait_for_load_state('load')
            page_height = page.evaluate("() => document.body.scrollHeight")

            # Cuộn xuống 1 trang 3 lần
            for _ in range(0, 2):
                page.evaluate(f"window.scrollBy(0, {page_height})")
                page.wait_for_load_state('load')
                if (page.locator('//div[@class="ZFiwCf" and span[span[text()="Điểm tham quan khác"]]]').count() > 0):
                    if (page.locator('//div[@class="ZFiwCf" and span[span[text()="Điểm tham quan khác"]]]').nth(
                            0).is_visible() == False):
                        break
                    page.locator('//div[@class="ZFiwCf" and span[span[text()="Điểm tham quan khác"]]]').nth(0).click()
                time.sleep(2)  # Điều chỉnh thời gian chờ giữa các lần cuộn

            attractions = page.locator('//div[@jsname="jXK9ad" and @class="Z8r5Gb ZVHLgc"]').all()
            for index, atraction in enumerate(attractions):
                attraction_dict = {}
                attraction_dict['name'] = atraction.locator('//div[@class="yVCOtc CvgGZ LJEGod aKoISd"]/span[1]').inner_text()
                attraction_dict['score'] = atraction.locator('//span[@class="yi40Hd YrbPuc"]').inner_text() if atraction.locator('//span[@class="yi40Hd YrbPuc"]').count() > 0 else "Chưa xét"
                attraction_dict['category'] = atraction.locator('//div[@class="ZJjBBf cyspcb DH9lqb"]/span[1]').inner_text() if atraction.locator('//div[@class="ZJjBBf cyspcb DH9lqb"]/span[1]').count() > 0 else "Địa điểm du lịch"
                attraction_dict['price'] = atraction.locator('//div[@class="rDUZLd JNI6Yb"]/span[1]').inner_text() if atraction.locator('//div[@class="rDUZLd JNI6Yb"]/span[1]').count() > 0 else "Không có giá"
                page.locator('//div[@jsname="jXK9ad" and @class="Z8r5Gb ZVHLgc"]').nth(index).click()
                time.sleep(1)

                if page.locator('//div[@class="C9waJd "]/a[2]/div[1]/span[1]').count() > 0:
                    attraction_dict['address'] = page.locator('//div[@class="C9waJd "]/a[2]/div[1]/span[1]').inner_text()
                elif page.locator("//a[@class='zfFVc']/div[1]/span[1]").count() > 0:
                    attraction_dict['address'] = page.locator("//a[@class='zfFVc']/div[1]/span[1]").inner_text()
                else:
                    attraction_dict['address'] = "Không có địa chỉ cụ thể"
                attraction_dict['province'] = vietnamProvinces[i]
                attraction_dict['review count'] = page.locator('//span[@class="PN9vWe"]').inner_text().strip(
                    "()") if page.locator('//span[@class="PN9vWe"]').count() > 0 else "không có đánh giá"
                img_descs = page.locator(
                    '//div[@class="nNzjpf-cS4Vcb-PvZLI-ywRG6e-RJLb9c nNzjpf-cS4Vcb-PvZLI-v3Bspd"]/img[1]').all()
                list_img_descs = []
                for k in range(0, 2):
                    if k >= len(img_descs):
                        break

                    # lấy URL chính xác
                    url = img_descs[k].get_attribute('src')

                    # Loại bỏ các tham số không cần thiết (ví dụ: w130-h87-n-k-no)
                    cleaned_url = url.split('=')[0]
                    list_img_descs.append(cleaned_url + ", ")
                attraction_dict['description images'] = "".join(list_img_descs)
                attraction_full_dict.append(attraction_dict)
        df = pd.DataFrame(attraction_full_dict)
        df.to_excel('attraction6.xlsx', index=False)
        df.to_csv('attraction6.csv', index=False)

        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    main()
