# MyCurrency Project
 
MyCurrency is a Django-based web platform that allows users to calculate currency exchange rates using data from multiple external providers, including CurrencyBeacon. This project implements a flexible architecture with the Adapter Design Pattern to manage currency exchange rates efficiently.
 
## Table of Contents
- [Project Setup](#project-setup)
- [Configure Database](#configure-datebase)
- [Running the Project](#running-the-project)
- [Celery Setup](#celery-setup)
- [Redis Setup](#redis-setup)
- [Services](#services)
- [Contributing](#contributing)
- [APIs Collection](#apis-collection)
- [Summary Of APIS](#apis-summary)



 
## Project Setup

**I am using Windows**
 
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/prashanthchaduvala/Mycurrency.git
   
2. **Navigate to the Project Directory**
    - cd MyCurrency
  
3. **Create a Virtual Environment**
    - python -m venv currency-venv

4. **Activate a Virtual Environment**
 . On Windows:
    - currency-venv\Scripts\activate.bat
 . On macOS/Linux:
    - source currency-venv/bin/activate

5. **Checkout the Master Branch:**
 - git checkout master


6. **Install Dependencies :**
    - pip install -r requirements.txt

## Configure Database

    . Update your settings.py with your database configuration.
    
- I am using default django provided database
        >> SQLITE3
        >> DATABASES = {
        >> 'default': {
        >>    'ENGINE': 'django.db.backends.sqlite3',
        >>    'NAME': BASE_DIR / 'db.sqlite3',
        >>    }
        >> }
- If you want change the databse use this code 

        >> DATABASES = {
        >>     'default': {
        >>         'ENGINE': 'django.db.backends.mysql',
        >>         'NAME': 'databse name',
        >>         'USER': 'databse username',
        >>         'PASSWORD': 'databse password',
        >>         'HOST':'host number',
        >>         'PORT':'port number',
        >>         "OPTIONS": {
        >>               'ssl_disabled':True,
                    
        >>            }
        >>     }
        >> }
    >> . Run the following commands to create migrations and migrate the database generating tables & columns:
    - python manage.py makemigrations
    - python manage.py migrate




## Celery Setup
> Use below link to setup celery
 - https://www.geeksforgeeks.org/celery-integration-with-django/
- pip install celery
- pip install django
>  or
- pip install celery django-celery
  - Add celery and Django-celery-beat to the INSTALLED_APPS list in Django settings.
- 'celery',
 - In the Django project’s settings.py file, add the following code:
>> myproject/settings.py

    # set the celery broker url
    - CELERY_BROKER_URL = 'redis://localhost:6379/0'

    # set the celery result backend
    - CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # set the celery timezone
    - CELERY_TIMEZONE = 'UTC'
>> In the Django project’s __init__.py file, add the following code:
>. myproject/__init__.py

 - from .celery import app as celery_app

 - __all__ = ['celery_app']
>> Create a Celery instance in the Django project. This is typically done in a file called celery.py in our Django project root:
    # mycurrency/celery.py

    import os
    from celery import Celery

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault
        ('DJANGO_SETTINGS_MODULE', 'gfg.settings')

    app = Celery('gfg')

    # Using a string here means the worker doesn't 
    # have to serialize the configuration object to 
    # child processes. - namespace='CELERY' means all 
    # celery-related configuration keys should 
    # have a `CELERY_` prefix.
    app.config_from_object('django.conf:settings',
                        namespace='CELERY')

    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()

>> Celery Commands
 . celery -A gfg worker -l info
- if using the periodic task feature 
 . celery -A gfg beat -l info 

## Redis Setup
> I am using windows so this commands for windows 
 - https://github.com/microsoftarchive/redis/releases


## Running the Project
    - after installing the dependencies & settings
    - run server using below command 
    - git checkout master
    >> python manage.py runserver 8001



## Services
 
The MyCurrency platform interacts with external APIs and implements several key services to ensure smooth functionality. Below is an overview of the services used in the project:
 
### 1. **Currency Exchange Rate Data Service**
   This service interacts with external providers like **CurrencyBeacon** to retrieve and update the currency exchange rates.
 
   - **Adapter Design Pattern**: We use this pattern to integrate multiple currency providers while keeping the rest of the platform unaware of the specific provider details. The system can be easily extended to support new providers by implementing the required adapter.
 
   - **Provider Resilience**: In case one provider fails, the system dynamically switches to the next available provider based on their priority.
 
   - **Endpoints:**
     - `/update-exchange-rates/`: Fetches the latest exchange rates from active providers and updates the local database.
     - `/currency-rates/`: Retrieves historical or recent exchange rates from the local database for a specific currency and date range.
 
   - **Priority Management**: Providers can be activated or deactivated at runtime, and their priority can be changed dynamically, allowing for flexible integration and failure management.
 
### 2. **Currency Conversion Service**
   This service provides the ability to convert a specific amount from one currency to another using the most recent available exchange rate.
 
   - **External API Interaction**: The conversion rates are fetched from **CurrencyBeacon** or other external providers, ensuring up-to-date and accurate conversion data.
 
   - **Endpoint:**
     - `/convert/`: Allows users to convert a specific amount from a source currency to a target currency.
 
   - **Parameters:**
     - `from_currency`: The base currency to convert from.
     - `to_currency`: The target currency to convert to.
     - `amount`: The amount to convert.
   
### 3. **Back Office Services (Admin Panel)**
   The back-office/admin interface allows administrators to manage currencies and exchange rates. It provides the following functionalities:
   
   - **Currency Management**: Admins can add, edit, or delete currency records.
   - **Currency Converter View**: Admins can use the online currency converter to quickly convert between currencies.
 
   These admin functionalities simplify the maintenance of the system and allow for manual intervention when necessary.
 
### 4. **Historical Data Loader (Asynchronous Task)**
   This service handles the loading of historical exchange rate data, which may involve processing large datasets.
 
   - **Async Task with Celery**: This task is handled asynchronously using Celery to ensure that historical data is loaded efficiently without blocking other operations of the platform.
 
   - **Task Trigger**: The task can be triggered manually from the admin panel or via scheduled jobs.
 
### 5. **Mock Data Provider (For Testing)**
   In addition to live data from **CurrencyBeacon**, a mock provider is implemented to generate random exchange rate data for testing purposes. This ensures that the platform can be thoroughly tested without relying on live data, which may not always be available or suitable for testing.
 
   - **Adapter Integration**: The mock provider is integrated seamlessly using the Adapter pattern, just like the live providers.
 
### 6. **Caching and Database Interaction**
   To optimize performance, the platform stores fetched exchange rates in the local database. If a request for exchange rate data is made and the data is already available in the database, it retrieves the data from the local store rather than calling the external API again.
 
   This approach reduces the number of external API calls, improving performance and minimizing API usage costs.
 
## Summary of API Endpoints
 
- `/update-exchange-rates/`: Updates exchange rates using external providers.
- `/currency-rates/`: Retrieves exchange rate data for a specific time period.
- `/convert/`: Converts a specified amount from one currency to another.
 


## APIs Collection

### 1. `/currency-rates/` (GET)
   **Description**: This endpoint retrieves a list of currency exchange rates for a specified period.
   
   **Parameters**:
   - `source_currency` (required): The source currency code (e.g., `EUR`).
   - `date_from` (required): The start date of the period for which to retrieve exchange rates (format: `YYYY-MM-DD`).
   - `date_to` (required): The end date of the period for which to retrieve exchange rates (format: `YYYY-MM-DD`).
   
   **Expected Response**: A time series list of exchange rates for the specified currency and date range.
   
   **Example Usage**: source_currency=EUR&date_to=2024-10-22&date_from=2024-10-22

### 2. `/convert/` (GET)
**Description**: This endpoint performs a currency conversion between two specified currencies using the latest available exchange rates.
 
**Parameters**:
- `source_currency` (required): The base currency code to convert from (e.g., `USD`).
- `exchanged_currency` (required): The target currency code to convert to (e.g., `EUR`).
- `amount` (required): The amount to convert.
 
**Expected Response**: A JSON object containing the conversion result, including the rate and converted value.
 
**Example Usage**: source_currency=SBD&exchanged_currency=AED&amount=100

 
### 3. `/currencies/` (GET/POST)
**Description**: This endpoint retrieves a list of all available currencies or allows for the creation of a new currency.
 
**GET Parameters**: None.
 
**POST Parameters**:
- `code` (required): The currency code (e.g., `USD`).
- `name` (required): The name of the currency (e.g., `United States Dollar`).
- `symbol` (optional): The currency symbol (e.g., `$`).
 
**Expected Response**: A list of available currencies or a success response after creating a new currency.
 
**Example Usage**:sample data  [{"id":1,"code":"AED","name":"UAE Dirham","symbol":"د.إ"},{"id":2,"code":"AFN","name":"Afghani","symbol":"؋"},{"id":3,"code":"ALL","name":"Lek","symbol":"L"},{"id":4,"code":"AMD","name":"Armenian Dram","symbol":"դր."},{"id":5,"code":"ANG","name":"Netherlands Antillean Guilder","symbol":"ƒ"}],,,,

### 4. `/currencies/<int:pk>/` (GET/PUT/DELETE)
**Description**: This endpoint allows retrieving, updating, or deleting a specific currency by its primary key (`pk`).
 
**Parameters**:
- `pk`: The primary key of the currency to retrieve, update, or delete.
 
**Expected Response**: The details of the requested currency, or a success response after updating/deleting a currency.
 
**Example Usage**: {
                        "id": 1,
                        "code": "AED",
                        "name": "UAE Dirham",
                        "symbol": "د.إ"
                    }

### 5. `/v1/currency-rates/` (GET)
**Description**: This is a versioned endpoint for retrieving currency exchange rates. It provides backward compatibility if future API versions introduce breaking changes.
 
**Parameters**:
- `source_currency` (required): The source currency code (e.g., `EUR`).
- `date_from` (required): The start date of the period to retrieve rates.
- `date_to` (required): The end date of the period to retrieve rates.
 
**Expected Response**: A list of exchange rates between the specified dates for the given source currency.
 
**Example Usage**:


## Summary Of APIS

- `/currency-rates/`: Retrieve exchange rates for a specific currency and time range.
- `/convert/`: Convert a specified amount between two currencies.
- `/currencies/`: List or create available currencies.
- `/currencies/<int:pk>/`: Retrieve, update, or delete a specific currency by ID.
- `/v1/currency-rates/`: Retrieve currency rates with API versioning for backward compatibility.
 
These endpoints form the backbone of the **MyCurrency** platform, providing currency management and exchange rate data retrieval functionality. The `v1/currency-rates/` endpoint ensures that future changes to the API will not break current implementations using versioning.

