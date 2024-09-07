import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

from infrastructure.exception import ValidationException
from infrastructure.webdrive.SelectorType import SelectorType

class WebDriveSelenium:
    def __init__(self, webdriver, url_test: str) -> None:
        self.webdriver = webdriver
        self.url_test = url_test
        self.screenshots = []
    
    def highlight_element(self, element):
        self.webdriver.execute_script("arguments[0].style.border='3px solid red'", element)

    def save_screenshot(self, step_name: str):
        self.screenshots.append({'step_name': step_name, 'image': self.webdriver.get_screenshot_as_png()})

    def check_captcha(self):
        try:
            recaptcha_iframe = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
            )
            if recaptcha_iframe:
                print("reCAPTCHA detectado dentro de um iframe! Teste não pode continuar.")
                self.save_screenshot('captcha_detected.png')
                return True

            captcha_present = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "g-recaptcha"))
            )
            if captcha_present:
                print("CAPTCHA detectado diretamente na página! Teste não pode continuar.")
                self.save_screenshot('captcha_detected.png')
                return True
            return False
        except Exception as error:
            return False
    
    def step_input(self, type: str, element: str, value: str, validation: dict):
        field = self.webdriver.find_element(SelectorType[type].value, element)
        self.highlight_element(field)
        field.send_keys(value)
        msg = field.get_attribute("validationMessage")
        validation_result = msg == validation['message']
        if validation_result is False:
            raise ValidationException(f'"{msg}" != "{validation["message"]}"')
        self.save_screenshot(f'{element}_filled')
        time.sleep(2)
        return validation_result
    
    def step_click(self, type: str, element: str, value: str = None, validation: dict = None):
        send_button = WebDriverWait(self.webdriver, 10).until(
            EC.element_to_be_clickable((SelectorType[type].value, element))
        )
        self.highlight_element(send_button)
        self.save_screenshot('before_click')
        send_button.click()

    def __step_type(self, type: str):
        type_step = {
            'input': self.step_input,
            'click': self.step_click
        }
        return type_step[type]

    def execute(self, url: str, steps: dict):
        note = ''
        try:
            validations = []
            self.webdriver.get(url)
            self.save_screenshot('initial_load')

            for step in steps:
                step_executor = self.__step_type(step['action_type'])
                validation_result = step_executor(step['type'], step['element'], step['value'], step['validations_field'])
                validations.append(validation_result)

            time.sleep(1)
            if self.check_captcha():
                note = 'Teste concluido porem reCAPTCHA foi detectado'
        except Exception as e:
            error_screenshot_name = f"error_{time.strftime('%Y%m%d_%H%M%S')}"
            self.save_screenshot(error_screenshot_name)
            self.webdriver.quit()
            print(f"An error occurred: {str(e)}")
            raise e
        finally:
            self.webdriver.quit()
            return note
