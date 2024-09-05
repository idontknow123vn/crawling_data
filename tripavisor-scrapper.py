from playwright.sync_api import sync_playwright
import pandas as pd
import time


def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        # checkin_date = '2024-09-02'
        # checkout_date = '2024-09-05'

        page_url = f'https://www.tripadvisor.com.vn/Attractions-g298085-Activities-Da_Nang.html'

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()

        page.goto(page_url, timeout=60000)

        new_page = None

        def on_new_page(event_page):
            nonlocal new_page
            new_page = event_page

        context.on("page", on_new_page)

        page.wait_for_load_state('load')


        categories = page.locator('//button[@class="OKHdJ z Pc PQ Pp PD W _S Gn Rd _M PQFNM wSSLS"]').all()

        print(f'There are: {len(categories)} categories.')

        with page.expect_popup() as popup_info:
            page.locator('//a[@class="BMQDV _F Gv wSSLS SwZTJ"]/button[@class="OKHdJ z Pc PQ Pp PD W _S Gn Rd _M PQFNM wSSLS"]').first.click()

        new_page = popup_info.value

        new_page.wait_for_load_state('load')

        time.sleep(10)
        # hotels_list = []
        # for hotel in hotels:
        #     hotel_dict = {}
        #     hotel_dict['khách sạn'] = hotel.locator('//div[@class="nBrpc o W"]').inner_text()
        #     hotel_dict['giá'] = hotel.locator('//span[@data-automation="metaRegularPrice"]').inner_text()
        #     hotel_dict['đánh giá'] = hotel.locator('//div[@class="luFhX o W f u w JSdbl"]').get_attribute('aria-label').split(". ")[0]
        #     # hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
        #     hotel_dict['lượt review'] = hotel.locator('//span[@class="S4"]').inner_text().split()[0]
        #
        #     hotels_list.append(hotel_dict)
        #
        # df = pd.DataFrame(hotels_list)
        # df.to_excel('hotels_list2.xlsx', index=False)
        # df.to_csv('hotels_list2.csv', index=False)

        browser.close()


if __name__ == '__main__':
    main()