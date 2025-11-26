import re

REPLY_PATTERNS = [
    "^On (.*) wrote:$",  # apple mail/gmail reply
    "^Am (.*) schrieb (.*):$",  # German
    "^Le (.*) a écrit :$",  # French
    "^Le (.*), (.*) a écrit :$",  # French alternative
    "El (.*) escribió:$",  # Spanish
    r"^(.*) написал\(а\):$",  # Russian
    "^Den (.*) skrev (.*):$",  # Swedish/Danish/Norwegian
    "^Den (.*) skrev (.*) följande:$",  # Swedish
    "^Den (.*) skrev (.*) følgende:$",  # Norwegian/Danish
    "^(.*) skrev den (.*):$",  # Norwegian alternative
    "^(.*) schreef op (.*):$",  # Dutch
    "^Op (.*) schreef (.*):$",  # Dutch alternative
    "^Il giorno (.*) (.*) ha scritto:$",  # Italian
    "^Il (.*), (.*) ha scritto:$",  # Italian alternative
    "^Em (.*) escreveu:$",  # Brazillian portuguese
    "([0-9]{4}/[0-9]{1,2}/[0-9]{1,2}) (.* <.*@.*>)$",  # gmail (?) reply
]

REPLY_DATE_SPLIT_REGEX = re.compile(
    r"^(.*(:[0-9]{2}( [apAP]\.?[mM]\.?)?)), (.*)?$"
)

FORWARD_MESSAGES = [
    # apple mail forward
    "Begin forwarded message",
    "Anfang der weitergeleiteten E-Mail",  # German
    "Début du message réexpédié",  # French
    "Doorgestuurd bericht volgt",  # Dutch
    "Inizio messaggio inoltrato",  # Italian
    "Vidarebefordrat meddelande börjar",  # Swedish
    "Videresendt melding",  # Norwegian
    "Videresendt besked",  # Danish
    "Inicio del mensaje reenviado",  # Spanish
    # gmail/evolution forward
    "Forwarded [mM]essage",
    "Weitergeleitete Nachricht",  # German
    "Message transféré",  # French
    "Doorgestuurd bericht",  # Dutch
    "Messaggio inoltrato",  # Italian
    "Vidarebefordrat meddelande",  # Swedish
    "Videresendt [mM]elding",  # Norwegian
    "Videresendt e-post",  # Norwegian
    "Videresendt [bB]esked",  # Danish
    "Videresendt e-mail",  # Danish
    "Vidarebefordrad e-post",  # Swedish
    "Doorgestuurde e-mail",  # Dutch
    "E-mail transféré",  # French
    "Courriel transféré",  # French
    "E-mail inoltrata",  # Italian
    "Weitergeleitete E-Mail",  # German
    "Mensaje reenviado",  # Spanish
    # outlook
    "Original [mM]essage",
    "Ursprüngliche Nachricht",  # German
    "Message [dD]'origine",  # French
    "Oorspronkelijk [bB]ericht",  # Dutch
    "Messaggio [oO]riginale",  # Italian
    "Ursprungligt meddelande",  # Swedish
    "Opprinnelig melding",  # Norwegian
    "Oprindelig besked",  # Danish
    "Mensaje [oO]riginal",  # Spanish
    # mail.ru forward (Russian)
    "Пересылаемое сообщение",
]

# We yield this pattern to simulate Outlook forward styles. It is also used for
# some emails forwarded by Yahoo.
FORWARD_LINE = "________________________________"

FORWARD_PATTERNS = (
    [
        f"^{FORWARD_LINE}$",
    ]
    + [f"^---+ ?{p} ?---+$" for p in FORWARD_MESSAGES]
    + [f"^{p}:$" for p in FORWARD_MESSAGES]
)

FORWARD_STYLES = [
    # Outlook starts forwards directly with the "From: " line but we can catch
    # it with the header to avoid falsely identifying a forward
    # - #B5C4DF and #E1E1E1 are known border colors.
    # - "padding:3.0pt 0in 0in 0in" and "padding:3.0pt 0cm 0cm 0cm" are known
    #   paddings.
    re.compile(
        r"^border:none;border-top:solid #[0-9a-fA-f]{6} 1\.0pt;"
        r"padding:3\.0pt 0(in|cm) 0(in|cm) 0(in|cm)$",
        re.UNICODE,
    ),
]


HEADER_MAP = {
    "from": "from",
    "von": "from",  # German
    "de": "from",  # French/Spanish
    "van": "from",  # Dutch
    "da": "from",  # Italian
    "från": "from",  # Swedish
    "fra": "from",  # Norwegian/Danish
    "от кого": "from",  # Russian
    "to": "to",
    "an": "to",  # German
    "para": "to",  # Spanish
    "à": "to",  # French
    "pour": "to",  # French
    "aan": "to",  # Dutch
    "a": "to",  # Italian
    "til": "to",  # Norwegian/Danish/Swedish
    "till": "to",  # Swedish
    "кому": "to",  # Russian
    "cc": "cc",
    "kopie": "cc",  # German
    "kopia": "cc",  # Swedish
    "kopi": "cc",  # Norwegian/Danish
    "bcc": "bcc",
    "cco": "bcc",  # Spanish/Italian
    "cci": "bcc",  # French
    "blindkopie": "bcc",  # German
    "dold kopia": "bcc",  # Swedish
    "blindkopi": "bcc",  # Norwegian/Danish
    "reply-to": "reply-to",
    "antwort an": "reply-to",  # German
    "antwoord aan": "reply-to",  # Dutch
    "répondre à": "reply-to",  # French
    "rispondi a": "reply-to",  # Italian
    "svara till": "reply-to",  # Swedish
    "svar til": "reply-to",  # Norwegian/Danish
    "responder a": "reply-to",  # Spanish
    "date": "date",
    "sent": "date",
    "received": "date",
    "datum": "date",  # German/Dutch/Swedish
    "dato": "date",  # Norwegian/Danish
    "gesendet": "date",  # German
    "verzonden": "date",  # Dutch
    "data": "data",  # Italian
    "envoyé": "date",  # French
    "envoyé le": "date",  # French
    "sendt": "date",  # Norwegian/Danish
    "skickat": "date",  # Swedish
    "enviado el": "date",  # Spanish
    "enviados": "date",  # Spanish
    "fecha": "date",  # Spanish
    "дата": "date",  # Russian
    "subject": "subject",
    "betreff": "subject",  # German
    "onderwerp": "subject",  # Dutch
    "oggetto": "subject",  # Italian
    "objet": "subject",  # French
    "sujet": "subject",  # French
    "ämne": "subject",  # Swedish
    "emne": "subject",  # Norwegian/Danish
    "asunto": "subject",  # Spanish
    "тема": "subject",  # Russian
}

HEADER_KEYS = list(HEADER_MAP.keys())
HEADER_OR = "|".join(re.escape(k) for k in HEADER_KEYS)
HEADER_RE = re.compile(
    rf"^\s*\*?({HEADER_OR})\s*:\*?(.*)$",
    flags=re.IGNORECASE | re.UNICODE,
)

COMPILED_PATTERN_MAP = {
    "reply": [re.compile(regex) for regex in REPLY_PATTERNS],
    "forward": [re.compile(regex) for regex in FORWARD_PATTERNS],
}

COMPILED_PATTERNS: list[re.Pattern] = [
    pattern
    for patterns in COMPILED_PATTERN_MAP.values()
    for pattern in patterns
]

MULTIPLE_WHITESPACE_RE = re.compile(r"\s+")

# Amount to lines to join to check for potential wrapped patterns in plain text
# messages.
MAX_WRAP_LINES = 2

# minimum number of headers that we recognize
MIN_HEADER_LINES = 2

# minimum number of lines to recognize a quoted block
MIN_QUOTED_LINES = 3

# Characters at the end of line where we join lines without adding a space.
# For example, "John <\njohn@example>" becomes "John <john@example>", but
# "John\nDoe" becomes "John Doe".
STRIP_SPACE_CHARS = r"<([{\"'"
