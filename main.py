import csv
from pprint import pprint
import re

with open("adressbook.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["lastname", "firstname", "surname", "organization", "position", "phone", "email"])

    file_writer.writerow(["Дядюля", "Екатерина", "Андреевна", "ФНС", "Cоветник отдела нормативного и "
                                                                     "методологического обеспечения государственной "
                                                                     "регистрации юридических лиц и индивидуальных "
                                                                     "предпринимателей Управления регистрации и учета "
                                                                     "налогоплательщиков", "+7(495)9130468",
                          "opendata@nalog.ru"])

    file_writer.writerow(["Блитман", "Александр", "Михайлович", "ФНС", "Заместитель отдела методологии взаимодействия "
                                                                       "с налогоплательщиками по телекоммуникационным "
                                                                       "каналам связи Управления электронного "
                                                                       "документооборота из компании ФНС России",
                          "8(495)9130000 ", "mns10650@nalog.ru"])

    file_writer.writerow(["Коцарёва", "Полина", "Андреевна", "ФНС", "референт Административного департамента",
                          "+7(495)9833699 ", "Polina.Kotcareva", "@minfin.ru"])

with open("adressbook.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # pprint(contacts_list)


def name_normalization(rows):
    result = [' '.join(employee[0:3]).split(' ')[0:3] + employee[3:7] for employee in rows]
    return result


def remove_duplicates(updated_name_list):
    no_duplicates = []
    for compared in updated_name_list:
        for employee in updated_name_list:
            if compared[0:2] == employee[0:2]:
                list_employee = compared
                compared = list_employee[0:2]
                for i in range(2, 7):
                    if list_employee[i] == '':
                        compared.append(employee[i])
                    else:
                        compared.append(list_employee[i])
        if compared not in no_duplicates:
            no_duplicates.append(compared)
    return no_duplicates


def updating_phone_numbers(rows, regular, new):
    adressbook = []
    pattern = re.compile(regular)
    phonebook = [[pattern.sub(new, string) for string in strings] for strings in rows]
    return phonebook


updated_name_list = name_normalization(contacts_list)
no_duplicates_list = remove_duplicates(updated_name_list)
regular = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
correct_list = updating_phone_numbers(no_duplicates_list, regular, r'+7(\2)\3-\4-\5')
regular_2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*'
updated_adressbook = updating_phone_numbers(correct_list, regular_2, r'+7(\2)\3-\4-\5 доб.\6')

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(updated_adressbook)
