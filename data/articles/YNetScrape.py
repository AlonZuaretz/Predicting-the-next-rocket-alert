
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def Save_Lists(main_titles_list, sub_titles_list, date_time_list, total_samples, page_number):

    N = len(main_titles_list)
    sample = total_samples - N + 1
    # Open the file in append mode to add new titles without overwriting previous ones
    with open('Main_Titles.txt', 'a', encoding='utf-8') as file:
        file.write(f"Page Number: {page_number}\n\n")
        for ind, title in enumerate(main_titles_list):
            file.write(f"Sample number: {sample}\n")
            file.write(f"{title}\n\n")  # Write each string followed by two new lines
            sample = sample + 1

    sample = total_samples - N + 1
    with open('Sub_Titles.txt', 'a', encoding='utf-8') as file:
        file.write(f"Page Number: {page_number}\n\n")
        for ind, title in enumerate(sub_titles_list):
            file.write(f"Sample number: {sample}\n")
            file.write(f"{title}\n\n")  # Write each string followed by two new lines
            sample = sample + 1

    sample = total_samples - N + 1
    with open('Date_Time.txt', 'a', encoding='utf-8') as file:
        file.write(f"Page Number: {page_number}\n\n")
        for ind, title in enumerate(date_time_list):
            file.write(f"Sample number: {sample}\n")
            file.write(f"{title}\n\n")  # Write each string followed by two new lines
            sample = sample + 1


def Save_Fail(i, page_number):
    with open('Failures.txt', 'a', encoding='utf-8') as file:
        file.write(f"Article {i + 1} failed at page: {page_number}\n\n")  # Write each string followed by two new lines

def find_with_multiple_selectors(driver, selectors, wait_time = 20):
    """
    Tries to find an element using multiple CSS selectors.
    Returns the first element found or raises a TimeoutException if none are found.
    """
    for selector in selectors:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element  # Return the first found element
        except TimeoutException:
            # Continue to the next selector if the current one fails
            pass
    # If none of the selectors work, raise a TimeoutException
    raise TimeoutException(f"None of the selectors matched: {selectors}")



def YNetDriver():
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()  # Make sure chromedriver is in PATH or specify its location

    url_0 = "https://www.ynet.co.il/topics/%D7%9E%D7%9C%D7%97%D7%9E%D7%94/34"

    driver.get(url_0)

    # Allow the page to load
    # time.sleep(5)  # Adjust the sleep time based on your connection speed
    wait = WebDriverWait(driver, 20)

    # Find all image elements in the list
    IMGS = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".imageView")))

    # Define multiple possible CSS selectors for all three interesting blocks

    main_title_selectors = [
        "div.mainTitleWrapper h1.mainTitle",  # First option
        "div.PremiumArticleHeaderComponenta div.title" ]  # ynet+ articles

    # For samples in pages 1 - 79, it's better to put the option with h2 first, for all the older pages it's better
    # putting the line without h2 first, saves time this way
    # The same for the last two lines for the  ynet+, for the recent pages put span.subTitle line first, for older pages
    # put the line that doesn't have span.subTitle first for the same reason.
    sub_title_selectors = [
        "div.subTitleWrapper span.subTitle",  # First option
        "div.subTitleWrapper h2 span.subTitle",  # Alternative option
        "div.PremiumArticleHeaderComponenta div.subTitle",  # ynet+ articles option 1
        "div.PremiumArticleHeaderComponenta div.subTitle span.subTitle" ]  # ynet+ articles option 2

    date_time_selectors = [
        "div.authoranddate div.authors span.date time.DateDisplay",  # First option
        "div.PremiumArticleHeaderComponenta div.bottomSection div.publicationDetails div.date" ]  # ynet+ articles

    total_samples = 0
    page_number = 0



    for j in range(248):
        main_titles_list = []
        sub_titles_list = []
        date_time_list = []

        curr_page_url = driver.current_url

        page_number = page_number + 1
        print("Page Number: " + str(page_number))

        # Iterate through the articles
        for i in range(len(IMGS)):
            try:
                print('1')
                # Find the images again, as the DOM may refresh after navigating back
                IMGS = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".imageView")))

                print('2')
                # Click on the current image
                IMGS[i].click()
                print(f"Clicked on image {i + 1}")

                # Perform actions on the new page here (e.g., scrape data)
                print('3')
                # Wait for main_title element to appear on the new page
                main_title = find_with_multiple_selectors(driver, main_title_selectors)
                print('4')
                # Wait for sub_title element to appear on the new page
                sub_title = find_with_multiple_selectors(driver, sub_title_selectors)
                print('5')
                # Wait for date_time element to appear on the new page
                date_time = find_with_multiple_selectors(driver, date_time_selectors)

                # Extract the text content of the div
                main_title_text = main_title.text
                sub_title_text = sub_title.text
                date_time_text = date_time.text
                print(f"Extracted Main Title: {main_title_text}")
                print(f"Extracted Sub Title: {sub_title_text}")
                print(f"Extracted Date Time: {date_time_text}")

                # Save the information (for example, into a list or file)
                # Here, appending to a list:
                main_titles_list.append(main_title_text)
                sub_titles_list.append(sub_title_text)
                date_time_list.append(date_time_text)
                print('6')
                # Go back to the previous page
                driver.back()
                print(f"Returned to the main page after article {i + 1}")
                print('7')
                # The bottom line lets the thing wait 30 more seconds after pressing back, to make sure
                # it doesn't fuck up in going back
                WebDriverWait(driver, 20).until(  # Increase the timeout value here
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

            except TimeoutException:
                print('8')
                # Quit the driver
                driver.quit()
                time.sleep(10)

                # Go back to the previous page when failed totally
                driver = webdriver.Chrome()  # Make sure chromedriver is in PATH or specify its location
                driver.get(curr_page_url)

                print('9')
                # The bottom line lets the thing wait 30 more seconds after pressing back, to make sure
                # it doesn't fuck up in going back
                WebDriverWait(driver, 60).until(  # Increase the timeout value here
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                print('10')
                # Saves to txt which article failed
                Save_Fail(i, page_number)

                print(f"Returned to the main page after failure at article {i + 1} in page {page_number}")
                if i == 10:
                    total_samples = total_samples + len(main_titles_list)

                    print('11')
                    # Open the file in append mode to add new titles without overwriting previous ones
                    # Save_Lists(main_titles_list, sub_titles_list, date_time_list, total_samples, page_number)

                    print('12')
                    # Wait for next page button
                    next_page = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//a[@title="כתבות נוספות"]'))
                    )

                    print('13')
                    # Click the link
                    next_page.click()

                else:
                    i = i + 1

        total_samples = total_samples + len(main_titles_list)

        print('14')
        # Save Lists to file
        Save_Lists(main_titles_list, sub_titles_list, date_time_list, total_samples, page_number)

        print('15')
        # Wait for next page button
        next_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@title="כתבות נוספות"]'))
        )

        print('16')
        # Click the next page button
        next_page.click()

    print('17')
    # Quit the driver
    driver.quit()
    # return main_titles_list, sub_titles_list, date_time_list, fail_count, fail_count_ind_list


if __name__ == '__main__':
    # main_titles_list, sub_titles_list, date_time_list, fail_count, fail_count_ind_list = funky_func()
    YNetDriver()

