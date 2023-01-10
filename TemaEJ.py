# import re 
# import os
import funcEJ as f
# clear = lambda: os.system('cls')

while True:
  print('-----------------------------------')
  # clear()

  print("что будем делать")

  print("1. Создать файлики")
  print("2. Продублировать темы в файлах")
  print("3. Выставить темы")
  print("4. Проверить столбцы")
  print("5. Закрыть занятие")
  print("6. Открыть занятие")

  choice = int(input(''))
  diir = "D:\\Desktop\\Desktop\\Пары\\2022-2023\\_журнал\\txt"
  # input('Какя директория: ')


  if choice==1:
    ch1 = int(input('Все? - 1\Нет - 0: '))
    # print(diir)
    if(ch1==1):
      f.createFile(diir)
    else:
      print(f.spisok)
      print('пока не сделано')
      # ch2 = int(input('Какой индекс:  '))

  elif choice==2:
    ch2 = int(input('Теория - 1\\ Практика - 2: '))
    ch21 = int(input('Все -1. Или конкретно id:  '))
    print(f.spisok)
    f.dubleFileAll(diir,ch2,ch21)

  elif choice==3:
    ch3 = int(input('Теория - 1\\ Практика - 2: '))
    ch31 = int(input('Все -1. Или конкретно id:  '))

    if ch3 ==1:
      f.saveThemesTeory(diir,ch31)
    elif ch3==2:
      f.saveThemesPracticy(diir,ch31)
    else:
      print('NO')
      # return 

  elif choice==4:
    print('Будут проврены все столбцы, если даты есть всё правильно')
    ch4 = int(input('Теория - 1\\ Практика - 2: '))
    f.examinationRows(ch4)

  elif choice==5:
    ch5 = int(input('Теория - 1\\ Практика - 2: '))
    ch51 = int(input('Все -1. Или конкретно id:  '))

    if ch5 == 1:
      f.closeTheory(diir,ch51)
    elif ch5 == 2:
      f.closePractic(diir,ch51)
    else:
      print('Попробуй ещё')


  elif choice==6:
    ch6 = int(input('Теория - 1\\ Практика - 2: '))
    ch61 = int(input('Все -1. Или конкретно id:  '))

    if ch6 == 1:
      f.openTheory(diir,ch61)
    elif ch6 == 2:
      f.openPractic(diir,ch61)
    else:
      print('Попробуй ещё')



  else:
    print('Такого выбора нет')


