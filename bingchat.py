"""
The script uses Selenium and Bing Chat to browse search results and extract the answer from the chatbot.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time 
from icecream import ic

def get_shadow_root(driver, element):
    """Return the shadow root of a given web element."""
    return driver.execute_script('return arguments[0].shadowRoot', element)


def bing_search(prompt):

    # Create an instance of the Edge WebDriver
    edge_path = './bin/msedgedriver.exe'
    service = Service(executable_path=edge_path)

    # Set EdgeOptions to open an incognito window
    options = Options()
    options.add_argument("--inprivate")

    # start the driver
    driver = webdriver.Edge(service = service, options = options)

    # enlarge the window
    driver.maximize_window()

    # Open Bing
    url = "https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx"
    driver.get(url)
    # Wait for the page to load completely
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="b_sydConvCont"]/cib-serp'))
    )
    time.sleep(5)

    # Start with the outermost host element
    host_element = driver.find_element(By.XPATH, '//*[@id="b_sydConvCont"]/cib-serp')
    shadow_root = get_shadow_root(driver, host_element)
    print(f">>> {1}")
    ic(shadow_root)

    # the second layer
    host_element2 = shadow_root.find_element(By.CSS_SELECTOR, '#cib-conversation-main')
    shadow_root2 = get_shadow_root(driver, host_element2)
    print(f">>> {2}")
    ic(shadow_root2)

    # the third layer: the conversation style box an the input box diverge here
    host_element3 = shadow_root2.find_element(By.CSS_SELECTOR, "cib-welcome-container[product='bing'][chat-type='consumer']")
    shadow_root3 = get_shadow_root(driver, host_element3)
    print(f">>> {3}")
    ic(shadow_root3)

    conversation_style_box = shadow_root3.find_element(By.CSS_SELECTOR, "cib-tone-selector[product='bing'][chat-type='consumer'][visible]")
    shadow_root_stylebox = get_shadow_root(driver, conversation_style_box)
    print(f">>> {4}: conversation_style_box")
    ic(shadow_root_stylebox)
    # click the precise button
    button = shadow_root_stylebox.find_element(By.CSS_SELECTOR, "button.tone-precise[role='radio']")
    print(f">>> {5}: button")
    ic(button)
    button.click()
    time.sleep(1)

    # find text input
    host_element_text = shadow_root.find_element(By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main")
    shadow_root_text = get_shadow_root(driver, host_element_text)
    print(f">>> {6}: text")
    ic(shadow_root_text)

    host_element_text2 = shadow_root_text.find_element(By.CSS_SELECTOR, "cib-text-input[serp-slot='none'][product='bing'][mode='conversation'][alignment='left']")
    shadow_root_text2 = get_shadow_root(driver, host_element_text2)
    print(f">>> {7}: text input")
    ic(shadow_root_text2)
    
    textarea_element = shadow_root_text2.find_element(By.CSS_SELECTOR, "textarea#searchbox")
    print(f">>> {8}: textarea")
    ic(textarea_element)

    # send text
    textarea_element.send_keys(prompt)
    # hist enter
    textarea_element.send_keys(Keys.RETURN)
    # Wait for the chat reply
    time.sleep(60)
    WebDriverWait(shadow_root2, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "cib-chat-turn[serp-slot='none']"))
    )

    # find the returned chat
    host_element_returnedchat = shadow_root2.find_element(By.CSS_SELECTOR, "cib-chat-turn[serp-slot='none']")
    shadow_root_returnedchat = get_shadow_root(driver, host_element_returnedchat)
    print(f">>> {9}: reply")
    ic(shadow_root_returnedchat)

    host_element_returnedchat2 = shadow_root_returnedchat.find_element(By.CSS_SELECTOR, "cib-message-group.response-message-group[source='bot'][serp-slot='none']")
    shadow_root_returnedchat2 = get_shadow_root(driver, host_element_returnedchat2)
    print(f">>> {10}: reply")
    ic(shadow_root_returnedchat2)

    host_element_returnedchat3 = shadow_root_returnedchat2.find_element(By.CSS_SELECTOR, "cib-message[type='text'][source='bot'][serp-slot='none'][product='bing']")
    shadow_root_returnedchat3 = get_shadow_root(driver, host_element_returnedchat3)
    print(f">>> {11}: reply")
    ic(shadow_root_returnedchat3)

    host_element_returnedchat4 = shadow_root_returnedchat3.find_element(By.CSS_SELECTOR, "cib-shared[serp-slot='none']")
    shadow_root_returnedchat4 = get_shadow_root(driver, host_element_returnedchat4)
    print(f">>> {12}: reply")
    ic(shadow_root_returnedchat4)

    replied_text = shadow_root_returnedchat3.find_element(By.CSS_SELECTOR, "cib-shared[serp-slot='none']")
    print(f">>> {12.5}: reply")
    ic(replied_text)
    replied_text = replied_text.find_element(By.CSS_SELECTOR, 'div.content[tabindex="0"]')
    print(f">>> {13}: reply")
    ic(replied_text)
    ic(replied_text.text)

    replied_text_p = replied_text.find_element(By.CSS_SELECTOR, "p")
    print(f">>> {14}: reply")
    ic(replied_text_p)
    ic(replied_text_p.text)

    replied_text_a = replied_text.find_element(By.CSS_SELECTOR, "a")
    print(f">>> {15}: reply")
    ic(replied_text_a)
    # get all the links from the reply
    ic(replied_text_a.get_attribute('href'))

    answer =  {
        "text": replied_text.text,
        "link" : replied_text_a.get_attribute('href')
    } 

    driver.quit()  # Close the browser
    return answer


if __name__ == "__main__":

    keywords = ['google', 'meta', 'microsoft']

    for keyword in keywords: 

        prompt = f"What is {keyword}'s stock price today?"
        answer = bing_search(prompt)
        print(answer)

