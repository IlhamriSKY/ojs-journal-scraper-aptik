from collections import OrderedDict

sources = OrderedDict([
    ("unpar", "https://journal.unpar.ac.id/"),
    ("uaj", "https://ejournal.atmajaya.ac.id"),
    ("ukwms", "https://journal.ukwms.ac.id/"),
    ("scu", "https://journal.unika.ac.id/"),
    ("uajy", "https://ojs.uajy.ac.id/"),
    ("usd", "https://e-journal.usd.ac.id/"),
    ("unwira", "https://journal.unwira.ac.id/"),  # Blocked by Cloudflare
    ("ust", "https://ejournal.ust.ac.id/"),
    ("uwdp", "https://journal.widyadharma.ac.id/"),
    ("ukdc", "https://jurnal.ukdc.ac.id/"),
    ("stikvinc", "https://journal.stikvinc.ac.id"),
    ("stikcarolus", "https://jurnal.stik-sintcarolus.ac.id"),
    ("stikeselisabeth", "http://ejournal.stikeselisabethmedan.ac.id:85")
])


university_mapping = {
    "unpar.ac.id": "Universitas Katolik Parahyangan",
    "atmajaya.ac.id": "Universitas Katolik Indonesia Atma Jaya",
    "ukwms.ac.id": "Universitas Katolik Widya Mandala Surabaya",
    "unika.ac.id": "Soegijapranata Catholic University",
    "uajy.ac.id": "Universitas Atma Jaya Yogyakarta",
    "usd.ac.id": "Universitas Sanata Dharma",
    "unwira.ac.id": "Universitas Katolik Widya Mandira",
    "ust.ac.id": "Unika St. Thomas Medan",
    "widyadharma.ac.id": "Universitas Widya Dharma Klaten",
    "ukdc.ac.id": "Universitas Katolik Darma Cendika",
    "stikvinc.ac.id": "STIKES Katolik St. Vincentius a Paulo Surabaya",
    "stik-sintcarolus.ac.id": "STIK Sint Carolus",
    "stikeselisabethmedan.ac.id": "STIKES Elisabeth Medan"
}
