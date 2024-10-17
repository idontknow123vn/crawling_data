from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re

def main():
    with (sync_playwright() as p):
        page_url = f'https://maps.google.com'

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale='vi-VN'
        )
        page = context.new_page()

        page.goto(page_url, timeout=60000)

        page.wait_for_selector('canvas')

        vietnamProvinces = [
            # "An Giang", "Bà Rịa - Vũng Tàu",
            # "Bạc Liêu",
            # # "Bắc Kạn",
            # "Bắc Giang",
            # "Bắc Ninh",
            # "Bến Tre",
            # "Bình Dương",
            "Bình Định",
            # "Bình Phước",
            "Bình Thuận",
            # "Cà Mau",
            # "Cao Bằng", "Cần Thơ",
            # "Đà Nẵng",
            # "Đắk Lắk", "Đắk Nông",
            # "Điện Biên", "Đồng Nai", "Đồng Tháp",
            # "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh",
            # "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên",
            # "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng",
            # "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An",
            # "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình",
            # "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng",
            # "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa",
            # "Thừa Thiên Huế", "Tiền Giang", "TP Hồ Chí Minh", "Trà Vinh", "Tuyên Quang",
            # "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]
        data_food = []
        try:
            for i in range(0, len(vietnamProvinces)):
                page.wait_for_load_state('load')
                page.locator('//input[@id="searchboxinput"]').fill("quán ăn ở " + vietnamProvinces[i])
                time.sleep(1.5)
                page.press('//input[@id="searchboxinput"]', 'Enter')

                for h in range(0, 25):
                    page.locator('//div[@aria-label="Kết quả cho quán ăn ở ' + vietnamProvinces[i] + '"]').evaluate(
                        'el => el.scrollTop = el.scrollHeight')
                    time.sleep(2)
                data_food_province_small = page.locator('//div[@class="Nv2PK THOPZb CpccDe "]').all()
                for index, data_food_province in enumerate(data_food_province_small):
                    data_food_dict = {}
                    map_canvas = page.locator('//canvas[@id]')
                    map_box = map_canvas.bounding_box()

                    if map_box:
                        # Số lần kéo
                        drag_times = 3
                        drag_distance = 200  # Khoảng cách kéo mỗi lần (pixels)

                        for _ in range(drag_times):
                            # Di chuyển chuột đến giữa bản đồ
                            page.mouse.move(map_box['x'] + map_box['width'] / 2, map_box['y'] + map_box['height'] / 2)

                            # Nhấn giữ chuột (click và giữ)
                            page.mouse.down()

                            # Kéo bản đồ sang phải
                            page.mouse.move(map_box['x'] + map_box['width'] / 2 + drag_distance,
                                            map_box['y'] + map_box['height'] / 2, steps=10)

                            # Thả chuột ra để hoàn thành kéo
                            page.mouse.up()

                            # Đợi một chút trước khi kéo tiếp lần sau (nếu cần)
                            page.wait_for_timeout(1000)  # Đợi 1 giây
                    else:
                        print("Không tìm thấy bản đồ")
                    if page.locator('//div[@class="Nv2PK THOPZb CpccDe "]').nth(index).count() > 0:
                        page.locator('//div[@class="Nv2PK THOPZb CpccDe "]').nth(index).click()
                        time.sleep(3)
                    else:
                        break
                    time.sleep(1.5)
                    data_food_dict['name'] = page.locator('//h1[@class="DUwDvf lfPIob"]').inner_text() if page.locator(
                        '//h1[@class="DUwDvf lfPIob"]').count() > 0 else "không có tên??????"
                    data_food_dict['address'] = page.locator(
                        '//div[@class="Io6YTe fontBodyMedium kR99db fdkmkc "]').nth(0).inner_text() if page.locator('//div[@class="Io6YTe fontBodyMedium kR99db fdkmkc "]').count() > 0 else "Không có địa chỉ"
                    data_food_dict['score'] = page.locator('//div[@class="F7nice "]/span[1]/span[1]').inner_text() if page.locator('//div[@class="F7nice "]/span[1]/span[1]').count() > 0 else "Chưa xét"
                    data_food_dict['reviews count'] = page.locator(
                        '//div[@class="F7nice "]/span[2]/span[1]/span[1]').inner_text().strip("()") if page.locator('//div[@class="F7nice "]/span[2]/span[1]/span[1]').count() > 0 else "0"
                    current_url = page.url

                    # Trích xuất tọa độ từ URL
                    regex = r"@(-?\d+\.\d+),(-?\d+\.\d+)"
                    match = re.search(regex, current_url)

                    if match:
                        latitude = match.group(1)
                        longitude = match.group(2)

                        data_food_dict['latitude'] = latitude
                        data_food_dict['longitude'] = longitude
                    else:
                        data_food_dict['latitude'] = "None"
                        data_food_dict['longitude'] = "None"
                    data_food_dict['province'] = vietnamProvinces[i]
                    data_food_dict['category'] = page.locator(
                        '//button[@class="DkEaL "]').inner_text() if page.locator(
                        '//button[@class="DkEaL "]').count() > 0 else "None"

                    if page.locator('//span[@class="mgr77e"]/span[1]/span[2]/span[1]/span[1]').count() > 0:
                        data_food_dict['price'] = page.locator(
                            '//span[@class="mgr77e"]/span[1]/span[2]/span[1]/span[1]').inner_text().replace('\u00a0', ' ').strip()
                        # data_food_dict['discount'] = page.locator('//span[@class="fontBodySmall A1XLKe"]').inner_text()
                    else:
                        data_food_dict['price'] = "Không có giá"
                        # data_food_dict['discount'] = "Không có giảm giá"
                    # elif page.locator('//span[@class="fontTitleLarge Cbys4b"]').count() > 0:
                    #     data_food_dict['price'] = page.locator(
                    #         '//span[@class="fontTitleLarge Cbys4b"]').inner_text().replace('\u00a0', ' ').strip()
                    #     data_food_dict['discount'] = "Không có giảm giá"
                    # else:
                    #     data_food_dict['price'] = "Không có giá"
                    #     data_food_dict['discount'] = "Không có giảm giá"
                    page.locator('//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]').nth(0).evaluate(
                        'el => el.scrollTop = el.scrollHeight') if page.locator('//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]').count() > 0 else None
                    elements_without_aria = page.locator(
                        '//div[@class="LTs0Rc" and @role="group"]').all()
                    data_food_dict['services'] = "None"
                    services = ""
                    if len(elements_without_aria) > 0:
                        for element in elements_without_aria:
                            service = element.locator('//div[@aria-hidden]').inner_text()
                            services += service + ", "
                    data_food_dict['services'] = services
                    img_descs = page.locator('//img[@class="DaSXdd"]').all()
                    list_img_descs = []
                    for k in range(0, 4):
                        if k >= len(img_descs):
                            break
                        # Lấy giá trị style của thẻ div chứa background-image
                        # style = img_descs[k].evaluate(
                        #     'el => el.style.backgroundImage')
                        #
                        # # Sử dụng regex để lấy URL chính xác
                        # url = re.search(r'url\("(.+?)"\)', style).group(1)
                        url = img_descs[k].get_attribute('src')

                        # Loại bỏ các tham số không cần thiết (ví dụ: w130-h87-n-k-no)
                        cleaned_url = url.split('=')[0]
                        list_img_descs.append(cleaned_url + ", ")
                    data_food_dict['description images'] = "".join(list_img_descs)
                    if page.locator('//div[@jsname="ZMv3u"]/div[3]').count() > 0:
                        page.locator('//div[@jsname="ZMv3u"]/div[3]').click()
                    else:
                        page.locator('//canvas[@id]').click()
                    data_food.append(data_food_dict)


            df = pd.DataFrame(data_food)
            df.to_excel('data_food4.xlsx', index=False)
            df.to_csv('data_food4.csv', index=False)
            browser.close()

        except Exception as e:
            # df = pd.DataFrame(food_stores)
            # df.to_excel('food_store1.xlsx', index=False)
            # df.to_csv('food_store1.csv', index=False)
            print(e)


if __name__ == '__main__':
    main()