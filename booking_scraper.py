from playwright.sync_api import sync_playwright
import pandas as pd
import time


def main():
    
    with (sync_playwright() as p):
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # page_url này sẽ redirect đến đà nẵng trong khoảng thời gian từ 15/09/2024 đến 17/09/2024,
        # khi đến ngày 15 thì đổi lại url đà nẵng trong ngày khác ở tương lai để lây dữ liệu
        page_url = f'https://www.booking.com/searchresults.vi.html?ss=%C4%90%C3%A0+N%E1%BA%B5ng&ssne=%C4%90%C3%A0+N%E1%BA%B5ng&ssne_untouched=%C4%90%C3%A0+N%E1%BA%B5ng&label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEquAEXyAEM2AEB6AEB-AENiAIBqAIDuAL9sN-2BsACAdICJDkzYjg2NjEwLTEyYmUtNDgzMi04ODFiLTYxZDU2MzY4ODllNNgCBuACAQ&sid=67c37a7529c55ff331b675d4e291635f&aid=304142&lang=vi&sb=1&src_elem=sb&src=searchresults&dest_id=-3712125&dest_type=city&checkin=2024-09-15&checkout=2024-09-17&group_adults=1&no_rooms=1&group_children=0'
        page.goto(page_url, timeout=60000)
        provinces = [
            "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre",
            "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao Bằng",
            "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai",
            # "Hà Giang",
            # "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên",
            # "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An",
            # "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam",
            # "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình",
            # "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh",
            # "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]

        hotels_list = []

        for i in range(0, len(provinces)):
            page.wait_for_load_state('load')
            page_height = page.evaluate("() => document.body.scrollHeight")

            # Cuộn xuống nửa trang 3 lần
            for _ in range(3):
                page.evaluate(f"window.scrollBy(0, {page_height / 2.5})")
                page.wait_for_load_state('load')
                if(page.locator('//button[span[text()="Tải thêm kết quả"]]').count() > 0):
                    page.locator('//button[span[text()="Tải thêm kết quả"]]').click()
                time.sleep(2)  # Điều chỉnh thời gian chờ giữa các lần cuộn


            hotels = page.locator('//div[@data-testid="property-card"]').all()
            print(f'There are: {len(hotels)} hotels in {"Đà Nẵng" if i==0 else provinces[i - 1]}.')

            for index, hotel in enumerate(hotels):
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]/div[1]'
                                                    ).inner_text() if hotel.locator('//div[@data-testid="review-score"]'
                                                                                    ).count() > 0 else hotel.locator('//div[@data-testid="external-review-score"]/div[1]/div[1]'
                                                                                                                     ).inner_text() if hotel.locator('//div[@data-testid="external-review-score"]'
                                                                                                                                                     ).count() > 0 else "None"
                hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]'
                                                         ).inner_text() if hotel.locator('//div[@data-testid="review-score"]'
                                                                                         ).count() > 0 else hotel.locator('//div[@data-testid="external-review-score"]/div[1]/div[1]'
                                                                                                                          ).inner_text() if hotel.locator('//div[@data-testid="external-review-score"]'
                                                                                                                                                          ).count() > 0 else "None"
                hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0] if hotel.locator('//div[@data-testid="review-score"]').count() > 0 else "None"
                hotel_dict['province'] = "Đà Nẵng" if i == 0 else provinces[i - 1]
                with context.expect_page() as new_page_info:
                    page.locator('//a[span[text()="Xem chỗ trống"]]').nth(index).click()

                new_page = new_page_info.value
                new_page.wait_for_load_state('load')

                hotel_dict['address'] = new_page.locator('//p[@id="showMap2"]/span[1]').inner_text()
                new_page.locator('//div[a[@data-preview-image-layout="see_more"]]').click()
                new_page.wait_for_load_state('load')
                img_descs = new_page.locator('//li[@class="bh-photo-modal-masonry-grid-item caption_hover"]/a[1]/img[@class="bh-photo-modal-grid-image"]').all()
                # print(f'There are: {len(img_descs)} description images in {hotel_dict["hotel"]}.')
                list_img_descs = []
                for k in range(0, 2):
                    if k >= len(img_descs):
                        break
                    list_img_descs.append(img_descs[k].get_attribute('src').join(", "))
                hotel_dict['description images'] = "".join(list_img_descs)
                new_page.close()

                hotels_list.append(hotel_dict)

            page.locator('//input[@id=":rh:"]').fill(provinces[i].append(", Vietnam"))
            time.sleep(0.75)
            page.locator('//button[span[text()="Tìm"]]').click()



        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list4.xlsx', index=False)
        df.to_csv('hotels_list4.csv', index=False)

        browser.close()

            
if __name__ == '__main__':
    main()