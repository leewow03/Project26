CREATE TABLE PI (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    height REAL,            -- 키
    weight REAL,            -- 몸무게
    body_fat REAL,          -- 체지방률
    muscle_mass REAL,       -- 근육량
    recorded_at DATE DEFAULT (CURRENT_DATE) -- 기록 날짜
);