import requests, bot, time


url = "https://discord.com/api/v8/applications/{bot-id}/commands"


headers = {
    "Authorization": "Bot " + bot.TOKEN
}

st = [
    {
        "name": "버튼설정",
        "description": "버튼 자판기를 해당 채널에 추가합니다.",
        "options": [],
    },
    {
        "name": "가입",
        "description": "자판기에 가입합니다.",
        "options": [],
    },
    {
        "name": "버튼설정",
        "description": "버튼 자판기를 해당채널에 추가합니다.",
        "options": [],
    },
    {
        "name": "잔액",
        "description": "자신의 잔액을 조회합니다..",
        "options": [],
    },
        {
        "name": "제품목록",
        "description": "제품 목록, 가격, 재고 상황을 봅니다..",
        "options": [],
    },
    {
        "name": "패널",
        "description": "관리자 패널 계정을 불러옵니다.",
        "options": [],
    },
    {
        "name": "구매",
        "description": "입력한 제품을 구매합니다.",
        "options": [
            {
                "type": 3,
                "name": "상품명",
                "description": "상품명을 입력해 주세요."
            },
            {
                "type": 4,
                "name": "개수",
                "description": "구매하실 상품의 개수를 입력해 주세요."
            }
        ],
    },
    {
        "name": "충전",
        "description": "문화상품권 충전을 진행합니다.",
        "options": [
            {
                "type": 3,
                "name": "코드",
                "description": "문화상품권 코드를 입력해 주세요."
            }
        ],
    }
]
for json in st:
    r = requests.post(url, headers=headers, json=json)
    print(r.text)
    time.sleep(4)