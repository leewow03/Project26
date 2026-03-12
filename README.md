# Project26__
```
├──  run.py  # 실행 버튼만
│
├── app/
│   │ 	├── models/
│  	│	│	├── Board: 게시판, 자료실
│   │	│	├── Exercise: 종목명, 타겟 부위 정보
│   │  	│	├── Member: 회원정보
│   │	│	├── PI  : 키, 몸무게, 체지방, 근육량
│   │   │	├── Routine 루틴 이름, 요일, 생성일
│   │	├──  Score: 점수로 등급제
│	│	└── WorkoutLog: 무게, 횟수, 수행 시간
│	│
│	├──routes/
│	└── services/
│			
├── static/
│
└── templates/
		├── auth
		└── layout


```



```
workout_project/
├── run.py                 # [실행] 서버를 켜는 메인 스위치
├── config.py              # [설정] Secret Key(세션용), DB 주소 등 보안 설정
│
└── app/                   # [패키지] 홈페이지 본체 폴더
    ├── __init__.py        # [연결] 블루프린트 등록 및 앱 초기화 (라우터들을 합치는 곳)
    ├── models.py          # [데이터] Member, PI, Exercise, Routine, WorkoutLog 등 (재료)
    │
    ├── views/             # [라우터 + 로직] @bp.route가 위치하는 곳
    │   ├── auth_views.py  # 로그인(세션 생성), 로그아웃, 회원가입 담당
    │   ├── work_views.py  # 운동 기록, 루틴 관리 (로그인 세션 확인)
    │   └── main_views.py  # 홈 화면, 대시보드 표시
    │
    ├── services/          # [계산기] 뷰에서 호출하는 복잡한 로직 (선택 사항)
    │   ├── score_service.py # 점수 계산, 등급 판별 공식
    │   └── health_service.py # BMI 계산, PI 변화 분석
    │
    ├── static/            # [자원] CSS, 이미지(운동 아이콘), JS
    └── templates/         # [화면] HTML 파일 (그릇)
        ├── layout.html    # 공통 뼈대 (상단바에 로그인/로그아웃 버튼)
        ├── auth/          # login.html, signup.html
        └── exercise/      # workout_log.html, routine_list.html
```
