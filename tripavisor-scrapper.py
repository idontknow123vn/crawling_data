from playwright.sync_api import sync_playwright
import pandas as pd
import time


def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        # checkin_date = '2024-09-02'
        # checkout_date = '2024-09-05'

        page_url = f'https://restaurantguru.com'

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()

        page.goto(page_url, timeout=60000)


        provinces = [
            # "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre",
            # "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao Bằng",
            # "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai",
            # "Hà Giang",
            # "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên",
            # "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An",
            # "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận",
            "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam",
            "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình",
            "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh",
            "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]



        # def on_new_page(event_page):
        #     nonlocal new_page
        #     new_page = event_page
        #
        # context.on("page", on_new_page)
        #
        # page.wait_for_load_state('load')
        #
        #
        # categories = page.locator('//button[@class="OKHdJ z Pc PQ Pp PD W _S Gn Rd _M PQFNM wSSLS"]').all()
        #
        # print(f'There are: {len(categories)} categories.')
        #
        # with page.expect_popup() as popup_info:
        #     page.locator('//a[@class="BMQDV _F Gv wSSLS SwZTJ"]/button[@class="OKHdJ z Pc PQ Pp PD W _S Gn Rd _M PQFNM wSSLS"]').first.click()
        #
        # new_page = popup_info.value
        #
        # new_page.wait_for_load_state('load')
        #
        # time.sleep(10)
        # # hotels_list = []
        # # for hotel in hotels:
        # #     hotel_dict = {}
        # #     hotel_dict['khách sạn'] = hotel.locator('//div[@class="nBrpc o W"]').inner_text()
        # #     hotel_dict['giá'] = hotel.locator('//span[@data-automation="metaRegularPrice"]').inner_text()
        # #     hotel_dict['đánh giá'] = hotel.locator('//div[@class="luFhX o W f u w JSdbl"]').get_attribute('aria-label').split(". ")[0]
        # #     # hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
        # #     hotel_dict['lượt review'] = hotel.locator('//span[@class="S4"]').inner_text().split()[0]
        # #
        # #     hotels_list.append(hotel_dict)
        # #
        # # df = pd.DataFrame(hotels_list)
        # # df.to_excel('hotels_list2.xlsx', index=False)
        # # df.to_csv('hotels_list2.csv', index=False)
        #
        browser.close()


if __name__ == '__main__':
    main()