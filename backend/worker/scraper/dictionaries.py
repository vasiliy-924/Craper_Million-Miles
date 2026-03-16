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

SPEC_LABEL_MAP = {
    "年式(初度登録年)": "year",
    "走行距離": "mileage_km",
    "本体価格": "price_jpy",
    "支払総額": "total_price_jpy",
    "ミッション": "transmission",
    "エンジン種別": "fuel",
    "ボディタイプ": "body_type",
}

PREFECTURE_MAP = {
    "北海道": "Hokkaido",
    "東京都": "Tokyo",
    "大阪府": "Osaka",
    "愛知県": "Aichi",
    "神奈川県": "Kanagawa",
    "福岡県": "Fukuoka",
}
