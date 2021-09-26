YatubeProject
-
Данный проект представляет собой социальную сеть, где пользователь после регистрации:

*Может создать пост(текст + картинка)

*Редактировать или удалять свои посты

*Под любым постом оставлять комментарии

*Подписываться на других пользователей

*Узнать о стеке технологий (ссылка снизу - технологии)

*Прочитать о создателе данного проекта (ссылка снизу - Об авторе)

*Открыть ленту избранных авторов

Реализована пагинация постов, регистрация с проверкой валидности введенных данных, кэширование, также написаны тесты для проверки работоспособности проекта


Развертывание проекта
-
1. Зайдите в GitBash, при необходимости установите
2. При помощи команд cd "каталог" - перейти в каталог и cd .. - подняться на уровень вверх, перейдите в нужный каталог для копирования репозитория
3. Клонирование репозитория:
```
git clone https://github.com/GorsheninNikolay/YatubeProject
```
4. Переход в каталог:
```
cd YatubeProject 
```
Создание виртуальной среды:
```
python -m venv venv 
```
5. Активация виртуальной среды:
```
source venv/Scripts/activate
```
6. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
7. Перейти в каталог
```
cd yatube
```
8. Создание миграций
``` 
python manage.py migrate 
```
9. Запуск проекта
```
python manage.py runserver
```
Удерживайте ctrl и левой кнопкой мыши нажмите на появившийся ip адрес, если он не появился, то перейдите по адресу: http://127.0.0.1:8000/

Готово! =)

Системные требования
-

Python 3.7.3

GitBash

Стек используемых технологий
-

### BackEnd
*Django v 2.2.6

*Python 3.7.3

*GitBash

### FrontEnd
*Программа NicePage

*HTML

*CSS

*JavaScript
