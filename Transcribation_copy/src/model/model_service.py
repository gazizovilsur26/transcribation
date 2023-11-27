import whisper_timestamped as whisper
import json
import os
from pathlib import Path
from model.pipeline.model import load_model
import pickle as pk
from config.config import settings
from loguru import logger
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import multiprocessing
# from pathos.multiprocessing import ProcessingPool as Pool

class LoadModel:
    def __init__(self, model_name=settings.model_name):
        self.model_name = model_name
        self.model = None
        self.rec = None
    
    def load_model(self):
        logger.info('Model selection...')
        if settings.model_name == 'vosk-model-ru-0.22':
            logger.info(f'Selected model for transcribation: {settings.model_name}')
            self.model = Model(f"{settings.model_path}/{settings.model_name}")
            self.rec = KaldiRecognizer(self.model, 16000)
            SetLogLevel(0)
        else:
            logger.info(f'Selected model for transcribation: {settings.model_name}')
            logger.info(f'checking the existance of model config file at {settings.model_path}/{settings.model_name}')
            model_path = Path(f'{settings.model_path}/{settings.model_name}')
            if not model_path.exists():
                logger.warning(f'model at {settings.model_path}/{settings.model_name} was not found --> building {settings.model_name}')
                load_model()
            logger.info(f'model {settings.model_name} exists! --> loading model configuration file')
            self.model = pk.load(open(f'{settings.model_path}/{settings.model_name}', 'rb'))
            



class Transcribation:
    def __init__(self, model_name=settings.model_name):
        # self.model_name = model_name
        self.input_path = settings.output_path
        # self.model = None
        # self.rec = None
    
    # def load_model(self):
    #     if self.model_name == 'vosk-model-ru-0.22':
    #         self.model = Model('model/models/vosk-model-ru-0.22')
    #         self.rec = KaldiRecognizer(self.model, 16000)
    #         SetLogLevel(0)

    #     else:
    #         self.model = pk.load(open(f'{settings.model_path}/{settings.model_name}', 'rb'))


    
    
  

    def transcribe_whisper(self, wav_file, output_dir, model):
        # model = pk.load(open(f'{settings.model_path}/{settings.model_name}', 'rb'))
        if wav_file.endswith('.wav'):
            wav_path = os.path.join(self.input_path, wav_file)
            audio = whisper.load_audio(wav_path)
            result = whisper.transcribe(model, audio, language="ru")
            json_string = json.dumps(result, indent=2, ensure_ascii=False)
            json_filename = os.path.splitext(wav_file)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)
            with open(json_path, mode="w",encoding="utf-8") as file:
                file.write(json_string)

    def transcribe_vosk(self, wav_file, output_dir, model):
        if wav_file.endswith(".wav"):
            wav_path = os.path.join(self.input_path, wav_file)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # model = Model("model/models/vosk-model-ru-0.22")
            # SetLogLevel(0)

            wf = wave.open(wav_path, "rb")
            # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            #     exit(1)

            # rec = KaldiRecognizer(self.model, wf.getframerate())
            
            model.SetWords(True)
            model.Reset()

            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if model.AcceptWaveform(data):
                    result = json.loads(model.Result())
                    results.append(result)

            final_result = json.loads(model.FinalResult())
            results.append(final_result)

            transformed_data = {
                "segments": []
            }
            for i in range(len(results)):
                try:
                    new_dict = {
                        "text": results[i]['text'],
                        "start": results[i]['result'][0]['start'],
                        "end": results[i]['result'][-1]['end'],
                        "words": results[i]['result'][-1]['end']
                    }
                    transformed_data["segments"].append(new_dict)
                except:
                    pass

            json_string = json.dumps(transformed_data, indent=2, ensure_ascii=False)
            json_filename = os.path.splitext(wav_file)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)

            with open(json_path, 'w', encoding='utf-8') as file:
                file.write(json_string)

    def transcribe(self, wav_file, model):

        output_dir = settings.output_dir
        if settings.model_name == 'whisper_timestamped_large':
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            self.transcribe_whisper(wav_file, output_dir, model)
            


        if settings.model_name == 'vosk-model-ru-0.22':
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            self.transcribe_vosk(wav_file, output_dir, model)




        
    def combine_dialog(self, manager_json, client_json):
        
        # Загрузка данных
        with open(f'{settings.output_dir }/{manager_json}', 'r', encoding='utf-8') as manager_file:
            manager_data = json.load(manager_file)

        with open(f'{settings.output_dir}/{client_json}', 'r', encoding='utf-8') as client_file:
            client_data = json.load(client_file)


        combined_dialog = [] # здесь собираем диалог
        manager_segments = manager_data["segments"]
        client_segments = client_data["segments"]
        current_speaker = "Сотрудник" if manager_segments[0]["start"] < client_segments[0]["start"] else "Клиент"

        manager_index, client_index = 0, 0 # счётчик для индекса сегмента 

        while (manager_index < len(manager_segments)) and (client_index < len(client_segments)):
            manager_segment = manager_segments[manager_index]
            client_segment = client_segments[client_index]

            # manager_words = manager_segment["words"]
            # client_words = client_segment["words"]
            manager_words = manager_segment["text"]
            client_words = client_segment["text"]

            if current_speaker == "Сотрудник": # можно вместо сотруднк/клиент использовать абонент1,2
                # combined_dialog.append({"Сотрудник": ' '.join([word["text"] for word in manager_words])})
                combined_dialog.append({"Сотрудник": manager_words})
                manager_index += 1
            else:
                # combined_dialog.append({"Клиент": ' '.join([word["text"] for word in client_words])})
                combined_dialog.append({"Клиент": client_words})
                client_index += 1

            # Проверка того, кто следующий говорит. Сравниваем по времени
            if manager_index < len(manager_segments) and client_index < len(client_segments):
                if manager_segments[manager_index]["start"] < client_segments[client_index]["start"]:
                    current_speaker = "Сотрудник"
                else:
                    current_speaker = "Клиент"

        # если ещё оставлись сегменты
        while manager_index < len(manager_segments):
            manager_segment = manager_segments[manager_index]
            # combined_dialog.append({"Сотрудник": ' '.join([word["text"] for word in manager_segment["words"]])})
            combined_dialog.append({"Сотрудник": manager_segment["text"]})
            manager_index += 1

        while client_index < len(client_segments):
            client_segment = client_segments[client_index]
            # combined_dialog.append({"Клиент": ' '.join([word["text"] for word in client_segment["words"]])})
            combined_dialog.append({"Клиент": client_segment["text"]})
            client_index += 1

        # Соханение в джейсонку
        with open(f'{settings.combined_dialogs_path}/combined_{manager_json}', 'w', encoding='utf-8') as combined_file:
            json.dump(combined_dialog, combined_file, ensure_ascii=False, indent=2)