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
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "宮城県": "Miyagi",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa",
}
