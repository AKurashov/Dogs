from  tkinter import *
from  tkinter import messagebox as mb
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO

from PIL.ImageOps import expand
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
                img_size = (int(width_spinbox.get()),int(height_spinbox.get()))
                #Зададим размер картинок, чтобы они подгонялись под размер
                img.thumbnail(img_size)
                img = ImageTk.PhotoImage(img)
                tab = ttk.Frame(notebook)
                notebook.add(tab, text = f"Картинка №{notebook.index('end')+1}")
                lb=ttk.Label(tab, image=img)
                lb.pack(padx=10,pady=10)
                lb.image = img
            except Exception as e:
                mb.showerror("Ошибка", f"Возникла ошибка {e} при загрузке изображения")
        progress.stop()

def progr():
    progress["value"] = 0
    progress.start(30)
    window.after(3000, show_image)
window = Tk()
window.title("Картинки с собачками")
window.geometry("350x200")

label = ttk.Label()
label.pack(pady = 10)

button = ttk.Button(text = "Загрузить изображение", command=progr)
button.pack(pady=10)
progress = ttk.Progressbar(mode = "determinate", length=300)
progress.pack(pady = 10)

width_level = ttk.Label(text="Ширина:")
width_level.pack(side = "left", padx=(50, 10))
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side = "left", padx=(0, 10))
height_label = ttk.Label(text="Высота")
height_label.pack(side = "left", padx=(0, 10))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side = "left", padx=(0, 10))

top_level_window = Toplevel(window)
top_level_window.title("Изображения собак")

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

window.mainloop()
