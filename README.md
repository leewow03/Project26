# Project26

"""
   운동용/
│
├── run.py                # 1. 실행 스위치 (딱 서버만 켜는 코드)
├── config.py             # 2. 비밀 설정 (DB 비번, 시크릿 키 등)
│
├── app/                  # 회원로그인
│   ├── __init__.py       # Flask 설정 초기화 (조립 설명서)
│   ├── routes/           # 3. 길 안내 (login_route.py, board_route.py)
│   ├── models/           # 4. 창고 설계도 (회원 테이블, 게시판 테이블 정의)
│   │                      Routine: 이름, 요일, 생성일 정보를 가짐.
│   │                      Exercise: 종목명, 타겟 부위 정보를 가짐.
│   │                      WorkoutLog: 무게, 횟수, 수행 시간 정보를 가짐.
│   └── services/         # 5. 복잡한 계산 (비번 암호화, 데이터 가공)
│                          Routine Service: "월요일 루틴을 가져와서 오늘 운동할 목록을 만들어라."
│                          Log Service: "사용자가 입력한 무게가 저번보다 무거우면 '최고 기록 달성!' 알림을 띄워라."
│                          Exercise Service: "새로운 운동 종목을 추가할 때 이미 있는 이름인지 중복 체크해라."
│                             Session
│                             Crm
│
├── static/               # [정적 자원: 변하지 않는 것들]
│   ├── css/              # 디자인 (모든 페이지 공용)
│   └── js/               # 동작 (회원가입 유효성 검사 등)
│
└── templates/            # [설계도: 화면 화면들]
    ├── layout/           # 공통 양식 (상단 메뉴바, 하단 푸터)
    └──── auth/           #  관련 HTML
                            join.html
                            login.html
                            main.html

"""
