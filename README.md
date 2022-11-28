<h2>Analysis_of_prices</h2>
Цель проекта - визуализация данных о средних ценах на товары, взятых из Excel-таблиц c сайта https://www.belstat.gov.by/, выборка этих данных по ключевым словам.<br><br>
Проект написан в двух версиях: консольная - Excel_to_DataFrame (Console).py: удобочитаемо визуализирует данные - идеально для Data Scientist инженеров.
Вторая версия - телеграм-бот, который позволит всем желающим оперативно получить информацию о средних ценах без необходимости ее поиска по Excel-таблицам Белстата (а в них почти по 400 строк).
<br><br>
Движок проекта написан с использованием ООП (файл classes.py), библиотеки Pandas и ее основного объекта DataFrame.<br>
Pet-проект будет дорабатываться и дополняться функционалом. <br>
<h2>Запуск из терминала проекта:</h2><br>
<code>pip install pandas tabulate xlrd pyTelegramBotAPI requests</code><br>
<h4>Если в процессе выполнения программы будут ошибки, дополнительно прописать в терминале:</h4><br>
<code>pip install --upgrade xlrd</code><br>
