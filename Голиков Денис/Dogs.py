from  tkinter import *
from  tkinter import messagebox as mb
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO

from bottle import response


def get_dog_image():
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        # Узнаем статус запроса
        response.raise_for_status()
        # Переменную data кладем ответ в формате json
        data = response.json()
        # возвращаем информацию о строке с картинкой
        return data["message"]
    except Exception as e:
        mb.showerror("Ошибка", f"Возникла ошибка {e} при запросе к API ")
        return None


def show_image():
    # Получаем ссылку на изображение с помощью другой функции
        image_url = get_dog_image()
        if image_url:
            try:
                # ответ = запросу получаем из интернета что-то по ссылке
                response = requests.get(image_url, stream = True)
                # Получаем статус ответа
                response.raise_for_status()
                #Загружаем в img_data с помощью BytesIO
                img_data = BytesIO(response.content)
                # Обрабатываем с помощью pillow
                img = Image.open(img_data)
                #Зададим размер картинок, чтобы они подгонялись под размер
                img.thumbnail((300, 300))
                img = ImageTk.PhotoImage(img)
                #Загружаем её на метку
                label.config(image=img)
                label.image = img
            except Exception as e:
                mb.showerror("Ошибка", f"Возникла ошибка {e} при загрузке изображения")
        progress.stop()

def progr():
    progress["value"] = 0
    progress.start(30)
    window.after(3000, show_image)
window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

label = ttk.Label()
label.pack(pady = 10)

button = ttk.Button(text = "Загрузить изображение", command=progr)
button.pack(pady=10)
progress = ttk.Progressbar(mode = "determinate", length=300)
progress.pack(pady = 10)

window.mainloop()
