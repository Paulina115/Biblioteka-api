# Biblioteka API

Aplikacja w **FastAPI** do zarządzania biblioteką (użytkownicy, książki, rezerwacje, historia wypożyczeń) w **architekturze cebulowej**, z autoryzacją JWT i obsługą **asynchronicznej bazy danych**.

---

## Stos technologiczny

- **Python 3.12** – logika backendu, OOP, programowanie asynchroniczne  
- **FastAPI** – REST API, walidacja danych (Pydantic), dependency injection  
- **SQLAlchemy 2.0 (async)** – ORM, relacje, zapytania  
- **PostgreSQL** – baza danych  
- **JWT / OAuth2** – autoryzacja i role użytkowników  
- **Dependency Injector** – zarządzanie zależnościami  
- **Docker** – konteneryzacja  

---

## Funkcjonalności

- Zarządzanie użytkownikami (rejestracja, aktualizacja, role, logowanie)  
- Obsługa książek i ich kopii (dodawanie, aktualizacja, dostępność)  
- Rezerwacje książek i historia wypożyczeń  
- Autoryzacja i role użytkowników (user, librarian)  

---

## Uruchomienie

1. Sklonuj repozytorium:
   
git clone https://github.com/twoj_uzytkownik/biblioteka-api.git
cd biblioteka-api

Zbuduj i uruchom kontener:

docker-compose up --build



