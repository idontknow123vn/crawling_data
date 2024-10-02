from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re


def main():
    with sync_playwright() as p:
        page_url = f'https://www.google.com/search?q=qu%C3%A1n+%C4%83n&sca_esv=5cebedcd039efd62&sca_upv=1&biw=1920&bih=991&tbm=lcl&sxsrf=ADLYWIKqYuiwtE6Be8JwH-zw5Omz6NQWdA%3A1727399925536&ei=9Qf2ZvO0IKrk2roPw-qquQY#rlfi=hd:;si:;mv:[[16.034058899999998,108.24371749999999],[15.9935612,108.2049799]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9'

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
        food_stores = []

        try:
            for i in range(0, len(vietnamProvinces)):
                page.wait_for_load_state('load')
                page.locator('//textarea[@title="Tìm kiếm"]').fill("quán ăn ở " + vietnamProvinces[i])
                time.sleep(1.5)
                page.press('//textarea[@title="Tìm kiếm"]', 'Enter')

                food_stores_per_province_large = []
                # Paging
                for j in range(1, 6):
                    page.locator('//div[@id="center_col"]').evaluate('el => el.scrollTop = el.scrollHeight')
                    food_stores_per_province_small = page.locator('//div[@class="VkpGBb"]').all()
                    for index, food_stores_ in enumerate(food_stores_per_province_small):
                        food_dict = {}
                        page.locator('//div[@class="dbg0pd"]').nth(index).click()
                        time.sleep(1.5)
                        page.locator('//div[@class="AVvGRc"]').nth(0).evaluate('el => el.scrollTop = el.scrollHeight')
                        food_dict['name'] = food_stores_.locator('//div[@class="dbg0pd"]').inner_text() if food_stores_.locator('//div[@class="dbg0pd"]').count() > 0 else "None"
                        food_dict['address'] = food_stores_.locator('//div[@jsname="MZArnb"]/div[3]').inner_text() if food_stores_.locator('//div[@jsname="MZArnb"]/div[3]').count() > 0 else "None"
                        food_dict['score'] = food_stores_.locator('//span[@class="yi40Hd YrbPuc"]').inner_text() if food_stores_.locator('//span[@class="yi40Hd YrbPuc"]').count() > 0 else "Chưa xét"
                        food_dict['reviews count'] = food_stores_.locator('//span[@class="RDApEe YrbPuc"]').inner_text().strip("()") if food_stores_.locator('//span[@class="RDApEe YrbPuc"]').count() > 0 else "0"
                        price_text = page.locator('//div[@class="Neccf"]/div[1]/div[1]/span[2]').inner_text() if page.locator('//div[@class="Neccf"]/div[1]/div[1]/span[2]').count() > 0 else "None"
                        # Tách chuỗi theo ký tự xuống dòng
                        price_and_report = price_text.split('\n')

                        # Lấy từng phần tử
                        price = price_and_report[0] if len(price_and_report) > 0 else "None"
                        report = price_and_report[1] if len(price_and_report) > 1 else "None"
                        food_dict['avg price'] = price.replace('\u00a0', ' ').strip()
                        food_dict['province'] = vietnamProvinces[i]
                        img_descs = page.locator('//div[@class="vwrQge" and @role="img"]').all()
                        list_img_descs = []
                        for k in range(0, 2):
                            if k >= len(img_descs):
                                break
                            # Lấy giá trị style của thẻ div chứa background-image
                            style = img_descs[k].evaluate(
                                'el => el.style.backgroundImage')

                            # Sử dụng regex để lấy URL chính xác
                            url = re.search(r'url\("(.+?)"\)', style).group(1)

                            # Loại bỏ các tham số không cần thiết (ví dụ: w130-h87-n-k-no)
                            cleaned_url = url.split('=')[0]
                            list_img_descs.append(cleaned_url + ", ")
                        food_dict['description images'] = "".join(list_img_descs)
                        food_stores_per_province_large.append(food_dict)
                    try:
                        page.locator('//a[span[text()="Tiếp"]]').click()
                    except Exception as e:
                        break
                    time.sleep(1)
                food_stores.extend(food_stores_per_province_large)
            df = pd.DataFrame(food_stores)
            df.to_excel('food_store7.xlsx', index=False)
            df.to_csv('food_store7.csv', index=False)
            browser.close()
        except Exception as e:
            # df = pd.DataFrame(food_stores)
            # df.to_excel('food_store1.xlsx', index=False)
            # df.to_csv('food_store1.csv', index=False)
            print(e)


if __name__ == '__main__':
    main()
