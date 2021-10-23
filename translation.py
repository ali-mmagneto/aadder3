
class Translation (object):

    START_TEXT = """<b>Hey,</b>\n
<b>This is a Telegram Bot to Merge Subtitle into a video</b>

<b>Send me a Telegram file to Get started</b>

Use help Command for more details..

    """

    
    
    DOWNLOAD_SUCCESS = """File downloaded successfully!

Time taken : {} seconds."""
    FILE_SIZE_ERROR = "ERROR : Cannot Extract File Size from URL!"
    MAX_FILE_SIZE = "File size is greater than 2Gb. Which is the limit imposed by telegram!"
    LONG_CUS_FILENAME = """Filename you provided is greater than 60 characters.
Please provide a shorter name."""
    UNSUPPORTED_FORMAT = "ERROR : File format {} Not supported!"
