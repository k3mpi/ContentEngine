api_key = "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"
# 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
OPENAI_API_KEY = "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"

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


def create_article(post):
    print("creating ai response")

    prompt = """
    Erstelle zum gegebenen Kontext einen langen und umfangreichend Artikel. Grundlage sind zehn gründe zu einem Thema und keywords und hashtags.
    Auf dieser grundlage sollst du nun ein passendes Thema finden worüber du einen Artikel schreiben sollst. es Soll zu den GRünden passen.
    Ein artikel ist wie folgt gegliedert:
    
    title: packende und interessante überschrift
    intro: kurze einleitung über 3-4 Sätze
    
    unterpunkt_1: titel zur subtopic / unterthema
    text_1: text zur subtopic / unterthema 
        
    unterpunkt_2: titel zur subtopic / unterthema
    text_2: text zur subtopic / unterthema 
        
    unterpunkt_3: titel zur subtopic / unterthema
    text_3: text zur subtopic / unterthema 
    
    cta_title : titel der abschließenden call to action 
    cta_text : text zur call to action
    
    Nachfolgend das XML Format wie die Response formatiert werden soll:
    <title> title </title>
    <intro> introduction </intro>  
    <subtitle> subtitle 1</subtitle> 
    <text> text 1 </text>
    <subtitle> subtitle 2</subtitle> 
    <text>text 2</text>
    <subtitle> subtitle 3</subtitle> 
    <text>text 3</text>
    <cta_title> call to action title</cta_title> 
    <cta_text> call to action text </cta_text> 
    
   
     Hier der Content welcher als quelle dient finde eine intereassante topic, die den leser neugierig macht und schreibe einen ca 500 wörter langen artikel schreibe nicht über 10 gründe sondern verfasse einen allgemeineren artikel als 10 gründe für ...:
     """
    content = post.get_full_content()
    prompt += content

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))


def hashtag_data(post):
    print("creating ai response")

    prompt = """
   Es sollen Hashtags anhand eines Beitrags erstellt werden. Die Hashtags sollen möglichst organisch sein.
   Erstelle eine Liste mit 20 relevanten Hashtags aus. 
    Dann sollen SEO Keywords gefunden werden. Erstelle eine Liste mit 5 Keywords.
    zusätzlich soll eine Metabeschreibung erstellt werden. 2 -3 Knackige Sätze, welche das
   oder die Hauptkeywords wiederspigeln.

     nutze als Ausgabeformat foldende XML-Vorlage:

     <hashtag> hashtag 1 </hashtag>
     <hashtag> hashtag 2</hashtag>

     ...
     <hashtag> hashtag 10 </hashtag>
     
    <keyword> keyword 1 </keyword>
    <keyword> keyword 2 </keyword>
    
    <keyword> keyword 5 </keyword>
    
    <meta> Metabeschreibung </meta>
     


     Halte dich unbedingt an dieses Format und gib immer genau 20 Hashtags aus

     Die Trends lauten:

     """
    content = post.get_full_content()
    prompt += content

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))


def ideas_from_trends(trends):
    print("creating ai response")

    prompt = """
     Es soll eine Liste mit Topics erstellt werden. Ich möchte aus den Topics Listen mit 10 unterpunkten für diese Topic erstellen.
     Gib Mir 10  topics passend zu den Trends.  es soll sowas wie eine aussage, thema, fakten, etc. erstellt werden. wozu später je 10 unterpunkte gesucht werden. 
     die topics sollen möglichst positiv und bekräftigend sein.

     nutze als Ausgabeformat foldende XML-Vorlage:

     <idee> topic 1 </idee>
     <idee> topic 2</idee>

     ...
     <idee> topic 10 </idee>

    
     Halte dich unbedingt an dieses Format und gib immer genau 10 Ideen/Topics

     Die Trends lauten:

     """

    prompt += trends

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))



def  ai_response(idea):
    print("creating ai response")

    prompt = """
    Es soll eine Liste mit 10 Gründen für eine Sache / Thema erstellt werden.
    
    Erstelle eine topic wie "10 Gründe um ...". Die Topic fängt immer mit "10 Gründe um" an Erstelle genau 10 reasons, also Gründe zu dieser Topic:
    
    nutze als Ausgabeformat foldende XML-Vorlage:
    
    <topic> erstellte topic </topic>
    <reason_1> erklärung 1</reason_1>
    <description_1> grund 1</description_1>
    <reason_2> grund 2</reason_2>
    <description_2> erklärung 2</description_2>
    ...
    <reason_10> grund 10 </reason_10>
    <description_10> erklärung 10</description_10>
    
    Halte dich unbedingt an dieses Format und gib immer genau 10 gründe an.
    formuliere die gründe jeweils als ganzen Satz.
    Schreibe zu jedem Grund eine erklärung in der du Detaillierter auf den Grund eingehst.
    Sei bei den Gründen Kreativ, Motivierend und ansprechend. 
    
    Das Thema lautet:
    
    """
    prompt = """
        Es soll eine Liste mit 10 unterthemen/unterpunkten  zu einer Sache / Thema erstellt werden.
        die unterthemen können sein:
        10 Fakten zu einem Thema,
        10 Gründe für eine Sache,
        Top 10 Liste zu einem Thema,
        10 Punkte zu einer Sache -> generelle informationen etc.
        Erstelle eine packende Topic. Erstelle genau 10 unterthemen/unterpunkte zu dieser Topic. zu jedem
        Unterpunkt soll eine Topic erstellt werden.

        nutze als Ausgabeformat foldende XML-Vorlage:

        <topic> erstellte topic </topic>
        <reason_1> unterpunkt 1</reason_1>
        <description_1> erklärung 1</description_1>
        <reason_2> unterpunkt 2</reason_2>
        <description_2> erklärung 2</description_2>
        ...
        <reason_10> unterpunkt 10 </reason_10>
        <description_10> erklärung 10</description_10>

        Halte dich unbedingt an dieses Format und gib immer genau 10 gründe an.
        formuliere die gründe jeweils als ganzen Satz.
        Schreibe zu jedem Grund eine erklärung in der du Detaillierter auf den Grund eingehst.
        Sei bei den Gründen Kreativ, Motivierend und ansprechend. 

        Das Thema lautet:

        """
    prompt += idea

    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
        {"role": "user", "content": prompt}
      ]
    )

    print(completion.choices[0].message)

    return(str(completion.choices[0].message))

from gtts import gTTS
import os
from django.conf import settings

def text_to_speech(text,name, lang='de'):
    tts = gTTS(text=text, lang=lang)
    filename = f"{name}.mp3"  #
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    tts.save(file_path)
    return file_path
def create_audio_skript(post):
    print("creating ai response")

    prompt = """
    erstelle ein packendes und interessantes audio skript für ein video auf basis des gegebenen contents.
    die audio soll ca. 45 sekunden dauern
    
    das skript soll in einem <skript></skript> XML Tag ausgegeben werden.
    
    Die Formatierung sieht so aus: 
    <skript>Audio Skript</skript>
    
     """

    prompt += post.get_full_content()

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))

    return None


def ai_response_10reasons(idea):
    print("creating ai response 10 reasons")

    prompt = """
    Es soll eine Liste mit 10 Gründen für eine Sache / Thema erstellt werden.

    Erstelle eine topic wie "10 Gründe um ...". Die Topic fängt immer mit "10 Gründe um" an Erstelle genau 10 reasons, also Gründe zu dieser Topic:

    nutze als Ausgabeformat foldende XML-Vorlage:

    <topic> erstellte topic </topic>
    <reason_1> erklärung 1</reason_1>
    <description_1> grund 1</description_1>
    <reason_2> grund 2</reason_2>
    <description_2> erklärung 2</description_2>
    ...
    <reason_10> grund 10 </reason_10>
    <description_10> erklärung 10</description_10>

    Halte dich unbedingt an dieses Format und gib immer genau 10 gründe an.
    formuliere die gründe jeweils als ganzen Satz.
    Schreibe zu jedem Grund eine erklärung in der du Detaillierter auf den Grund eingehst.
    Sei bei den Gründen Kreativ, Motivierend und ansprechend. 

    Das Thema lautet:
    """
    prompt += idea

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))


def ai_response_10facts(idea):
    print("creating ai response 10 facts")

    prompt = """
                Es soll eine Liste mit 10 interessanten Fakten  zu einer Sache / Thema erstellt werden.
                das thema soll so strukturiert und erklärt werden.:

                Erstelle eine packende Topic. Erstelle genau 10 Fakten zu dieser Topic. zu jedem
                Fakt soll eine erläuterung erstellt werden.

                nutze als Ausgabeformat foldende XML-Vorlage:

                <topic> erstellte topic </topic>
                <reason_1> fakt 1</reason_1>
                <description_1> erläuterung 1</description_1>
                <reason_2> fakt 2</reason_2>
                <description_2> erläuterung 2</description_2>
                ...
                <reason_10> fakt 10 </reason_10>
                <description_10> erläuterung 10</description_10>

                Halte dich unbedingt an dieses Format und gib immer genau 10 fakten an.
                Schreibe zu jedem fakt eine erläuterung, in der du auf den fakt eingehst.
                Sei Kreativ, sachlich und ansprechend. 

                Das Thema lautet:

                """
    prompt += idea

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))

def ai_response_10paragraphs(idea):
    print("creating ai response 10 paragraphs")

    prompt = """
            Es soll eine Liste mit 10 unterthemen/unterpunkten/paragraphen  zu einer Sache / Thema erstellt werden.
            das thema soll so strukturiert und erklärt werden.:
           
            Erstelle eine packende Topic. Erstelle genau 10 unterpunkte zu dieser Topic. zu jedem
            Unterpunkt soll ein paragraph erstellt werden.

            nutze als Ausgabeformat foldende XML-Vorlage:

            <topic> erstellte topic </topic>
            <reason_1> unterpunkt 1</reason_1>
            <description_1> paragraph 1</description_1>
            <reason_2> unterpunkt 2</reason_2>
            <description_2> paragraph 2</description_2>
            ...
            <reason_10> unterpunkt 10 </reason_10>
            <description_10> paragraph 10</description_10>

            Halte dich unbedingt an dieses Format und gib immer genau 10 unterpunkte an.
            formuliere die unterpunkte als packende und interessante Überschrift
            Schreibe zu jedem punkt eine erklärung in der du auf den punkt eingehst.
            Sei Kreativ, sachlich und ansprechend. 

            Das Thema lautet:

            """
    prompt += idea

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))


def ai_response_top10(idea):
    print("creating ai response Top 10")

    prompt = """
                    Es soll eine Top 10 Liste zu einer Thematik erstellt werden.
                    Erstelle eine packende Topic. Erstelle genau 10 Plätze zu dieser Topic. Setze die 
                    Pätze in ein Ranking von 1-10. für jeden Platz soll eine beschreibung/begründung
                    erstellt werden

                    nutze als Ausgabeformat foldende XML-Vorlage:

                    <topic> erstellte topic </topic>
                    <reason_1> platz 1</reason_1>
                    <description_1> beschreibung 1</description_1>
                    <reason_2> platz 2</reason_2>
                    <description_2> beschreibung 2</description_2>
                    ...
                    <reason_10> platz 10 </reason_10>
                    <description_10> beschreibung 10</description_10>

                    Halte dich unbedingt an dieses Format und gib immer genau 10 Plätze an.
                    Schreibe zu jedem PLatz eine begründung.
                    Sei Kreativ, sachlich und ansprechend. 

                    Das Thema lautet:

                    """
    prompt += idea

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Du erstellst nach bedarf content, welcher in einer python anwendung weiterverarbeitet wird"},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return (str(completion.choices[0].message))