use bob;

CREATE TABLE Routine (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    routine_name TEXT NOT NULL,     -- 루틴 이름 (예: 상체 루틴, 다이어트 루틴)
    day_of_week TEXT,       -- 요일 (예: 월요일, Monday)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 생성일
);