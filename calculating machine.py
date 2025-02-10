import tkinter as tk

# 버튼 클릭 이벤트 핸들러
def on_button_click(value):
    if value == "=":
        try:
            result = str(eval(entry_var.get()))
            entry_var.set(result)
        except Exception:
            entry_var.set("Error")
    elif value == "C":
        entry_var.set("")
    else:
        entry_var.set(entry_var.get() + value)

# 메인 윈도우 설정
root = tk.Tk()
root.title("계산기")
root.geometry("300x400")

# 입력 필드
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 20), justify="right", bd=10, relief="ridge")
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8, sticky="nsew")

# 버튼 구성
buttons = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("C", "0", "=", "+")
]

# 버튼 생성
for i, row in enumerate(buttons, start=1):
    for j, btn_text in enumerate(row):
        btn = tk.Button(root, text=btn_text, font=("Arial", 18), width=5, height=2,
                        command=lambda value=btn_text: on_button_click(value))
        btn.grid(row=i, column=j, sticky="nsew")

# 행/열 크기 조정 (자동 확장)
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

# 실행 루프
root.mainloop()
