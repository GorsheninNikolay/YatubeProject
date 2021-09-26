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


Развертывание проекта
-
1. Зайдите/установите GitBash
2. При помощи команд cd "каталог" - перейти в каталог и cd .. - подняться на уровень вверх, перейдите в нужный каталог для копирования репозитория
3. Введите команду git clone https://github.com/GorsheninNikolay/YatubeProject
4. Введите в консоли cd YatubeProject и выполните команду python -m venv venv для создания виртуальный среды
5. Затем введите команду source venv/Scripts/activate - команда для активации виртуальной среды
6. Далее в консоли выполните команду pip install -r requirements.txt для загрузки нужных инструментов
7. После введите команду cd yatube, чтобы перейти в каталог yatube
8. Выполните команду python manage.py migrate для создания миграций
9. Заключительный этап - ввод команды python manage.py runserver для открытия сервера с данным проектом
Удерживайте ctrl и левой кнопкой мыши нажмите на появившийся ip адрес, если он не появился, то перейдите по адресу: http://127.0.0.1:8000/

Готово! =)

Системные требования
-
Python 3.7.3

GitBash

Стек используемых технологий
-

BackEnd
-
*Django v 2.2.6

*Python 2.7

*GitBash

FrontEnd
-
*Программу NicePage

*HTML

*CSS

*JavaScript
