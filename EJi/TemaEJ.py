import re 
import funcEJ as f


print("что будем делать")

print("1. Создать файлики")
print("2. Продублировать темы в файлах")
print("3. Выставить темы")
print("4. Проверить столбцы")

choice = int(input(''))
diir = input('Какя директория: ')


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
  ch2 = int(input('Все -1. Или конкретно id:  '))
  print(f.spisok)
  f.dubleFileAll(diir,ch2)

elif choice==3:
  ch3 = int(input('Теория - 1\\ Практика - 2: '))
  if ch3 ==1:
    f.saveThemesTeory(diir)
  elif ch3==2:
    f.saveThemesPracticy(diir)
  else:
    print('NO')
    # return 

elif choice==4:
  print('Будут проврены все столбцы, если даты есть всё правильно')
  ch4 = int(input('Теория - 1\\ Практика - 2: '))
  f.examinationRows(ch4)



else:
  print('Такого выбора нет')


