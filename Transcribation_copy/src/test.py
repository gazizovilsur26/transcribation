from multiprocessing import Process
from config.config import settings
from vosk import Model, KaldiRecognizer
from model.model_service import Transcribation
import os

# 1. Как создавать классы, которые наследуются от Process?
# 2. Как триггерить такие классы разом все?
# 3. Как передать входные данные в такой класс?

class ModelProcess(Process):
    def __init__(self, files):
        super().__init__()
        self.files = files
        self.m = Model(f'{settings.model_path}/{settings.model_name}')
        self.model = KaldiRecognizer(self.m, 16000)
        self.transcribation = Transcribation()

    def run(self):
        pass
        # data_folder = 'data/splitted'
        # for file_name in self.files:
        #     file_path = os.path.join(data_folder, file_name)
        #     self.transcribation.transcribe(file_path, self.model)

def main():
    NUM_CPU = 2
    data_folder = 'data/splitted'
    files = os.listdir(data_folder)

    # Разделение имен файлов на подгруппы для каждого процесса
    # chunk_size = len(files) // NUM_CPU
    # chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]
    files1 = files[0:4]
    files2 = files[4:8]
    p1 = ModelProcess(files1)
    p2 = ModelProcess(files2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # ml_prc_list = [ModelProcess(chunk) for chunk in chunks]

    # for prc in ml_prc_list:
    #     prc.start()  # Запуск каждого процесса

    # for prc in ml_prc_list:
    #     prc.join()  # Ожидание завершения каждого процесса

if __name__ == '__main__':
    main()

# from joblib import Parallel, delayed
# import os
# from config.config import settings
# from vosk import Model, KaldiRecognizer
# from model.model_service import Transcribation

# def initialize_model_and_transcriber():
#     return Model(f'{settings.model_path}/{settings.model_name}'), Transcribation()

# def transcribe_file(file_path, model, transcribation):
#     recognizer = KaldiRecognizer(model, 16000)
#     transcribation.transcribe(file_path, recognizer)

# def main():
#     model, transcribation = initialize_model_and_transcriber()

#     data_folder = 'data/splitted'
#     files = os.listdir(data_folder)
#     file_names = [file for file in files if file.endswith('.wav')]
#     file_paths = [os.path.join(data_folder, file_name) for file_name in file_names]

#     # Запускаем обработку файлов параллельно
#     Parallel(n_jobs=2)(delayed(transcribe_file)(file_path, model, transcribation) for file_path in file_paths)

# if __name__ == '__main__':
#     main()


# from joblib import Parallel, delayed
# import os
# from config.config import settings
# from vosk import Model, KaldiRecognizer
# from model.model_service import Transcribation

# def transcribe_file(file_path):
#     m = Model(f'{settings.model_path}/{settings.model_name}')
#     model = KaldiRecognizer(m, 16000)
#     transcribation = Transcribation()

#     transcribation.transcribe(file_path, model)

# def main():
#     data_folder = 'data/splitted'
#     files = os.listdir(data_folder)
#     file_names = [file for file in files if file.endswith('.wav')]
#     # file_paths = [os.path.join(data_folder, file_name) for file_name in file_names]

#     # Запускаем обработку файлов параллельно
#     Parallel(n_jobs=2)(delayed(transcribe_file)(file_name) for file_name in file_names)

# if __name__ == '__main__':
#     main()





# class ModelProcess(Process):
#     def __init__(self, files):
#         super().__init__()
#         self.files = files
#         self.m = Model(f'{settings.model_path}/{settings.model_name}')
#         self.model = KaldiRecognizer(self.m, 16000)
#         self.transcribation = Transcribation()

#     def run(self):
#         data_folder = 'data/splitted'
#         for file_name in self.files:
#             file_path = os.path.join(data_folder, file_name)
#             self.transcribation.transcribe(file_path, self.model)

# def main():
#     NUM_CPU = 2
#     data_folder = 'data/splitted'
#     files = os.listdir(data_folder)

#     # Разделение имен файлов на подгруппы для каждого процесса
#     chunk_size = len(files) // NUM_CPU
#     chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

#     ml_prc_list = [ModelProcess(chunk) for chunk in chunks]

#     for prc in ml_prc_list:
#         prc.start()  # Запуск каждого процесса

#     for prc in ml_prc_list:
#         prc.join()  # Ожидание завершения каждого процесса

# if __name__ == '__main__':
#     main()
