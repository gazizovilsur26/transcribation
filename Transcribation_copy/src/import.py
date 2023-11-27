from config.config import settings
from model.model_service import Transcribation
import os
from model.pipeline.preprocessing_audio import AudioProcessor, split_audio_all
from loguru import logger
import warnings
warnings.filterwarnings("ignore")
from multiprocessing import Pool, Process
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json

# def main():
#     logger.info('running the application...')
#     print('Начинаем')
#     audio_processor = AudioProcessor()
#     print('Разделение на каналы')
#     split_audio_all(audio_processor = audio_processor)
#     transcribation = Transcribation()
#     print('Загрузка модели')
#     model1 = Model('model/models/vosk-model-ru-0.22')
#     rec1 = KaldiRecognizer(model1, 16000)
#     SetLogLevel(0)
#     print('Транскрибация')
#     wav_list = [wav_file for wav_file in os.listdir(settings.output_path)]
#     for wav_file in wav_list:
#         transcribation.transcribe(wav_file, rec1)
#     # print('Схлопывание')
#     # folder_path = settings.output_dir
#     logger.info('start combining left channel text with right channel text')
#     # for filename in os.listdir(folder_path):
#     #     if filename.endswith("_left.json"):
#     #         left_filename = filename
#     #         right_filename = filename.replace("_left.json", "_right.json")
            


#     #         transcribation.combine_dialog(left_filename, right_filename)
#     # print('Конец')


# if __name__ == '__main__':
#     main()    
# data_folder = 'data/splitted'
# import os
# files = os.listdir(data_folder)
# file_names = [file for file in files if file.endswith('.wav')]
# print(file_names)

audio_processor = AudioProcessor()
print('Разделение на каналы')
split_audio_all(audio_processor = audio_processor)