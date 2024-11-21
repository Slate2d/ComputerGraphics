from PIL import Image

# Открываем изображение
image = Image.open('pop.png')

# Преобразуем изображение в режим RGB
image = image.convert('RGB')

# Получаем список всех цветов изображения
colors = image.getcolors(maxcolors=256**3)

# Вычисляем количество уникальных цветов
unique_colors = len(colors)

print(f"Количество уникальных цветов в изображении: {unique_colors}")
