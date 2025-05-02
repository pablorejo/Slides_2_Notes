import edge_tts
import asyncio
import os
    
def get_data_text(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


async def speak(salida,text):
    communicate = edge_tts.Communicate(text=text, voice="es-ES-ElviraNeural")
    await communicate.save(salida)


def main(file = 'MD\\5G_description\\5G_description_salida_note_final.md',
         audio_folder = 'audio',
         play_song=False):

    data = get_data_text(file)
    
    salida = os.path.join(audio_folder, file.split('\\')[-1].replace('.md', '.mp3'))

    asyncio.run(speak(salida,data))
    
    if speak: os.system(f"start {salida}")

if __name__ == "__main__":
    main(play_song=True)



