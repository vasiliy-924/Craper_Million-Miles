"""Japanese-to-English mapping for car attributes."""

BRAND_MAP = {
    "トヨタ": "Toyota",
    "ホンダ": "Honda",
    "日産": "Nissan",
}

FUEL_MAP = {
    "ガソリン": "petrol",
    "ディーゼル": "diesel",
    "ハイブリッド": "hybrid",
    "電気": "electric",
    "レギュラー": "petrol",
}

TRANSMISSION_MAP = {
    "フロアCVT": "CVT",
    "インパネCVT": "CVT",
    "フロアMTモード付CVT": "CVT",
    "インパネ4AT": "AT",
    "インパネ6AT": "AT",
    "フロアMT": "MT",
    "その他AT": "AT",
}

BODY_TYPE_MAP = {
    "ハッチバック": "hatchback",
    "ハッチバック・ミニバン": "hatchback",
    "ミニバン": "minivan",
    "SUV・クロカン": "SUV",
    "クロカン・ＳＵＶ": "SUV",
    "セダン": "sedan",
    "ステーションワゴン": "sedan",
    "クーペ": "coupe",
    "コンパクトカー": "compact",
    "その他": "other",
}

# For spec labels if you want to translate them later
SPEC_LABEL_MAP = {
    "年式(初度登録年)": "year",
    "走行距離": "mileage",
    "ボディタイプ": "body_type",
    "ミッション": "transmission",
    "エンジン種別": "fuel",
}