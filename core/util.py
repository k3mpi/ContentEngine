from django.utils.text import slugify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import random
import re
import textwrap

import requests
from googleapiclient.http import MediaFileUpload
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

from PIL import Image, ImageDraw, ImageFont
import io

from django.conf import settings
from django.conf.urls.static import static
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.speedx import speedx

from ContentEngine.settings import MEDIA_ROOT, BASE_DIR
from core.models import IGPost, IGSlide, Video, BackgroundVideo, Music, BackgroundImage, Hashtag
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def extract_audio_skript(xml_string):

    skript_pattern = r"<skript>(.*?)</skript>"

    # Suchen des Topics
    skript_match = re.search(skript_pattern, xml_string)
    skript = skript_match.group(1) if skript_match else None


    return skript
def extract_topic_and_reasons(xml_string):
    # Regex-Muster zum Finden des Topics und der Gründe
    topic_pattern = r"<topic>(.*?)</topic>"
    reason_pattern = r"<reason_\d+>(.*?)</reason_\d+>"
    description_pattern = r"<description_\d+>(.*?)</description_\d+>"

    # Suchen des Topics
    topic_match = re.search(topic_pattern, xml_string)
    topic = topic_match.group(1) if topic_match else None

    # Suchen aller Gründe
    reasons = re.findall(reason_pattern, xml_string)
    descriptions = re.findall(description_pattern, xml_string)

    return topic, reasons, descriptions
def extract_ideas(xml_string):
    # Regex-Muster zum Finden des Topics und der Gründe
    idea_pattern = r"<idee>(.*?)</idee>"

    # Suchen aller Gründe
    ideas = re.findall(idea_pattern, xml_string)

    return ideas

def extract_article(xml_string):
    # Regex-Muster zum Finden des Topics und der Gründe

    title_pattern = r"<title>(.*?)</title>"
    intro_pattern = r"<intro>(.*?)</intro>"
    subtitle_pattern = r"<subtitle>(.*?)</subtitle>"
    text_pattern = r"<text>(.*?)</text>"
    cta_title_pattern = r"<cta_title>(.*?)</cta_title>"
    cta_text_pattern = r"<cta_text>(.*?)</cta_text>"

    title_match = re.search(title_pattern, xml_string)
    title = title_match.group(1) if title_match else None
    intro_match = re.search(intro_pattern, xml_string)
    intro = intro_match.group(1) if intro_match else None
    subtitles = re.findall(subtitle_pattern, xml_string)
    texts = re.findall(text_pattern, xml_string)
    cta_title_match = re.search(cta_title_pattern, xml_string)
    cta_title = cta_title_match.group(1) if cta_title_match else None
    cta_text_match = re.search(cta_text_pattern, xml_string)
    cta_text = cta_text_match.group(1) if cta_text_match else None

    return title,intro,subtitles,texts,cta_title,cta_text
def extract_hashtags(xml_string):
    # Regex-Muster zum Finden des Topics und der Gründe
    hashtag_pattern = r"<hashtag>(.*?)</hashtag>"
    keyword_pattern = r"<keyword>(.*?)</keyword>"
    meta_pattern = r"<meta>(.*?)</meta>"

    # Suchen aller Gründe
    hashtags = re.findall(hashtag_pattern, xml_string)


    # Suchen des Topics
    meta_match = re.search(meta_pattern, xml_string)
    meta = meta_match.group(1) if meta_match else None

    # Suchen aller Gründe
    keywords = re.findall(keyword_pattern, xml_string)

    return hashtags, keywords, meta




def create_ig_post_images(topic, reasons, post):

    def estimate_text_length(text, font_size, max_width):
        """ Schätzt die Länge des Textes basierend auf der Schriftgröße und der maximalen Breite. """
        average_char_width = font_size * 0.6  # Annäherung an die durchschnittliche Breite eines Zeichens
        max_chars_per_line = max_width // average_char_width
        lines = textwrap.wrap(text, width=max_chars_per_line)
        return len(lines)




    slides = []
    print("loading bg img")
    size = (1080, 1080)
    watermark_size = (192, 192)

    background_images = BackgroundImage.objects.filter(theme=post.theme)
    if background_images:
        random_background = random.choice(background_images)
        background_img_path = random_background.image.path
    else:
        background_img_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/background.png')

    first_mask = post.project.slide_mask_first
    if first_mask:
        first_mask_path = first_mask.path
    else:
        first_mask_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/background.png')

    regular_mask = post.project.slide_mask_regular
    if first_mask:
        regular_mask_path = regular_mask.path
    else:
        regular_mask_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/background.png')

    last_mask = post.project.slide_mask_last
    if last_mask:
        last_mask_path = last_mask.path
    else:
        last_mask_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/background.png')

    last_img_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/last.png')

    watermark_path = post.project.watermark.path if post.project.watermark else None


    print("img loaded")
    try:

        regular_background = Image.open(background_img_path).resize(size)
        last_background = Image.open(last_mask_path).resize(size)

    except IOError as e:
        print(f"Fehler beim Laden der Hintergrundbilder: {e}")
        return slides
    try:
        first_mask = Image.open(first_mask_path)
        regular_mask = Image.open(regular_mask_path)
        last_mask = Image.open(last_mask_path)
    except IOError as e:
        print(f"Fehler beim Laden der Masken: {e}")
        return slides


    font_path = os.path.join(settings.STATICFILES_DIRS[0], 'fonts/Roboto-Regular.ttf')

    # Laden Sie die Schriftart
    try:
        font_title = ImageFont.truetype(font_path, size=60)  # Hier können Sie die Schriftgröße anpassen
        font_1 = ImageFont.truetype(font_path, size=48)  # Hier können Sie die Schriftgröße anpassen
        font_2 = ImageFont.truetype(font_path, size=30)  # Hier können Sie die Schriftgröße anpassen
    except IOError as e:
        print(f"Fehler beim Laden der Schriftart: {e}")
        return slides

    bg_img = Image.open(random.choice(background_images).image.path).resize(size)
    overlay = Image.new("RGBA", size, (0, 0, 0, 192))  # 50% Transparenz
    bg_img.paste(overlay, (0, 0), overlay)

    img = regular_background.copy()

    if first_mask_path:
        mask = Image.open(first_mask_path).resize(size)
        bg_img.paste(mask, (0, 0), mask)

    d = ImageDraw.Draw(bg_img)


    title = textwrap.wrap(topic.name, width=30)
    description = textwrap.wrap(topic.description, width=45)
    y_position = 160

    y_position = 320
    for line in title:
        d.text((140, y_position - 20), line, fill=(255, 255, 255), font=font_title)
        y_position += estimate_text_length(line, 60, 1080) * 60  # 42 ist die Schriftgröße

    # Basisverzeichnis für die Slides anpassen
    project_name_slug = slugify(post.project.name.lower())
    base_directory = os.path.join(settings.MEDIA_ROOT, f'projects/{post.project.id}-{project_name_slug}',
                                  f'{post.id}-{slugify(post.topic.name)}', 'slides')

    # Erstellen der Verzeichnisse, falls sie nicht existieren
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    slide_file_name = f"slide_{topic.id}_{topic.name}_first.png"
    slide_path = os.path.join(base_directory, slide_file_name)
    bg_img.save(slide_path)
    slides.append(os.path.relpath(slide_path, settings.MEDIA_ROOT))

    for i in range(0, len(reasons), 2):

        bg_img = Image.open(random.choice(background_images).image.path).resize(size)
        overlay = Image.new("RGBA", size, (0, 0, 0, 192))  # 50% Transparenz
        bg_img.paste(overlay, (0, 0), overlay)

        img = regular_background.copy()


        if regular_mask_path:
            mask = Image.open(regular_mask_path).resize(size)
            bg_img.paste(mask, (0, 0), mask)

        d = ImageDraw.Draw(bg_img)

        # Erster Grund
        reason1 = reasons[i]
        name1 = textwrap.wrap(reason1.name, width=35)
        description1 = textwrap.wrap(reason1.description, width=45)
        y_position = 160

        y_position = 160
        for line in name1:
            d.text((160, y_position), line, fill=(255, 255, 255), font=font_1)
            y_position += estimate_text_length(line, 48, 1080) * 48  # 42 ist die Schriftgröße
        y_position+=20
        for line in description1:
            d.text((200, y_position), line, fill=(255, 255, 255), font=font_2)
            y_position += estimate_text_length(line, 30, 1080) * 30  # 28 ist die Schriftgröße


        # Zweiter Grund, falls vorhanden
        if i + 1 < len(reasons):
            reason2 = reasons[i + 1]
            name2 = textwrap.wrap(reason2.name, width=35)
            description2 = textwrap.wrap(reason2.description, width=45)
            y_position = 560

            for line in name2:
                d.text((160, y_position), line, fill=(255, 255, 255), font=font_1)
                y_position += estimate_text_length(line, 48, 1080) * 48  # 42 ist die Schriftgröße
            y_position += 20
            for line in description2:
                d.text((200, y_position), line, fill=(255, 255, 255), font=font_2)
                y_position += estimate_text_length(line, 30, 1080) * 30  # 28 ist die Schriftgröße

        if watermark_path:
            watermark = Image.open(watermark_path).resize(watermark_size)
            # Positionieren Sie das Wasserzeichen unten links auf dem Bild
            bg_img.paste(watermark, (16, img.height - watermark.height - 16), watermark)
        # Speichern des Bildes
        slide_file_name = f"slide_{topic.id}_{topic.name}_{i // 2}.png"
        slide_path = os.path.join(base_directory, slide_file_name)
        bg_img.save(slide_path)
        slides.append(os.path.relpath(slide_path, settings.MEDIA_ROOT))

    # Letzter Slide
    img = last_background.copy()


    ImageDraw.Draw(img)
    slide_file_name = f"slide_{topic.id}_{topic.name}_last.png"
    slide_path = os.path.join(base_directory, slide_file_name)
    bg_img.save(slide_path)
    slides.append(os.path.relpath(slide_path, settings.MEDIA_ROOT))


    return slides
def add_slide_to_list(img, slides_list, file_name):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)  # Zurücksetzen des Buffers
    slide = ContentFile(buffer.getvalue(), name=file_name)
    slides_list.append(slide)


def create_post_video(topic, reasons, descriptions, mode, theme, category):
    print("loading bg video")
    background_video_path = os.path.join(settings.STATICFILES_DIRS[0], 'video/night_cross_road.mp4')
    music_path = os.path.join(settings.STATICFILES_DIRS[0], 'music/light.mp3')

    background_clip = VideoFileClip(background_video_path).subclip(0, 30)

    # Erstellen des Filter-Overlays (schwarze Ebene mit Transparenz)
    filter_clip = ColorClip(background_clip.size, color=(0, 0, 0), duration=30).set_opacity(0.5)

    # Formatieren des Text-Clips
    formatted_reasons = [f"{i+1}. {reason}" for i, reason in enumerate(reasons)]
    text_content = f"{topic}\n\n" + "\n\n"+"\n\n".join(formatted_reasons)
    text_clip = TextClip(text_content, fontsize=24, color='white', align='center')
    text_clip = text_clip.set_position('center').set_duration(30)

    # Laden der Hintergrundmusik und Anpassen der Dauer
    music_clip = AudioFileClip(music_path).subclip(0, 30)

    # Zusammenfügen aller Komponenten
    final_clip = CompositeVideoClip([background_clip, filter_clip, text_clip])
    final_clip = final_clip.set_audio(music_clip)

    # Speichern des finalen Videos im Media-Ordner
    video_file_name = f'post_video_{topic}.mp4'



    output_path = os.path.join(settings.MEDIA_ROOT, video_file_name)

    relative_video_path = os.path.relpath(output_path, MEDIA_ROOT)



    final_clip.write_videofile(output_path, codec='libx264', fps=24)

    return relative_video_path



def create_long_video(topic, reasons, mode, theme,post, category):


    if not post.audio:
        raise ValueError("Kein AudioComment für diesen Post gefunden.")

    # Pfad zur Sprachdatei aus dem AudioComment
    speech_path = post.audio.audio.path
    speech_clip = AudioFileClip(speech_path)
    speech_clip = speedx(speech_clip, factor=1.2)

    print("loading bg video")
    background_video = BackgroundVideo.objects.filter(theme=theme).order_by('?').first()
    background_music = Music.objects.filter(mode=mode).order_by('?').first()

    # Überprüfen, ob ein Video und eine Musikdatei gefunden wurden
    if not background_video or not background_music:
        raise ValueError("Background video or music not found")

    background_clip = VideoFileClip(background_video.file.path).subclip(0, speech_clip.duration)
    music_clip = AudioFileClip(background_music.file.path).subclip(0, speech_clip.duration)

    filter_clip = ColorClip(background_clip.size, color=(0, 0, 0), duration=speech_clip.duration).set_opacity(0.6)

    # Formatieren des Text-Clips
    formatted_reasons = [f"{i+1}. {reason}" for i, reason in enumerate(reasons)]
    text_content = f"{topic}\n\n" + "\n\n".join(formatted_reasons)
    text_clip = TextClip(text_content, fontsize=24, color='white', align='center')
    text_clip = text_clip.set_position('center').set_duration(speech_clip.duration)

    # Zusammenfügen aller Komponenten
    final_clip = CompositeVideoClip([background_clip, filter_clip, text_clip])
    final_clip = final_clip.set_audio(CompositeAudioClip([music_clip.volumex(0.3), speech_clip.volumex(1.5)]))

    # Speichern des finalen Videos
    video_file_name = f'post_video_{topic}.mp4'
    output_path = os.path.join(settings.MEDIA_ROOT, video_file_name)
    final_clip.write_videofile(output_path, codec='libx264', fps=24)

    return os.path.relpath(output_path, settings.MEDIA_ROOT)




scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_youtube_video(file, title, description, category_id, keywords, privacy_status):



    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Pfad zur client_secret.json Datei
    client_secret_file = os.path.join(settings.STATICFILES_DIRS[0],
                                      "core/client_secret_466800274114-ip61d8ide1tp1i06ial9ctepn8ecd3dv.apps.googleusercontent.com.json")

    # Definieren der benötigten OAuth-Scopes
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Erstellen des OAuth 2.0-Flows
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)

    # Starten des lokalen Servers zur Authentifizierung
    # Dies öffnet einen Browser, um den Authentifizierungsprozess zu starten
    credentials = flow.run_local_server(port=8081)

    # Erstellen des YouTube API-Client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": category_id,
            "description": description,
            "title": title,
            "tags": keywords
          },
          "status": {
            "privacyStatus": privacy_status
          }
        },
        media_body=MediaFileUpload(file)
    )
    response = request.execute()

    print(response)

def upload_image_to_google_drive(image_field_file):
    print("Uploading image to Google Drive...")
    image_path = image_field_file.path
    # Laden Sie Ihre Google API-Zugangsdaten
    credentials_path = os.path.join(settings.STATICFILES_DIRS[0],
                                      "core/client_secret_466800274114-ip61d8ide1tp1i06ial9ctepn8ecd3dv.apps.googleusercontent.com.json")

    # Definieren der benötigten OAuth-Scopes
    scopes =  ['https://www.googleapis.com/auth/drive.file']



    # Erstellen des OAuth 2.0-Flows
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)

    # Starten des lokalen Servers zur Authentifizierung
    # Dies öffnet einen Browser, um den Authentifizierungsprozess zu starten
    creds = flow.run_local_server(port=8081)


    # Erstellen Sie einen Drive-Service-Client
    service = build('drive', 'v3', credentials=creds)
    print("Uploading image...")
    # Hochladen eines Bildes (hier vereinfacht dargestellt)
    file_metadata = {'name': 'image.jpg'}
    media = MediaFileUpload(image_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("Uploading")
    # Setzen der Freigabeeinstellungen auf öffentlich
    file_id = file.get('id')
    service.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()
    print('generate public url')
    # Generieren der öffentlichen URL
    public_url = f"https://drive.google.com/uc?export=view&id={file_id}"
    return public_url
def publish_instagram_image(post):


    print("Publishing")

    access_token = post.project.instagram_account.access_token
    access_token = input("Enter your Instagram")

    print(access_token)
    ig_user_id = post.project.instagram_account.account_id

    image_url = IGSlide.objects.filter(ig_post=post.IGPost).first().png
    print("Image URL: ", image_url)

    public_url = upload_image_to_google_drive(image_url)

    print("Public URL: ", public_url)
    post_url=("https://graph.faceb"
              "ook.com/v18.0/{}/media").format(ig_user_id)
    hashtags = Hashtag.objects.filter(post=post)
    hashtags_str_list = [str(hashtag.name) for hashtag in hashtags]  # Erstellen Sie eine Liste von Hashtag-Strings
    hashtags_str = " ".join(hashtags_str_list)  # Verwenden Sie join, um die Liste in einen String zu konvertieren

    caption = f"{post.meta}\n *\n *\n *\n *\n *\n{hashtags_str}"

    payload = {
        'image_url': public_url,
        'caption': caption,
        'access_token':   access_token

    }
    print(payload)

    r = requests.post(post_url, data=payload)
    print(r.text)
    print("Instagram Post veröffentlicht!")
    pass

def publish_instagram_slider():
    pass

def publish_instagram_video():
    pass


def ai_response_10facts(idea):
    return None


def ai_response_10reasons(idea):
    return None