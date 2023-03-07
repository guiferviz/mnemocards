from mnemocards import PydanticTask


class Pronounce(PydanticTask):
    """Pronounce text in a note attribute.

    Attributes:
        language: [Two-letter
            code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the
            language to use in the pronunciation.
        attribute_to_pronounce: Note attribute to pronounce.
        append_media_file_to: Append generated media file path to a list
            attribute. This is needed for later steps that want to access the
            media files. For example, to package notes in an APKG we need to
            know where the media files are stored in order to include them in
            the APKG.
        output_dir: Output directory where generated files will be stored. This
            directory is relative to the global output_dir.
    """

    language: str
    attribute_to_pronounce: str
    append_media_file_to: str = "media_files"
    output_dir: str = "./media_files"
