English Version

## Accounting Platform

### Short Description

The platform allows users to log in or log out of the [pmsolution-facture.org](https://pmsolution-facture.org) site using their credentials. Once logged in, users can create factures categorized as either **internal** or **world**. Additionally, users can access a deductions application.

#### Features:
1. After logging in, users can:
   - Filter factures by name and other characteristics.
   - Select applications to navigate to from the main page.
   - Switch between internal and world factures on a dedicated page.
   - Translate existing text into the French language.

2. Permissions:
   - **Regular Users**: Can create, edit, update, and delete only their own factures.
   - **Admins**: Have full access to create, edit, update, and delete all factures.

3. **Security**:
   - An anti-brute-force mechanism is in place:
     - After 5 or more invalid login attempts, the system blocks the user's IP address.
   - All incoming requests are logged for auditing purposes.
   - Logs include details of user login and logout activities.

### Deployment Instructions

To build and run the application, use the following command:
```bash
docker-compose up --build
```

Russian Version
## Платформа для бухгалтерского учёта

### Краткое описание

Платформа позволяет пользователям входить и выходить из системы на сайте [pmsolution-facture.org](https://pmsolution-facture.org) с использованием своих учетных данных. После входа в систему пользователи могут создавать счета, которые делятся на категории: **внутренние** и **международные**. Также доступно приложение для вычетов.

#### Возможности:
1. После входа в систему пользователи могут:
   - Фильтровать счета по имени и другим характеристикам.
   - Выбирать приложения для перехода с главной страницы.
   - Переключаться между внутренними и международными счетами на отдельной странице.
   - Переводить существующий текст на французский язык.

2. Права доступа:
   - **Обычные пользователи**: Могут создавать, редактировать, обновлять и удалять только свои собственные счета.
   - **Администраторы**: Имеют полный доступ для создания, редактирования, обновления и удаления всех счетов.

3. **Безопасность**:
   - Реализован механизм защиты от брутфорса:
     - После 5 или более неудачных попыток входа система блокирует IP-адрес пользователя.
   - Все входящие запросы регистрируются для аудита.
   - Логи включают информацию о входе и выходе пользователей из системы.

### Инструкции по развертыванию

Чтобы собрать и запустить приложение, выполните следующую команду:
```bash
docker-compose up --build
