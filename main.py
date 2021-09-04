from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Progressbar, Style, Combobox
from tkinter import messagebox
import bitarray


def open_file():
    print("Загрузка из файла")
    filename = askopenfilename()
    if filename == "":
        return 0
    # Пытаемся открыть файл
    try:
        file = open(filename, "rb")
        inputText = file.read()
        file.close()
    except Exception as error:
        messagebox.showinfo('Ошибка при открытии файла', 'Не удалось открыть файл')
        return 0
    inputText = inputText.decode('ANSI')
    txt.delete(1.0, END)
    txt.insert(INSERT, inputText)
    print("Файл открыт")



def save_file():
    print("\nВыгрузка в файл\n")
    txt_original = txt2.get("1.0", 'end-1c')
    txt_2 = txt2.get(1.0, END)
    print("вывод: ", txt_original)
    print("число символов дял выгрузки", len(txt_original))
    filename = asksaveasfilename()
    result = txt_original.encode('ANSI')

    try:
        file = open(filename, "wb")
        file.write(result)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0


def bin_to_4(letter):
    while len(letter)<4:
        letter='0'+letter
    return letter


def bin_to_8(letter):
    a=bin(letter)[2:]
    while len(a)<8:
        a='0'+a
    return a

def bin_to_16(letter):
    a=bin(letter)[2:]
    while len(a)<16:
        a='0'+a
    return a

def bin_to_32(letter):
    a=bin(ord(letter))[2:]
    while len(a)<32:
        a='0'+a
    return a



def open_txt_key():
    txt_key.delete(1.0, END)
    filename = askopenfilename()
    print(filename)
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            txt_key.insert(INSERT, line)




def open_txt_posilka():
    txt_posilka.delete(1.0, END)
    filename = askopenfilename()
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            txt_posilka.insert(INSERT, line)

def save_file_key():
    print("\nВыгрузка в файл\n")
    txt_original = txt_key.get("1.0", 'end-1c')
    filename = asksaveasfilename()
    #result = txt_original.encode('ANSI')

    try:
        file = open(filename, "w", encoding='utf-8')
        file.write(txt_original)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0

def save_file_posilka():
    print("\nВыгрузка в файл\n")
    txt_original = txt_posilka.get("1.0", 'end-1c')
    filename = asksaveasfilename()
    # result = txt_original.encode('ANSI')

    try:
        file = open(filename, "w", encoding='utf-8')
        file.write(txt_original)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0


def sum_2_32(input_byte_string, key):
    a=int(input_byte_string,2)
    modul=int(0xFFFFFFFF) + 1
    b=int(key,2)

    result=(a+b)%modul
    result=bin(result)[2:]
    while len(result)<32:
        result = '0' + result
    return result


def GOST(L,R,session_key,s_block_table):
    for shifr_round in range(32):
        R_old = R
        # формируем раундовый ключ для каждой итерации
        key_for_current_round = ''
        for i in range(4):
            key_for_current_round += bin_to_8(session_key[shifr_round * 4 + i])

        # производим суммирование по модулю 2 в 32 степени
        after_sum_32 = sum_2_32(R, key_for_current_round)

        # произведем замены, в соответствии с таблицей замен

        after_zamena = ''
        for i in range(8):
            nujno_zamenit = after_sum_32[i * 4:i * 4 + 4]
            after_zamena += bin_to_4(bin(s_block_table[8 - i - 1][int(nujno_zamenit, 2)])[2:])

        # произведем циклический сдвиг влево
        sdvig_answer = after_zamena[11:32] + after_zamena[:11]

        # произведем операцию XOR
        total_answer = bin(int(L, 2) ^ int(sdvig_answer, 2))[2:]
        while len(total_answer) < 32:
            total_answer = '0' + total_answer

        if shifr_round < 31:
            R = total_answer
            L = R_old


        else:
            L = total_answer
            R = R_old
    result = L + R

    return result

def clicked():
    s_block_table = [[4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
                     [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
                     [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
                     [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
                     [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
                     [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
                     [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
                     [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]]
    if combo.get() == 'Зашифровать':
        added_symbols=0
        txt_original = txt.get("1.0", 'end-1c')
        while len(txt_original) % 8 != 0:
            txt_original += 'a'
            added_symbols+=1
        session_key_default = txt_key.get("1.0", 'end-1c')
        #session_key_default = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        i=0
        while len(session_key_default)<32:
            session_key_default+=session_key_default[i%len(session_key_default)]
            i += 1
        txt_key.delete(1.0, END)
        txt_key.insert(INSERT,str(added_symbols)+session_key_default)
        session_key = ''
        for i in range(128):
            session_key += session_key_default[i % len(session_key_default)]

        session_key_srez1 = session_key[:96]
        session_key_srez2 = session_key[96:]
        session_key_inverted = ''
        for i in range(32 // 4 + 1):
            temp = session_key_srez2[len(session_key_srez2) - i * 4:len(session_key_srez2) - i * 4 + 4]
            session_key_inverted += temp
        session_key = session_key_srez1 + session_key_inverted
        print(session_key)


        session_key = session_key.encode('ANSI')
        total_code_result=''
        txt_original = txt_original.encode("ANSI")

        s.configure("LabeledProgressbar", text="Шифрование простой заменой", foreground='black',
                    background='mediumseagreen')
        Progres_bar.configure(value=0)
        Progres_bar.update()
        if combo2.get() == "Режим простой замены":

            for part in range(0,len(txt_original)//8):
                L = bin_to_8(txt_original[part * 8]) + bin_to_8(txt_original[part * 8 + 1]) + bin_to_8(
                    txt_original[part * 8 + 2]) + bin_to_8(txt_original[part * 8 + 3])
                R = bin_to_8(txt_original[part * 8 + 4]) + bin_to_8(txt_original[part * 8 + 5]) + bin_to_8(
                    txt_original[part * 8 + 6]) + bin_to_8(txt_original[part * 8 + 7])
                result = GOST(L,R,session_key,s_block_table)
                for i in range(8):
                    bit_tmp = bitarray.bitarray(result[8*i : 8*i+8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result+=coding_result.decode('ANSI')

                progress_check=(part/(len(txt_original)//8))*100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()
            txt2.insert(INSERT,total_code_result)

            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()

        if combo2.get() == "Гаммирование с обратной связью":
            syncro = txt_posilka.get("1.0", 'end-1c')
            i = 0
            while len(syncro) < 8:
                syncro += syncro[i % 64]
                i += 1

            syncro=syncro.encode('ANSI')
            L = bin_to_8(syncro[0]) + bin_to_8(syncro[1]) + bin_to_8(syncro[2]) + bin_to_8(syncro[3])
            R = bin_to_8(syncro[4]) + bin_to_8(syncro[5]) + bin_to_8(syncro[6]) + bin_to_8(syncro[7])

            result=GOST(L,R,session_key,s_block_table)

            T = bin_to_8(txt_original[0]) + bin_to_8(txt_original[1]) + bin_to_8(txt_original[2]) + bin_to_8(
                txt_original[3]) + bin_to_8(txt_original[4]) + bin_to_8(txt_original[5]) + bin_to_8(
                txt_original[6]) + bin_to_8(txt_original[7])

            # произведем операцию XOR
            total_answer = bin(int(result, 2) ^ int(T, 2))[2:]
            while len(total_answer) < 64:
                total_answer = '0' + total_answer
            for i in range(8):
                bit_tmp = bitarray.bitarray(total_answer[8 * i: 8 * i + 8])
                coding_result = bit_tmp.tobytes()
                total_code_result += coding_result.decode('ANSI')

            for i in range(1,len(txt_original)//8):
                L = total_answer[:32]
                R = total_answer[32:]

                result=GOST(L,R,session_key,s_block_table)

                T = bin_to_8(txt_original[i * 8]) + bin_to_8(txt_original[i * 8 + 1]) + bin_to_8(
                    txt_original[i * 8 + 2]) + bin_to_8(
                    txt_original[i * 8 + 3]) + bin_to_8(txt_original[i * 8 + 4]) + bin_to_8(
                    txt_original[i * 8 + 5]) + bin_to_8(
                    txt_original[i * 8 + 6]) + bin_to_8(txt_original[i * 8 + 7])

                total_answer=bin(int(result, 2) ^ int(T, 2))[2:]
                while len(total_answer) < 64:
                    total_answer = '0' + total_answer

                for o in range(8):
                    bit_tmp = bitarray.bitarray(total_answer[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                progress_check = (i / (len(txt_original) // 8)) * 100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()



            txt2.insert(INSERT, total_code_result)
            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()








    elif combo.get()=="Расшифровать":
        txt2.delete(1.0, END)
        txt_original = txt.get("1.0", 'end-1c')
        txt_original = txt_original.encode("ANSI")
        total_code_result = ''

        s.configure("LabeledProgressbar", text="Шифрование простой заменой", foreground='black',
                    background='mediumseagreen')
        Progres_bar.configure(value=0)
        Progres_bar.update()

        if combo2.get()=="Режим простой замены":
            input_key = txt_key.get("1.0", 'end-1c')
            added_symbols = int(input_key[0])
            session_key_default = input_key[1:]
            i = 0
            while len(session_key_default) < 32:
                session_key_default += session_key_default[i % len(session_key_default)]
                i+=1
            session_key = ''
            for i in range(128):
                session_key += session_key_default[i % len(session_key_default)]

            session_key_srez1 = session_key[:32]
            session_key_srez2 = session_key[32:]
            session_key_inverted = ''
            for i in range(96 // 4 + 1):
                temp = session_key_srez2[len(session_key_srez2) - i * 4:len(session_key_srez2) - i * 4 + 4]
                session_key_inverted += temp
            session_key = session_key_srez1 + session_key_inverted
            session_key = session_key.encode('ANSI')





            for part in range(0, len(txt_original) // 8):
                L = bin_to_8(txt_original[part * 8]) + bin_to_8(txt_original[part * 8 + 1]) + bin_to_8(
                    txt_original[part * 8 + 2]) + bin_to_8(txt_original[part * 8 + 3])
                R = bin_to_8(txt_original[part * 8 + 4]) + bin_to_8(txt_original[part * 8 + 5]) + bin_to_8(
                    txt_original[part * 8 + 6]) + bin_to_8(txt_original[part * 8 + 7])

                result = GOST(L, R, session_key, s_block_table)

                for i in range(8):
                    bit_tmp = bitarray.bitarray(result[8 * i: 8 * i + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                progress_check = (part / (len(txt_original) // 8)) * 100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()
            txt2.insert(INSERT, total_code_result[:len(total_code_result)-added_symbols])
            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()

        if combo2.get() == "Гаммирование с обратной связью":
            input_key = txt_key.get("1.0", 'end-1c')
            added_symbols = int(input_key[0])
            session_key_default = input_key[1:]
            i=0
            while len(session_key_default)<32:
                session_key_default+=session_key_default[i%len(session_key_default)]
                i += 1
            session_key = ''
            for i in range(128):
                session_key += session_key_default[i % len(session_key_default)]

            session_key_srez1 = session_key[:96]
            session_key_srez2 = session_key[96:]
            session_key_inverted = ''
            for i in range(32 // 4 + 1):
                temp = session_key_srez2[len(session_key_srez2) - i * 4:len(session_key_srez2) - i * 4 + 4]
                session_key_inverted += temp
            session_key = session_key_srez1 + session_key_inverted
            print(session_key)
            session_key = session_key.encode('ANSI')


            syncro = txt_posilka.get("1.0", 'end-1c')
            i = 0
            while len(syncro) < 8:
                syncro += syncro[i % 64]
                i += 1
            syncro = syncro.encode('ANSI')


            L = bin_to_8(syncro[0]) + bin_to_8(syncro[1]) + bin_to_8(syncro[2]) + bin_to_8(syncro[3])
            R = bin_to_8(syncro[4]) + bin_to_8(syncro[5]) + bin_to_8(syncro[6]) + bin_to_8(syncro[7])

            result = GOST(L, R, session_key, s_block_table)

            T = bin_to_8(txt_original[0]) + bin_to_8(txt_original[1]) + bin_to_8(txt_original[2]) + bin_to_8(
                txt_original[3]) + bin_to_8(txt_original[4]) + bin_to_8(txt_original[5]) + bin_to_8(
                txt_original[6]) + bin_to_8(txt_original[7])

            # произведем операцию XOR
            total_answer = bin(int(result, 2) ^ int(T, 2))[2:]
            while len(total_answer) < 64:
                total_answer = '0' + total_answer
            for i in range(8):
                bit_tmp = bitarray.bitarray(total_answer[8 * i: 8 * i + 8])
                coding_result = bit_tmp.tobytes()
                total_code_result += coding_result.decode('ANSI')



            for i in range(1, len(txt_original) // 8):
                L = bin_to_8(txt_original[(i-1) * 8]) + bin_to_8(txt_original[(i-1) * 8 + 1]) + bin_to_8(
                    txt_original[(i-1) * 8 + 2]) + bin_to_8(
                    txt_original[(i-1) * 8 + 3])
                R = bin_to_8(txt_original[(i-1) * 8 + 4]) + bin_to_8(
                    txt_original[(i-1) * 8 + 5]) + bin_to_8(
                    txt_original[(i-1) * 8 + 6]) + bin_to_8(txt_original[(i-1) * 8 + 7])

                result = GOST(L, R, session_key, s_block_table)

                T = bin_to_8(txt_original[i * 8]) + bin_to_8(txt_original[i * 8 + 1]) + bin_to_8(
                    txt_original[i * 8 + 2]) + bin_to_8(
                    txt_original[i * 8 + 3]) + bin_to_8(txt_original[i * 8 + 4]) + bin_to_8(
                    txt_original[i * 8 + 5]) + bin_to_8(
                    txt_original[i * 8 + 6]) + bin_to_8(txt_original[i * 8 + 7])

                total_answer = bin(int(result, 2) ^ int(T, 2))[2:]
                while len(total_answer) < 64:
                    total_answer = '0' + total_answer

                for o in range(8):
                    bit_tmp = bitarray.bitarray(total_answer[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                progress_check = (i / (len(txt_original) // 8)) * 100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()

            txt2.insert(INSERT, total_code_result[:len(total_code_result)-added_symbols])
            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()







window = Tk()
window.title("ГОСТ")
window.geometry('1550x700')


lbl = Label(window, text="Ваше сообщение")
lbl.place(x=20,y=50)

txt=scrolledtext.ScrolledText(window, width=50, height=30)
txt.place(x=20, y=70)

lbl = Label(window, text="Расшифрованное сообщение:")
lbl.place(x=1100,y=50)

txt2=scrolledtext.ScrolledText(window, width=50, height=30)
txt2.place(x=1100, y=70)


lbl = Label(window, text="Ключ:")
lbl.place(x=500,y=230)
txt_key=scrolledtext.ScrolledText(window, width=50, height=5)
txt_key.place(x=500, y=250)


lbl = Label(window, text="Синхропосылка:")
lbl.place(x=500,y=350)
txt_posilka=scrolledtext.ScrolledText(window, width=50, height=5)
txt_posilka.place(x=500, y=370)

btn = Button(window, text="Открыть файл", command=open_file)
btn.place(x=180,y=565)
lbl = Label(window)

btn = Button(window, text="Сохранить в файл", command=save_file)
btn.place(x=1250,y=565)
lbl = Label(window)


combo = Combobox(window, width=30)
combo['values'] = ("Зашифровать", "Расшифровать")
combo.current(0)
combo.place(x=500, y=150)


combo2 = Combobox(window, width=50)
combo2['values'] = ("Режим простой замены", "Гаммирование с обратной связью")
combo2.current(0)
combo2.place(x=500, y=100)
btn = Button(window, text="Преобразовать", command=clicked)
btn.place(x=750,y=550)
lbl = Label(window)


btn = Button(window, text="Загрузить ключ", command=open_txt_key)
btn.place(x=950,y=250)
lbl = Label(window)

btn = Button(window, text="Сохранить ключ", command=save_file_key)
btn.place(x=950,y=300)
lbl = Label(window)



btn = Button(window, text="Загрузить синхропосылку", command=open_txt_posilka)
btn.place(x=925,y=380)
lbl = Label(window)

btn = Button(window, text="Сохранить синхропосылку", command=save_file_posilka)
btn.place(x=925,y=420)
lbl = Label(window)

s = Style(window)
s.layout("LabeledProgressbar", [('LabeledProgressbar.trough', {'children': [('LabeledProgressbar.pbar', {'side': 'left', 'sticky': 'ns'}), ("LabeledProgressbar.label", {"sticky": ""})], 'sticky': 'nswe'})])

# Сам виджет шкалы прогресса
Progres_bar = Progressbar(window, orient="horizontal", length=100, style="LabeledProgressbar")
Progres_bar.place(relx=0.36, rely=0.92, relwidth=0.281, relheight=0.03)

window.mainloop()