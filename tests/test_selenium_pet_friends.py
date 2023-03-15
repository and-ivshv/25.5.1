import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password

def test_my_pets():
    # неявное ожидание 5 сек при каждом шаге
    pytest.driver.implicitly_wait(5)
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что оказались на главной странице всех питомцев пользователей
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'

    # Переходим на страницу со списком питомцев пользователя
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    # явное ожидание 10 сек.
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))

    # Проверяем, что оказались на странице питомцев пользователя
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    # Находим соответствие кол-ва питомцев по статистике пользователя кол-ву питомцев в таблице.
    pets_number = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)

    # Проверяем, что у всех питомцев есть имя, возраст и порода и хотя бы у половины есть фото
    images = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img')
    names = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')
    breeds = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]')

    images_count = 0
    for i in range(len(pets_count)):
        if 'base64' in images[i].get_attribute('src'):
            images_count = images_count + 1
        else:
            images_count = images_count
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
    print(images_count)
    assert images_count / len(pets_count) >= 0.5

    # Проверяем, что у всех питомцев разные имена
    list_names = []
    for i in range(len(pets_count)):
        list_names.append(names[i].text)
    set_names = set(list_names)
    assert len(set_names) == len(list_names)

    # Проверяем, что в списке нет повторяющихся питомцев
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    pets_data = [pet.text for pet in all_pets]
    uniq_pets = set(pets_data)
    assert len(pets_data) == len(uniq_pets)