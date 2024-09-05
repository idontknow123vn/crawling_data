from playwright.sync_api import sync_playwright
import pandas as pd
import time


def main():
    
    with (sync_playwright() as p):
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2024-09-02'
        checkout_date = '2024-09-05'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page_url = f'https://www.booking.com/searchresults.vi.html?ss=%C4%90%C3%A0+N%E1%BA%B5ng&ssne=%C4%90%C3%A0+N%E1%BA%B5ng&ssne_untouched=%C4%90%C3%A0+N%E1%BA%B5ng&label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEquAEXyAEM2AEB6AEB-AENiAIBqAIDuAL9sN-2BsACAdICJDkzYjg2NjEwLTEyYmUtNDgzMi04ODFiLTYxZDU2MzY4ODllNNgCBuACAQ&sid=67c37a7529c55ff331b675d4e291635f&aid=304142&lang=vi&sb=1&src_elem=sb&src=searchresults&dest_id=-3712125&dest_type=city&checkin=2024-09-15&checkout=2024-09-17&group_adults=1&no_rooms=1&group_children=0'
        page.goto(page_url, timeout=60000)
        provinces = ["Hà Nội", "TP. Hồ Chí Minh", "Hội An", "Nha Trang", "Phú Quốc", "Quy Nhơn", "Vũng Tàu", "Đà Lạt", "Cần Thơ", "Phú Quốc", "Cà Mau", "Hạ Long", "Huế", "Mũi Né", "Sapa", "Sóc Trăng", "Vinh", "Đà Lạt", "Điện Biên", "Đồng Hới", "Hà Giang", "Hà Tĩnh", "Hải Dương", "Hòa Bình", "Kon Tum", "Lạng Sơn", "Lào Cai", "Ninh Bình", "Phan Thiết", "Phú Yên", "Quảng Bình", "Quảng Ngãi", "Quảng Trị", "Thanh Hóa", "Tuyên Quang", "Vĩnh Phúc", "Yên Bái"]

        hotels_list = []


        for i in range(0, len(provinces)):
            page.wait_for_load_state('load')

            for j in range(0, 1000, 100):  # Thay đổi phạm vi và bước nhảy tùy thuộc vào nhu cầu của bạn
                page.evaluate(f"window.scrollBy(0, {i})")
                time.sleep(0.2)  # Điều chỉnh thời gian giữa các lần cuộn
                # để thay đổi tốc độ

            hotels = page.locator('//div[@data-testid="property-card"]').all()
            print(f'There are: {len(hotels)} hotels in {"Đà Nẵng" if i==0 else provinces[i - 1]}.')

            for hotel in hotels:
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

                hotels_list.append(hotel_dict)

            page.locator('//input[@id=":rh:"]').fill(provinces[i])
            time.sleep(1)
            page.locator('//button[span[text()="Tìm"]]').click()



        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list2.xlsx', index=False)
        df.to_csv('hotels_list2.csv', index=False)

        browser.close()

            
if __name__ == '__main__':
    main()