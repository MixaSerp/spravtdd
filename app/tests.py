# app/tests.py
import pytest
from django.urls import reverse
from django.db import IntegrityError
from app.models import Term

# ==========================================
# ТЕСТЫ ДЛЯ МОДЕЛИ (БАЗА ДАННЫХ)
# ==========================================

@pytest.mark.django_db
def test_term_creation():
    """Проверка создания термина"""
    term = Term.objects.create(
        name="Компьютерная информация",
        definition="Сведения в форме электрических сигналов",
        gost_name="ГОСТ Р 58432-2019",
        gost_link=""
    )
    assert term.name == "Компьютерная информация"
    assert Term.objects.count() == 1

@pytest.mark.django_db
def test_term_unique_name():
    """TDD Step 2: Проверка уникальности названия"""
    Term.objects.create(
        name="Тестовый термин",
        definition="Определение 1",
        gost_name="ГОСТ 1",
        gost_link=""
    )
    
    with pytest.raises(IntegrityError):
        Term.objects.create(
            name="Тестовый термин",
            definition="Определение 2",
            gost_name="ГОСТ 2",
            gost_link=""
        )

# ==========================================
# ТЕСТЫ ДЛЯ СТРАНИЦЫ И ПОИСКА (VIEWS)
# ==========================================

@pytest.mark.django_db
def test_main_page_status_code(client):
    """Проверка, что главная страница доступна (код 200)"""
    url = reverse('term_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_main_page_contains_terms(client):
    """Проверка, что термины отображаются на странице"""
    Term.objects.create(name="Абап", definition="Язык SAP", gost_name="ГОСТ")
    Term.objects.create(name="Баг", definition="Ошибка", gost_name="ГОСТ")
    
    url = reverse('term_list')
    response = client.get(url)
    
    content = response.content.decode('utf-8')
    assert "Абап" in content
    assert "Баг" in content

@pytest.mark.django_db
def test_search_functionality(client):
    """Проверка работы поиска по терминам"""
    Term.objects.create(name="Абап", definition="Язык программирования SAP", gost_name="ГОСТ")
    Term.objects.create(name="Баг", definition="Ошибка в программе", gost_name="ГОСТ")
    Term.objects.create(name="Бэкап", definition="Резервное копирование", gost_name="ГОСТ")
    
    url = reverse('term_list')
    response = client.get(url, {'q': 'Баг'})
    
    content = response.content.decode('utf-8')
    assert "Баг" in content
    assert "Ошибка" in content

@pytest.mark.django_db
def test_main_page_groups_by_letter(client):
    """Проверка группировки терминов по буквам"""
    Term.objects.create(name="Абап", definition="Опр А", gost_name="ГОСТ")
    Term.objects.create(name="Ава", definition="Опр А2", gost_name="ГОСТ")
    Term.objects.create(name="Баг", definition="Опр Б", gost_name="ГОСТ")
    
    url = reverse('term_list')
    response = client.get(url)
    
    content = response.content.decode('utf-8')
    assert "А" in content
    assert "Б" in content