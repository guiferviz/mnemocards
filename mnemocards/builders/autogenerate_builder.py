import os
import csv
from mnemocards.builders.vocabulary_builder import VocabularyBuilder
from mnemocards.builders.vocabulary_builder import remove_parentheses, remove_spaces


class AutogenerateBuilder(VocabularyBuilder, object):

    def __init__(self):
        pass

    def build_cards(self, data_dir, src, deck_config, clean_audio=True):
        notes, media = [], []

        # Get data from config.
        header = src["header"]
        color = src.get("card_color", "#f5f5f5")
        show_p = "true" if src.get("pronunciation_in_reverse", False) else ""
        tsv_as_source = src.get("use_tsv_for_generation", False)
        filename = os.path.join(data_dir, src["word_file"])

        if tsv_as_source:
            filename = os.path.join(data_dir, src["tsv_file"])

        generate_audio = src.get("audio", False)

        if generate_audio:
            media_dir = self.prepare_media_dir(data_dir, generate_audio)

        furigana = src.get("furigana", False)
        card_properties = src.get("card_properties", None)
        tags = []

        save_tsv = src.get("save_tsv", False)

        if save_tsv:

        if card_properties is not None:
            tags = card_properties.get("tags", [])
        # Read TSV file.

        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            # Skip header if header is true in the configuration file.
            if header:
                next(iterator)
            for i, row in enumerate(iterator):
                note_id, ylw, yle, lylw, lylp, lyle, row_tags = row
                assert type(tags) == list
                note_tags = tags.copy()
                note_tags.extend(row_tags.split(","))
                # Generate audio.
                if generate_audio:
                    clean_text = remove_parentheses(lylw)
                    if furigana:
                        # If you leave those spaces you get wrong
                        # pronunciations, like in `スペイン 人`.
                        # Instead of `supein jin` it pronounces it as
                        # `supein hito` because the kanji `人` alone is
                        # pronounced as `hito`.
                        clean_text = remove_spaces(clean_text)
                    hash_text = get_hash_id(clean_text, bytes=8)
                    sound_file = f"{media_dir}/{hash_text}.mp3"
                    if not os.path.exists(sound_file):
                        print(f"Creating audio file {sound_file}")
                        lang = generate_audio["lang"]
                        tts = gTTS(clean_text, lang=lang)
                        tts.save(sound_file)
                    lylp += f" [sound:{hash_text}.mp3]"
                    media.append(sound_file)
                # Create note.
                note = NoteID(
                    note_id,
                    model=CARD_MODEL_JAPANESE if furigana else CARD_MODEL,
                    fields=[
                        ylw, yle, lylw, lylp, lyle, color, show_p
                    ],
                    tags=note_tags
                )
                notes.append(note)
        # Remove unused audio files.
        # TODO: this should be optional. Add an argument to force clean.
        # FIXME: if you reuse the same media folder for another vocabulary
        # builder you are going to delete media files from the other cards...
        if generate_audio and clean_audio:
            all_audio_files = glob.glob(f"{media_dir}/*.mp3")
            unused_audio_files = set(all_audio_files) - set(media)
            for i in unused_audio_files:
                print(f"Removing unused audio file {i}")
                os.remove(i)

        return notes, media
