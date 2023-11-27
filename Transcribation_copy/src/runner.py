from config.config import settings
from model.model_service import Transcribation
import os
from model.pipeline.preprocessing_audio import AudioProcessor, split_audio_all
from loguru import logger
import warnings
warnings.filterwarnings("ignore")
from multiprocessing import Pool, Process
from vosk import Model, KaldiRecognizer, SetLogLevel
import whisper_timestamped as whisper
import wave
import json
from  concurrent.futures import ProcessPoolExecutor
import pickle as pk
# import dill

def main():
    logger.info('running the application...')
    print('Начинаем')
    audio_processor = AudioProcessor()
    print('Разделение на каналы')
    split_audio_all(audio_processor = audio_processor)
    transcribation = Transcribation()
    print('Загрузка модели')
    transcribation.load_model()
    print('Транскрибация')
    transcribation.transcribe()
    print('Схлопывание')
    folder_path = settings.output_dir
    logger.info('start combining left channel text with right channel text')
    for filename in os.listdir(folder_path):
        if filename.endswith("_left.json"):
            left_filename = filename
            right_filename = filename.replace("_left.json", "_right.json")
            


            transcribation.combine_dialog(left_filename, right_filename)
    print('Конец')

def main():

    logger.info('running the application...')
    print('Начинаем')
    audio_processor = AudioProcessor()
    print('Разделение на каналы')
    split_audio_all(audio_processor = audio_processor)
    transcribation = Transcribation()
    number_of_processes = 2
    # model1 = Model('model/models/vosk-model-ru-0.22')
    # rec1 = KaldiRecognizer(model1, 16000)
    # SetLogLevel(0)
    # model2 = Model('model/models/vosk-model-ru-0.221')
    # rec2 = KaldiRecognizer(model2, 16000)
    # SetLogLevel(0)
    # models = [rec1, rec2]
    model = pk.load(open(f'{settings.model_path}/{settings.model_name}', 'rb'))
    wav_list = [wav_file for wav_file in os.listdir(settings.output_path)]
    wav_list1 = wav_list[0:2]
    wav_list2 = wav_list[2:4]
    wav_list = [wav_list1, wav_list2]
    processes = []
    # p1 = Process(target=transcribation.transcribe, args=(wav_list[0], models[0]))
    # p2 = Process(target=transcribation.transcribe, args=(wav_list[1], models[1]))
    # processes.append(p1)
    # processes.append(p2)
    # p1.start()
    # p2.start()
    # for p in processes:
    #     p.join()
    with ProcessPoolExecutor(max_workers=2) as executor:
        result = executor.submit(transcribation.transcribe, wav_list, model)
        result.result()



if __name__ == '__main__':
    main()


# from config.config import settings
# from model.model_service import Transcribation
# import os
# from model.pipeline.preprocessing_audio import AudioProcessor, split_audio_all
# from loguru import logger
# import warnings
# import whisper_timestamped as whisper
# from multiprocessing import Pool
# import torch
# from vosk import Model, KaldiRecognizer, SetLogLevel

# def process_audio(wav_file):
#     model = model = Model('model/models/vosk-model-ru-0.22')
#     rec = KaldiRecognizer(model, 16000)
#     SetLogLevel(0)
#     transcribation = Transcribation()
#     transcribation.transcribe(wav_file, rec)

# if __name__ == '__main__':
#     logger.info('running the application...')
#     print('Начинаем')
#     audio_processor = AudioProcessor()
#     print('Разделение на каналы')
#     split_audio_all(audio_processor=audio_processor)

#     print('Сохранение модели')
    # model = whisper.load_model('large', device='cpu')
    # with open(f'{settings.model_path}/{settings.model_name}', 'wb') as file:
    #     torch.save(model.state_dict(), file)
    # process_audio(os.listdir(settings.output_path)[0])
    # print('Транскрибация')
    # pool = Pool(processes=2)
    # pool.map(process_audio, [wav_file for wav_file in os.listdir(settings.output_path)])








# print('Модель сохарнена')
# logger.info('running the application...')
# audio_processor = AudioProcessor()
# print('Начинаем деление аудио на каналы')
# split_audio_all(audio_processor=audio_processor)
# transcribation = Transcribation()
# print('Начинаем транскрибацию')

# def transcribe_process(waf_files, model):
#     for waf_file in waf_files:
#         transcribation.transcribe(waf_file, model)

# if __name__ == '__main__':
#     # Загрузка модели из файла
#     with open(f'{settings.model_path}/{settings.model_name}', 'rb') as file:
#         model = torch.load(file)

#     waf_files = os.listdir(settings.output_path)  # список данных звонков для транскрибации
#     num_processes = 2  # Количество процессов для выполнения транскрибации
#     processes = []
#     chunk_size = len(waf_files) // num_processes

#     # Разбиваем файлы для обработки между процессами
#     for i in range(num_processes):
#         start = i * chunk_size
#         end = (i + 1) * chunk_size if i < num_processes - 1 else len(waf_files)
#         process_files = waf_files[start:end]

#         process = Process(target=transcribe_process, args=(process_files, model))
#         processes.append(process)
#         process.start()

#     # Ждем завершения всех процессов
#     for process in processes:
#         process.join()


#--------------------------------------------------------------------
# from config.config import settings
# import os
# from model.pipeline.preprocessing_audio import AudioProcessor, split_audio_all
# from loguru import logger
# import warnings
# warnings.filterwarnings("ignore")
# from multiprocessing import Pool
# import pickle
# from model.model_service import Transcribaзtion

# logger.info('running the application...')
# audio_processor = AudioProcessor()
# print('Начинаем деление аудио на каналы')
# split_audio_all(audio_processor = audio_processor)
# transcribation = Transcribation()
# print('Начинаем транскрибацию')
# if __name__ == '__main__':
#     # Загрузка модели из файла
#     with open(f'{settings.model_path}/{settings.model_name}', 'rb') as file:
#         model = pickle.load(file)

#     # waf_files = [wav_file for wav_file in os.listdir(settings.output_path)]  # список данных звонков для транскрибации
#     with Pool(processes=2) as pool:  # Пример использования пула из 4 процессов
#         args = [(waf_file, model) for waf_file in os.listdir(settings.output_path)]
#         pool.starmap(transcribation.transcribe, args)
#-----------------------------------------------------------------------------------------------
    # transcriptions содержит результаты транскрибации каждого звонка


# # @logger.catch
# def main():
#     logger.info('running the application...')
#     audio_processor = AudioProcessor()
#     split_audio_all(audio_processor = audio_processor)
#     load_model = LoadModel()
#     load_model.load_model()
#     model = load_model.model
#     ml_svc = ModelService(input_path=settings.output_path, model=model)
#     # ml_svc.load_model(model_name=settings.model_name)

#     # ml_svc.transcribe()
#     def pool_handler_4(output_dir = settings.output_dir): # Объект для параллельного транскрибирования
        
#         p = Pool(2) # ЗАДАЙ КОЛ-ВО ЯДЕР!!!!!!!!! 
#         p.map(ml_svc.transcribe_vosk, [(wav_file, output_dir) for wav_file in os.listdir(ml_svc.input_path)])

#     pool_handler_4() 

#     folder_path = settings.output_dir
#     logger.info('start combining left channel text with right channel text')
#     for filename in os.listdir(folder_path):
#         if filename.endswith("_left.json"):
#             left_filename = filename
#             right_filename = filename.replace("_left.json", "_right.json")
            


#             ml_svc.combine_dialog(left_filename, right_filename)

# if __name__ == '__main__':
#     main()