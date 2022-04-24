import os
import random
import datetime

from colorama import init, Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle


class InstagramBot:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.headless = True
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe")

    def login_and_get_cookies(self, user: str, password: str, recreate: bool = False) -> None:
        """
        Авторизация на сайте https://www.instagram.com/ и выгрузка куки для дальнейшего входа без пароля

        :param user: Логин аккаунта instagram
        :param password: Пароль аккаунта instagram
        :param recreate: Перезапись куки, если равен True
        """
        if os.path.isfile(os.getcwd() + f"\\{user}_cookies") and not recreate:
            print(Fore.LIGHTGREEN_EX + "Cookie already exists!")
        else:
            self.driver.get("https://www.instagram.com/")
            time.sleep(5)
            username_input = self.driver.find_element(by=By.NAME, value="username")  # ВВОД ЛОГИНА
            username_input.clear()
            username_input.send_keys(user)

            password_input = self.driver.find_element(by=By.NAME, value="password")  # ВВОД ПАРОЛЯ
            password_input.clear()
            password_input.send_keys(password)

            time.sleep(5)

            password_input.send_keys(Keys.ENTER)  # НАЖИМАЕМ ENTER

            time.sleep(10)

            # cookies
            pickle.dump(self.driver.get_cookies(), open(f"{user}_cookies", "wb"))

        self.driver.close()
        self.driver.quit()

    def send_message_to_instagram(self, users_list_direct: set, msg: str, img_path: list, user: str) -> None:
        """
        Отправка сообщений в директ (Instagram)

        :param users_list_direct: Аккаунты для рассылки сообщений
        :param msg: Сообщение
        :param img_path: Список изображений (при необходимости)
        :param user: Логин аккаунта, с которого будет происходить рассылка
        """
        init()
        try:
            self.driver.get("https://www.instagram.com/")
            time.sleep(5)
            for cookie in pickle.load(open(f"{user}_cookies", "rb")):
                self.driver.add_cookie(cookie)
            time.sleep(3)
            self.driver.refresh()
            time.sleep(5)

            print(Fore.LIGHTGREEN_EX + f"Uploaded {len(users_list_direct)} accounts! [{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%d/%m/%Y %H:%M:%S')}]")

            if self.driver.find_element(by=By.XPATH, value="/html/body/div[5]/div/div"):  # УБИРАЕМ КНОПКУ УВЕДОМЛЕНИЙ
                self.driver.find_element(by=By.XPATH, value="/html/body/div[5]/div/div/div/div[3]/button[2]").click()
            time.sleep(5)

            # ПЕРЕХОДИМ В ДИРЕКТ
            self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a").click()
            time.sleep(3)

            # КНОПКА ОТПРАВИТЬ СООБЩЕНИЕ В ДИРЕКТЕ
            self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
            time.sleep(7)

            # ВВОДИМ ПОЛУЧАТЕЛЯ
            for index, user in enumerate(users_list_direct):
                to_input = self.driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input")
                to_input.send_keys(user)
                time.sleep(3)

                # КНОПКА ВЫБОРА ПОЛУЧАТЕЛЯ
                self.driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/div/div[2]/div[2]").find_element_by_tag_name("button").click()
                time.sleep(5)

                # КНОПКА ДАЛЕЕ
                self.driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/div/div[1]/div/div[3]/div/button").click()
                time.sleep(5)

                # ВИДЖЕТ ВВОДА СООБЩЕНИЯ
                text_message_area = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
                text_message_area.clear()
                text_split = msg.split("\n")
                for text in text_split:
                    text_message_area.send_keys(text)
                    if text_split.index(text) != len(text_split) - 1:  # do what you need each time, if not the last element
                        text_message_area.send_keys(Keys.SHIFT + Keys.ENTER)
                time.sleep(5)
                text_message_area.send_keys(Keys.ENTER)
                time.sleep(5)

                print(Fore.LIGHTRED_EX + f"Message sent to {user}! [{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%d/%m/%Y %H:%M:%S')}]")
                time.sleep(3)

                if img_path:
                    send_img_input = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
                    for img in img_path:
                        send_img_input.send_keys(img)
                        time.sleep(random.randrange(3, 6))
                    print(Fore.LIGHTBLUE_EX + f"Images sent to {user}! [{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%d/%m/%Y %H:%M:%S')}]")
                print()
                print(Fore.LIGHTCYAN_EX + f"Completed {index + 1}/{len(users_list_direct)}")
                print()
                # ПЕРЕХОДИМ В ДИРЕКТ
                self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/div/div[1]/div/div[3]/div/div[2]/a").click()
                time.sleep(random.randrange(600, 620))  # ЗАСЫПАЕМ НА 600(ЖЕЛАТЕЛЬНО) СЕКУНД ПОСЛЕ ОТПРАВКИ СООБЩЕНИЯ

                if index != len(users_list_direct) - 1:
                    # КНОПКА ОТПРАВИТЬ СООБЩЕНИЕ В ДИРЕКТЕ
                    self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
                    time.sleep(7)
        except Exception as ex:
            print(ex)
            self.driver.close()
            self.driver.quit()
        finally:
            print(Fore.LIGHTYELLOW_EX + f"\nNewsletter completed! [{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%d/%m/%Y %H:%M:%S')}]")
            self.driver.close()
            self.driver.quit()
