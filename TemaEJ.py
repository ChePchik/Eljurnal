# import re 
# import os
import funcEJ as f
# clear = lambda: os.system('cls')

while True:
  print('-----------------------------------')
  # clear()

  print("что будем делать")


  print("0. Авторизоваться")
  print("1. Создать файлики")
  print("2. Продублировать темы в файлах")
  print("3. Создать файл (пока теория)")
  print("4. Выставить темы")
  print("5. Проверить столбцы")
  print("6. Закрыть занятие")
  print("7. Открыть занятие")

  choice = int(input(''))
  # diir = "D:\\Desktop\\Desktop\\Пары\\2022-2023\\_журнал\\txt"
  # input('Какя директория: ')


  if choice==0:
    f.auth()

  if choice==1:
    ch1 = int(input('Теория - 1\Практика - 2: '))
    f.createFile(ch1)

  elif choice==2:
    ch2 = int(input('Теория - 1\\ Практика - 2: '))
    ch21 = int(input('Все -1. Или конкретно id:  '))
    print(f.spisok)
    f.dubleFileAll(ch2,ch21)

  elif choice==3:
    f.create_spisok_student()

  elif choice==4:
    ch4 = int(input('Теория - 1\\ Практика - 2: '))
    ch41 = int(input('Все -1. Или конкретно id:  '))

    if ch4 ==1:
      f.saveThemesTeory(ch41)
    elif ch4==2:
      f.saveThemesPracticy(ch41)
    else:
      print('NO')
      # return 

  elif choice==5:
    print('Будут проврены все столбцы, если даты есть всё правильно')
    ch5 = int(input('Теория - 1\\ Практика - 2: '))
    f.examinationRows(ch5)



  elif choice==6:
    ch6 = int(input('Теория - 1\\ Практика - 2: '))
    ch61 = int(input('Все -1. Или конкретно id:  '))

    if ch6 == 1:
      f.closeTheory(ch61)
    elif ch6 == 2:
      f.closePractic(ch61)
    else:
      print('Попробуй ещё')
      

  elif choice==7:
    ch7 = int(input('Теория - 1\\ Практика - 2: '))
    ch71 = int(input('Все -1. Или конкретно id:  '))

    if ch7 == 1:
      f.openTheory(ch71)
    elif ch7 == 2:
      f.openPractic(ch71)
    else:
      print('Попробуй ещё')

  else:
    print('Такого выбора нет')


