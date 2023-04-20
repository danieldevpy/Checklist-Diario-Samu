from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class TestCaseSelenium(unittest.TestCase):
        
        def setUp(self):
            self.options = ChromeOptions()
            self.options.headless = True
            self.driver = webdriver.Chrome(chrome_options=self.options, service=ChromeService(ChromeDriverManager().install()))

        def test_complete(self):
            self.driver.get("http://localhost:8000/")
            name = self.driver.find_element(By.NAME, "unity")
            name.send_keys("admin")
            passw = self.driver.find_element(By.NAME, "password")
            passw.send_keys("admingeral")
            btn = self.driver.find_element(By.XPATH, '/html/body/main/div/form/div/input[3]')
            btn.click()

            pacotes = self.driver.find_elements(By.ID, "pacote")
            btns = self.driver.find_elements(By.CLASS_NAME, "btn")
            inputs = self.driver.find_elements(By.CLASS_NAME, "input")
            for i, inputx in enumerate(inputs):
                if i == 0:
                    pacotes[0].click()
                # voltar
                if i == 6:
                    btns[0].click()
                    time.sleep(1)
                    pacotes[1].click()
                if i == 66:
                    btns[1].click()
                    time.sleep(1)
                    pacotes[2].click()
                if i == 123:
                    btns[2].click()
                    time.sleep(1)
                    pacotes[3].click()
                if i == 169:
                    btns[3].click()
                    time.sleep(1)
                    pacotes[4].click()
                if i == 191:
                    btns[4].click()
                    time.sleep(1)
                    pacotes[5].click()
                    namec = self.driver.find_element(By.NAME, "nomecompleto")
                    namec.send_keys("Teste Unitario")
                    cargo = self.driver.find_element(By.NAME, "cargo")
                    cargo.send_keys("ROBO")
                    km = self.driver.find_element(By.NAME, "km")
                    km.send_keys("0000")
                    btns[5].click()
                    time.sleep(5)
                    break

                inputx.send_keys(f'{i}')
                time.sleep(0.1)
            self.assertIn("Finalizado", self.driver.title)


if __name__ == "__main__":
    unittest.main()
