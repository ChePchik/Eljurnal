import spisok_student as s
import re
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


dates_from = os.getenv('DATES_FROM')
dates = os.getenv('DATES')
cookie = os.getenv('COOKIE')
diir = os.getenv('DIIR')

url_tab_rows = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_rows"
url_save = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_save_work_lesson_subject"
url_close = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_close_lesson_action"
url_open = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_open_lesson_action"
url_tab_group = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_group_rows"
# получаем группы
url_tab_subject = "https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_subject_rows"
url_tab_stident = 'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_rows'
name = ''
les_id = 0

spisok = s.spisok
spisok_practicy = s.spisok_practicy

headers = {
    'Host': 'ssuz.vip.edu35.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookie
}

#!#####################################################################################
def payload_predmet_teory( group_id):
	payload = {
		   'unit_id': '22',
        'period_id': '30',
        'date_from': dates_from,
        'date_to': dates,
        'practical': '',
        'slave_mode': '1',
        'group_id': group_id,
	}
	return payload

def payload_predmet_practicy( group_id):
	payload = {
		   'unit_id': '22',
        'period_id': '30',
        'date_from': dates_from,
        'date_to': dates,
        'practical': '1',
        'slave_mode': '1',
        'group_id': group_id,
	}
	return payload


def payload_rows_teory(group_id, subject_id):
    payload = {
        "unit_id": 22,
        "period_id":	30,
        "date_from": dates_from,
        "date_to":	dates,
        "practical":	"",
        "slave_mode":	"1",
        "month":	"",
        "group_id":	group_id,
        "subject":	"0",
        "subject_gen_pr_id":	"0",
        "exam_subject_id":	"0",
        "subject_sub_group_obj":	"{\"subject_id\": "+str(subject_id)+"}",
        "subject_id":	str(subject_id),
        # "view_lessons":	"false"
    }
    return payload


def payload_rows_practicy(dates, group_id, subject_id, sub_group_id):
    payload = {
        "unit_id": 22,
        "period_id":	30,
        "date_from": dates_from,
        "date_to":	dates,
        "practical":	"1",
        "slave_mode":	"1",
        "month":	"",
        "group_id":	group_id,
        "subject":	"0",
        "subject_gen_pr_id":	"0",
        "exam_subject_id":	"0",
        "subject_sub_group_obj": "",
        "subject_id":	subject_id,
        # "view_lessons":	"false"
    }
    if sub_group_id == 0:
        payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+"}"
    else:
        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
            subject_id+", \"sub_group_id\": "+sub_group_id+"}"
    return payload


def payload_rows_practicy_save_tema(les_id, student_id, dates, group_id, subject_id, sub_group_id, name_lessons):
    payload = {
        "lesson_id": les_id,
        "student_id": student_id,
        "unit_id": "22",
        "period_id": "30",
        "date_from": dates_from,
        "date_to": dates,
        "practical": "1",
        "slave_mode": "1",
        "month": "",
        "group_id": group_id,
        "subject": "0",
        "subject_gen_pr_id": "0",
        "exam_subject_id": "0",
        # {\"subject_id\": "+name['subject_id']+"}",
        "subject_sub_group_obj":	"",
        "subject_id": subject_id,
        "view_lessons": "false",
        "lesson_subject": name_lessons
    }
    if sub_group_id == 0:
        payload["subject_sub_group_obj"] = "{\"subject_id\": "+subject_id+"}"
    else:
        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
            subject_id+", \"sub_group_id\": "+sub_group_id+"}"
    return payload


def payload_theory_get_groups():
    # для получения списка групп
    payload = {
        'unit_id': '22',
        'period_id': '30',
        'date_from': dates_from,
        'date_to': dates,
        'practical': '',
        'slave_mode': '1',
    }
    return payload


def payload_practicy_get_groups():
    # для получения списка групп
    payload = {
        'unit_id': '22',
        'period_id': '30',
        'date_from': dates_from,
        'date_to': dates,
        'practical': '1',
        'slave_mode': '1',
    }
    return payload

#!#####################################################################################

def createFile(ch1):
    diirloc = diir
    spisok0 = ''

    if (ch1 == 1):
        diirloc = diirloc+'\\лекции'
        spisok0 = spisok
    elif (ch1 == 2):
        diirloc = diirloc+'\\практика'
        spisok0 = spisok_practicy

    for name in spisok0:
        try:
            with open(diirloc+"\\"+name['group']+'.txt', 'w', encoding="utf-8") as file2:
                print(name['group'])
        except Exception as e:
            print(e)
        finally:
            file2.close()


def dubleFileAll(ch2, ch21):
    diirloc = diir

    if ch2 == 1:
        diirloc = diirloc+'\\лекции'
        if ch21 == -1:
          spisok1 = spisok
        else:
          spisok1 = [spisok[ch21]]

    elif ch2 == 2:
        diirloc = diirloc+'\\практика'
        if ch21 == -1:
          spisok1 = spisok_practicy
        else:
          spisok1 = [spisok_practicy[ch21]]

    else:
        print('Такого действия нет')

    for name in spisok1:
        data_list = []
        with open(diirloc+"\\"+name['group']+'.txt', encoding="utf-8") as file:
            try:
                lines = file.readlines()
                for i in lines:
                    text = i.rstrip()
                    match = re.findall('[1-9]', text)
                    # print(match)
                    match = match[-1] if match else 0
                    for c in range(int(match)):
                        text = text.replace(match, "")
                        data_list.append(text.rstrip())

            except Exception as e:
                print(e)

            finally:
                # print(spisok)
                file.close()

        try:
            with open(diirloc+"\\rasp_"+name['group']+'.txt', 'w', encoding="utf-8") as file2:
                # file2.write("\n".join(spisok).join("\n"));
                for item in data_list:
                    file2.write("%s\n" % item)

        except Exception as e:
            print(e)

        finally:
            # print(name['group'],'Готово')
            file2.close()


def saveThemesPracticy(ch31):
    diirloc = diir

    if ch31 == -1:
        spisok_close = spisok_practicy
    else:
        spisok_close = [spisok_practicy[ch31]]

    for el in spisok_close:
      
        if 'sub_group_id' not in el:

            payload = payload_rows_practicy(
              dates, el["group_id"],
              el["subject_id"],
              0
            )
        else:
            payload = payload_rows_practicy(
            dates, el["group_id"],
            el["subject_id"],
            el["sub_group_id"]
            )

        response = requests.post(url_tab_rows, headers=headers, data=payload)

        data = response.json()
        print(data['rows'][0]['student_name'], el['group'])

        rows = data['rows'][0]['lessons']
        # print(rows)
        # return 0
        with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    if 'sub_group_id' not in el:

                      payload_save = payload_rows_practicy_save_tema(
                          les_id, el['student_id'],
                          dates, el['group_id'],
                          el['subject_id'],
                          0,
                          name_lessons
                      )
                    else:
                      payload_save = payload_rows_practicy_save_tema(
                          les_id, el['student_id'],
                          dates, el['group_id'],
                          el['subject_id'],
                          el["sub_group_id"],
                          name_lessons
                      )

                    # print(payload_save)
                    response = requests.post(
                        url_save, headers=headers, data=payload_save)
                    data = response.json()
                    print(el['group'])
                    print(i, response.status_code, data)

            except Exception as e:
                print(1, e)

            finally:
                file.close()
                print()
            # input()


def saveThemesTeory(ch31):
    diirloc = diir

    if ch31 == -1:
        spisok_close = spisok
    else:
        spisok_close = [spisok[ch31]]

    for name in spisok_close:
        payload_tab_rows = {
            "unit_id": 22,
            "period_id":	30,
            "date_from": dates_from,
            "date_to":	dates,
            "practical":	"",
            "slave_mode":	"",
            "month":	"",
            "group_id":	name['group_id'],
            "subject":	"0",
            "subject_gen_pr_id":	"0",
            "exam_subject_id":	"0",
            "subject_sub_group_obj":	"{\"subject_id\": "+name['subject_id']+"}",
            "subject_id":	name['subject_id'],
            "view_lessons":	"false"
        }
        response = requests.post(
            url_tab_rows, headers=headers, data=payload_tab_rows)
        # подучаем все столбцы
        # так как выдаёт всех студентов со всеми столбцами(попахивает бредом)
        # поэтому мы берём 0 элемент
        data = response.json()
        rows = data['rows'][0]['lessons']

        with open(diirloc+"\\лекции\\rasp_"+name['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    payload_save = {
                        "lesson_id": les_id,
                        "student_id": name['student_id'],
                        "unit_id": "22",
                        "period_id": "30",
                        "date_from": dates_from,
                        "date_to": dates,
                        "practical": "",
                        "slave_mode": "1",
                        "month": "",
                        "group_id": name['group_id'],
                        "subject": "0",
                        "subject_gen_pr_id": "0",
                        "exam_subject_id": "0",
                        "subject_sub_group_obj":	"{\"subject_id\": "+name['subject_id']+"}",
                        "subject_id": name['subject_id'],
                        "view_lessons": "false",
                        "lesson_subject": name_lessons
                    }

                    response = requests.post(
                        url_save, headers=headers, data=payload_save)
                    data = response.json()
                    print(name['group'])
                    print(i, response.status_code, data)

                    # print(lines[i], rows[i]['id'])
                #   text =i.rstrip()
                #   print(text)
            except Exception as e:
                print(e)

            finally:
                file.close()
                print()


def examinationRows(ch4: int):

    if ch4 == 1:
        for el in spisok:
            payload = payload_rows_teory(el["group_id"], el["subject_id"])
            response = requests.post(url_tab_rows, headers=headers, data=payload)

            data = response.json()
            print(data['rows'][0]['student_name'], el['group'])

            rows = data['rows'][0]['lessons']
            for i in rows:
                print(i['id'], i['date'])
            # input()
    else:
        for el in spisok_practicy:
          if 'sub_group_id' not in el:

            payload = payload_rows_practicy(
                dates,
                el["group_id"],
                el["subject_id"],
                0 
            )
          else:
            payload = payload_rows_practicy(
                dates,
                el["group_id"],
                el["subject_id"],
                el["sub_group_id"]
            )


            response = requests.post(
                url_tab_rows, headers=headers, data=payload)

            data = response.json()
            print(data['rows'][0]['student_name'], el['group'])

            rows = data['rows'][0]['lessons']
            for i in rows:
                print(i['id'], i['date'])
            # input()


def closeTheory(ch51: int):
    diirloc = diir

    spisok_close = ""
    if ch51 == -1:
        spisok_close = spisok
    else:
        spisok_close = [spisok[ch51]]

    for el in spisok_close:
        payload = payload_rows_teory(el["group_id"], el["subject_id"])
        response = requests.post(url_tab_rows, headers=headers, data=payload)
        data = response.json()
        rows = data['rows'][0]['lessons']

        with open(diirloc+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    # name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    payload_save = {
                        "lesson_id": les_id,
                        "student_id": el['student_id'],
                        "unit_id": "22",
                        "period_id": "30",
                        "date_from": dates_from,
                        "date_to": dates,
                        "practical": "",
                        "slave_mode": "1",
                        "month": "",
                        "group_id": el['group_id'],
                        "subject": "0",
                        "subject_gen_pr_id": "0",
                        "exam_subject_id": "0",
                        "subject_sub_group_obj":	"{\"subject_id\": "+el['subject_id']+"}",
                        "subject_id": el['subject_id'],
                        # "view_lessons": "false",
                        # "lesson_subject": name_lessons
                    }

                    response = requests.post(
                        url_close, headers=headers, data=payload_save)
                    data = response.json()
                    print(el['group'])
                    print(i, response.status_code, data)

                    # print(lines[i], rows[i]['id'])
                #   text =i.rstrip()
                #   print(text)
            except Exception as e:
                print(e)

            finally:
                file.close()
                print()


def closePractic(ch51: int):
    diirloc = diir

    spisok_close = ""
    if ch51 == -1:
        spisok_close = spisok_practicy
    else:
        spisok_close = [spisok_practicy[ch51]]

    for el in spisok_close:
        if 'sub_group_id' not in el:

          payload = payload_rows_practicy(
              dates, el["group_id"],
              el["subject_id"],
              0
          )
        else:
          payload = payload_rows_practicy(
              dates, el["group_id"],
              el["subject_id"],
              el["sub_group_id"]
          )

        response = requests.post(url_tab_rows, headers=headers, data=payload)

        data = response.json()
        rows = data['rows'][0]['lessons']

        with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    # name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    payload_save = {
                        "lesson_id": les_id,
                        "student_id": el['student_id'],
                        "practical": "1",
                        "unit_id": "22",
                        "period_id": "30",
                        "date_from": dates_from,
                        "date_to": dates,
                        "slave_mode": "1",
                        "month": "",
                        "group_id": el['group_id'],
                        "subject": "0",
                        "subject_gen_pr_id": "0",
                        "exam_subject_id": "0",
                        "subject_sub_group_obj": "",
                        "subject_id": el['subject_id'],
                        "view_lessons": "false",
                        "subperiod": "399",
                        "mark": ""
                    }
                    if 'sub_group_id' not in el:
                    
                        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                            el['subject_id']+"}"
                    else:
                        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                            el['subject_id']+", \"sub_group_id\": " + \
                            el['subject_id']+"}"

                    response = requests.post(
                        url_close, headers=headers, data=payload_save)
                    data = response.json()
                    print(el['group'])
                    print(i, response.status_code, data)

            except Exception as e:
                print(e)

            finally:
                file.close()
            print()


def openTheory(ch61: int):
    diirloc = diir
    spisok_close = ""
    if ch61 == -1:
        spisok_close = spisok
    else:
        spisok_close = [spisok[ch61]]

    for el in spisok_close:
        payload = payload_rows_teory(dates, el["group_id"], el["subject_id"])
        response = requests.post(url_tab_rows, headers=headers, data=payload)
        data = response.json()
        rows = data['rows'][0]['lessons']

        with open(diirloc+"\\лекции\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    # name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    payload_save = {
                        "lesson_id": les_id,
                        "student_id": el['student_id'],
                        "unit_id": "22",
                        "period_id": "30",
                        "date_from": dates_from,
                        "date_to": dates,
                        "practical": "",
                        "slave_mode": "1",
                        "month": "",
                        "group_id": el['group_id'],
                        "subject": "0",
                        "subject_gen_pr_id": "0",
                        "exam_subject_id": "0",
                        "subject_sub_group_obj":	"{\"subject_id\": "+el['subject_id']+"}",
                        "subject_id": el['subject_id'],
                    }

                    response = requests.post(
                        url_open, headers=headers, data=payload_save)
                    data = response.json()
                    print(el['group'])
                    print(i, response.status_code, data)

                    # print(lines[i], rows[i]['id'])
                #   text =i.rstrip()
                #   print(text)
            except Exception as e:
                print(e)

            finally:
                file.close()
                print()


def openPractic(ch61: int):
    diirloc = diir
    spisok_close = ""
    if ch61 == -1:
        spisok_close = spisok_practicy
    else:
        spisok_close = [spisok_practicy[ch61]]

    for el in spisok_close:
        if 'sub_group_id' not in el:
          payload = payload_rows_practicy(
              dates, el["group_id"],
              el["subject_id"],
              0
          )
        else:
          payload = payload_rows_practicy(
              dates, el["group_id"],
              el["subject_id"],
              el["sub_group_id"]
          )

        response = requests.post(url_tab_rows, headers=headers, data=payload)

        data = response.json()
        rows = data['rows'][0]['lessons']

        with open(diirloc+"\\практика\\rasp_"+el['group']+'.txt', encoding="utf-8") as file:
            # считываем строчки из файла
            try:
                lines = file.readlines()
                for i in range(len(lines)):
                    # name_lessons = lines[i]
                    # print(name)
                    les_id = rows[i]['id']
                    # print(les_id,name)
                    payload_save = {
                        "lesson_id": les_id,
                        "student_id": el['student_id'],
                        "practical": "1",
                        "unit_id": "22",
                        "period_id": "30",
                        "date_from": dates_from,
                        "date_to": dates,
                        "slave_mode": "1",
                        "month": "",
                        "group_id": el['group_id'],
                        "subject": "0",
                        "subject_gen_pr_id": "0",
                        "exam_subject_id": "0",
                        "subject_sub_group_obj": "",
                        "subject_id": el['subject_id'],
                        "view_lessons": "false",
                        "subperiod": "399",
                        "mark": ""
                    }
                    if 'sub_group_id' not in el:
                    
                        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                            el['subject_id']+"}"
                    else:
                        payload["subject_sub_group_obj"] = "{\"subject_id\": " + \
                            el['subject_id']+", \"sub_group_id\": " + \
                            el['subject_id']+"}"

                    response = requests.post(
                        url_open, headers=headers, data=payload_save)
                    data = response.json()
                    print(el['group'])
                    print(i, response.status_code, data)

                    # print(lines[i], rows[i]['id'])
                #   text =i.rstrip()
                #   print(text)
            except Exception as e:
                print(e)

            finally:
                file.close()
            print()


def create_spisok_theory(groups):
	result = []
	ids = 0
	predmets = []
	print(groups)
	for g in groups['rows']:
		# print(g)

		payload_preedmet = payload_predmet_teory(g['id'])
		
		response_predmet = requests.post(url_tab_subject, headers=headers, data=payload_preedmet)
		data_premdet = response_predmet.json()
		# print('data_premdet', data_premdet)
		# input()

		for i, el in enumerate(data_premdet['rows']):
			if 'sub_group_id' not in el['id']:
				predmets.append(el)
                # что бы отсечь практические группы

				obj = json.loads(el['id'])['subject_id']
                # obj = json.loads(predmets[w][z]['id'])['subject_id']
                # print(g)
				payload_students = payload_rows_teory(g['id'],str(obj))

				student_response = requests.post(url_tab_stident, headers=headers,data=payload_students)
				student_id = student_response.json()['rows'][0]['student_id']
				# print(g)
				# print(el)
				# input()

				temp_res = {
                    "group": g['name'].split(' - ')[0] +' '+ el['name'],
                    "student_id": str(student_id),
                    "group_id": str(g['id']),
                    "subject_id": str(obj),
                    "id": ids
                }
				ids +=1
				print(temp_res)
				# input('result: ')
				result.append(temp_res)
	return result
# TODO#####################################################
def create_spisok_practicy(groups):
  try:
    result = []
    ids = 0
    predmets = []
    temp_res = []
    # print(groups)
    for gr in groups['rows']:
      match = re.search(r'\в', gr['name'].split(' - ')[0])
      match = match[0] if match else False
      # print(match)
      # print()
      
      # определяем группа платников

      payload_preedmet = payload_predmet_practicy(gr['id'])
      
      response_predmet = requests.post(url_tab_subject, headers=headers, data=payload_preedmet)
      data_premdet = response_predmet.json()
      # print(data_premdet)

      if match=='в':
        # платники
        if data_premdet['total'] == 0:
          print('null платники')
        else:
          for i,pr in enumerate(data_premdet['rows']):
            obj = json.loads(pr['id'])

            if 'sub_group_id' not in obj:

              payload_students = payload_rows_practicy(dates,
                                                        str(gr['id']),
                                                        str(obj["subject_id"]),
                                                        0
                                                        )

              student_response = requests.post(url_tab_stident, headers=headers,data=payload_students)
              student_id = student_response.json()['rows'][0]['student_id']
              print(pr)

              predmet = pr['name'].replace('/','-')
              temp_res = {
                      # "group": gr['name'].split(' - ')[0] +' '+ pr['name'].replace(re.search('\((.*?)\)',pr[0]['name'])[0],'')+i%2,
                      "group": gr['name'].split(' - ')[0] +' '+ predmet,
                      "student_id": str(student_id),
                      "group_id": str(gr['id']),
                      "subject_id": str(obj["subject_id"]),
                      "id": ids
                  }
              ids +=1
              result.append(temp_res)


      else:
        # не платники
        if data_premdet['total'] == 0:
          print('null не платники')
        else:
          for i,pr in enumerate(data_premdet['rows']):
            obj = json.loads(pr['id'])

            if 'sub_group_id' in obj:

              payload_students = payload_rows_practicy(dates,
                                                        str(gr['id']),
                                                        str(obj["subject_id"]),
                                                        str(obj["sub_group_id"]))

              student_response = requests.post(url_tab_stident, headers=headers,data=payload_students)
              student_id = student_response.json()['rows'][0]['student_id']
              print(pr)
              predmet = pr['name'].replace('/','-')
              temp_res = {
                      # "group": gr['name'].split(' - ')[0] +' '+ pr['name'].replace(re.search('\((.*?)\)',pr[0]['name'])[0],'')+i%2,
                      # эх жалко, такое выражение классное
                      "group": gr['name'].split(' - ')[0] +' '+ predmet,
                      "student_id": str(student_id),
                      "group_id": str(gr['id']),
                      "subject_id": str(obj["subject_id"]),
                      'sub_group_id': str(obj["sub_group_id"]),
                      "id": ids
                  }
              ids +=1
              result.append(temp_res)


    return result
  except Exception as e:
    print(e)
  except ValueError as ee:
    print(ee)
  

def create_spisok_student():

	payload_t = payload_theory_get_groups()
	response_t = requests.post(url_tab_group, headers=headers, data=payload_t)
	groups_t = response_t.json()

	payload_p = payload_practicy_get_groups()
	response_p = requests.post(url_tab_group, headers=headers, data=payload_p)
	groups_p = response_p.json()

	spth = create_spisok_theory(groups_t)
	spth2 = create_spisok_practicy(groups_p)

	with open('spisok_student.py', 'w', encoding='utf-8') as file:
		try:

			file.write('spisok = [\n')
			for i in spth:
				file.write('\t')
				file.write(str(i))
				file.write(',\n')
			file.write(']\n\n')

			file.write('spisok_practicy = [\n')
			for i in spth2:
				file.write('\t')
				file.write(str(i))
				file.write(',\n')
			file.write(']\n\n')

		except Exception as e:
			print(e)

		finally:
			file.close()
	print()
