

SLASH = np.array([
    [0, 0, 0, 0, 1,],
    [0, 0, 0, 1, 0,],
    [0, 0, 0, 1, 0,],
    [0, 0, 1, 0, 0,],
    [0, 1, 0, 0, 0,],
    [0, 1, 0, 0, 0,],
    [1, 0, 0, 0, 0,],])

def slash_find(self, pixels):
        # Поиск слэшей
        slash_arr = np.zeros((SensorCoord.HEIGHT, SensorCoord.WIDTH))      

        # Проход по ширине
        for x in range(self.rect_coord[2] // 2):
            arr = []

            # Проход по высоте
            for y in range(SensorCoord.HEIGHT):
                if pixels[x, y] == (255, 255, 255):
                    arr.append(1)
                else:
                    arr.append(0)

            # Обновление сенсора
            for i in range(SensorCoord.WIDTH - 1):
                slash_arr[:, i] = slash_arr[:, i + 1]
            slash_arr[:, SensorCoord.WIDTH - 1] = np.array(arr)

            # нахождение слэшей
            if np.array_equal(slash_arr, SLASH):
                print(x)