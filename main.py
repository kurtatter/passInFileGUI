import random
import tkinter as tk


window = tk.Tk()
window.resizable(False, False)

all_symbols_for_password = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0}
lower_items = set("abcdefghijklmnopqrstuvwxyz")
all_symbols_for_password |= lower_items
symbols = set("~!@#$%^:;><?&*()-_=+|/?.,")
upper_items = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

ENT_WIDTH = 86
frm_data = tk.Frame(master=window)
lbl_service = tk.Label(text="Сервис:", master=frm_data)
ent_service = tk.Entry(width=ENT_WIDTH, master=frm_data)

lbl_email = tk.Label(text="Email:", master=frm_data)
ent_email = tk.Entry(width=ENT_WIDTH, master=frm_data)
var_login = tk.BooleanVar()


def get_login_state():
    print(var_login.get())
    if var_login.get():
        print("Логин совпадает с почтой")
        ent_login.delete(0, tk.END)
        ent_login.insert(0, ent_email.get())
        ent_login["state"] = "disabled"
        print(ent_login.get())
    elif not var_login.get():
        print("Логин")
        ent_login["state"] = tk.NORMAL


lbl_login = tk.Label(text="Логин", master=frm_data)
ent_login = tk.Entry(width=ENT_WIDTH, master=frm_data)
chb_login = tk.Checkbutton(
    master=frm_data,
    text="Логин совпадает с почтой",
    variable=var_login,
    onvalue=True,
    offvalue=False,
    command=get_login_state,
    takefocus=0
)

lbl_phone = tk.Label(text="Номер телефона:", master=frm_data)
ent_phone = tk.Entry(width=ENT_WIDTH, master=frm_data)
var_phone = tk.IntVar()

NUMBER = None


def get_phone_state():
    print(var_phone.get())
    global NUMBER
    if var_phone.get() == 1:

        print("Телефон не нужен")
        NUMBER = ent_phone.get()
        ent_phone.delete(0, tk.END)
        ent_phone.insert(0, "—")
        ent_phone["state"] = "disabled"
    else:
        print("Телефон нужен")
        ent_phone["state"] = tk.NORMAL
        ent_phone.delete(0, tk.END)
        ent_phone.insert(0, str(NUMBER))


chb_phone = tk.Checkbutton(
    master=frm_data,
    text="Не нужен",
    variable=var_phone,
    onvalue=1,
    offvalue=0,
    command=get_phone_state,
    takefocus=0
)

lbl_password = tk.Label(text="Пароль:", master=frm_data)
ent_password = tk.Entry(width=ENT_WIDTH, master=frm_data)
var_password = tk.IntVar()
frm_generate_password = None
LBL_TITLE = None


def add_btn():
    global frm_generate_password
    global LBL_TITLE
    if var_password.get():
        LBL_TITLE = tk.Label(text="Генератор пароля")
        LBL_TITLE.pack(fill=tk.X)
        frm_generate_password = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=4, width=50)
        frm_generate_password.pack(fill=tk.X)

        var_count_password = tk.IntVar()
        var_count_password.set(8)

        def on_scale(val):
            v = int(float(val))
            var_count_password.set(v)

        lbl_pwd_count = tk.Label(text="Величина пароля:", master=frm_generate_password)
        lbl_pwd_count.grid(row=0, column=0, sticky="es")
        scale = tk.Scale(from_=8, to=128, length=384, command=on_scale, master=frm_generate_password,
                         orient=tk.HORIZONTAL)
        scale.grid(row=0, column=1)
        lbl_word = tk.Label(master=frm_generate_password, text="символов")
        lbl_word.grid(row=0, column=2, sticky="ws")

        var_symbols = tk.IntVar()

        def add_symbols():
            global all_symbols_for_password
            global symbols
            if var_symbols.get():
                all_symbols_for_password |= symbols
            else:
                all_symbols_for_password -= symbols
            print(all_symbols_for_password)

        chb_symbols = tk.Checkbutton(
            master=frm_generate_password,
            text="Символы (!@#$%^&*...)",
            variable=var_symbols,
            onvalue=1,
            offvalue=0,
            command=add_symbols,
            takefocus=0
        )
        chb_symbols.grid(row=1, column=0, pady=8, sticky="e")

        var_upper = tk.IntVar()

        def add_upper():
            global all_symbols_for_password
            global upper_items
            if var_upper.get():
                all_symbols_for_password |= upper_items
            else:
                all_symbols_for_password -= upper_items
            print(all_symbols_for_password)

        chb_upper = tk.Checkbutton(
            master=frm_generate_password,
            text="Буквы верхнего регистра (ABCD ...)",
            variable=var_upper,
            onvalue=1,
            offvalue=0,
            command=add_upper,
            takefocus=0
        )
        chb_upper.grid(row=1, column=1, pady=8, sticky="ew")

        def password_generator():
            global all_symbols_for_password

            psswd_list = list()
            for n in range(var_count_password.get()):
                psswd_list.append(str(random.choice(list(all_symbols_for_password))))
            ent_password.delete(0, tk.END)
            ent_password.insert(0, "".join(psswd_list))

        btn_generate_password = tk.Button(master=frm_generate_password, text="Сгенерировать пароль",
                                          command=password_generator, takefocus=0)
        btn_generate_password.grid(row=1, column=2, pady=8)
    else:
        frm_generate_password.destroy()
        LBL_TITLE.destroy()


chb_password_generate = tk.Checkbutton(
    master=frm_data,
    text="Сгенерировать",
    variable=var_password,
    onvalue=1,
    offvalue=0,
    command=add_btn,
    takefocus=0
)


def append_in_file():
    service = ent_service.get()
    email = ent_email.get()
    login = ent_login.get()
    phone_number = ent_phone.get()
    password = ent_password.get()
    if service and login and password:
        with open("passwords.txt", "a", encoding="utf-8") as file:
            file.flush()
            file.write("-----------------------------\n")
            file.write(f"Сервис: {service}\n")
            file.write(f"Почта: {email}\n")
            file.write(f"Логин: {login}\n")
            file.write(f"Телефон: {phone_number}\n")
            file.write(f"Пароль: {password}\n")
            ent_service.delete(0, tk.END)
            ent_email.delete(0, tk.END)
            ent_login["state"] = tk.NORMAL
            ent_login.delete(0, tk.END)
            ent_phone["state"] = tk.NORMAL
            ent_phone.delete(0, tk.END)
            ent_password.delete(0, tk.END)
            chb_login["variable"] = 0
            chb_phone["variable"] = 0
            chb_password_generate["variable"] = 0
    else:
        ...


btn_append = tk.Button(text="Добавить", pady=12, command=append_in_file)
btn_append.pack(side=tk.BOTTOM, fill=tk.X)
frm_data.pack()
lbl_service.grid(row=0, column=0, sticky="e")
ent_service.grid(row=0, column=1)
ent_service.focus()
lbl_email.grid(row=1, column=0, sticky="e")
ent_email.grid(row=1, column=1)
lbl_login.grid(row=2, column=0, sticky="e")
ent_login.grid(row=2, column=1)
chb_login.grid(row=2, column=2, sticky="w")
lbl_phone.grid(row=3, column=0, sticky="e")
ent_phone.grid(row=3, column=1)
chb_phone.grid(row=3, column=2, sticky="w")
lbl_password.grid(row=4, column=0, sticky="e")
ent_password.grid(row=4, column=1)
chb_password_generate.grid(row=4, column=2, sticky="w")

window.mainloop()
