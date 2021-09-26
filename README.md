YatubeProject
-
Данный проект представляет собой социальную сеть, где пользователь после регистрации:

*Может создать пост(текст + картинка)

*Редактировать или удалять свои посты

*Под любым постом оставлять комментарии

*Подписываться на других пользователей

*Узнать о стеке технологий(ссылка снизу - технологии)

*Прочитать о создателе данного проекта(ссылка снизу - Об авторе)

*Открыть ленту избранных авторов


Развертывание проекта
-
1. Зайдите/установите GitBash
2. При помощи команд cd "каталог" - перейти в каталог и cd .. - подняться на уровень вверх, перейдите в нужный каталог для копирования репозитория
3. Введите команду git clone https://github.com/GorsheninNikolay/YatubeProject
4. В данном каталоге при помощи терминала Git выполните команду python -m venv venv для создания виртуальный среды
5. Затем введите команду source venv/Scripts/activate - команда для активации виртуальной среды
6. Дальше в консоли выполните команду pip install -r requirements.txt для загрузки нужных инструментов
7. Далее введите команду cd yatube, чтобы перейти в каталог yatube
8. Выполните команду python manage.py makemigrations и python manage.py migrate для создания миграций
9. Заключительный этап - ввод команды python manage.py runserver для открытия сервера с данным проектом
Удерживайте ctrl и левой кнопкой мыши нажмите на появившийся ip адрес
Готово! =)

Стек используемых технологий
-
В данном проекте я использовал:

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
