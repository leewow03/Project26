use bob;

CREATE TABLE Exercise (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
	Exercise_name TEXT NOT NULL,     -- 종목명 (예: 스쿼트)
    target_muscle TEXT      -- 타겟 부위 (예: 하체)
);