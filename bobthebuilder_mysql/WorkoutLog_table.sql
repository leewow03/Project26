use bob;

CREATE TABLE WorkoutLog (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    routine_id INTEGER,     -- 어떤 루틴에 속하는가 (외래키)
    exercise_id INTEGER,    -- 어떤 운동을 했는가 (외래키)
    weight REAL,            -- 무게
    reps INTEGER,           -- 횟수
    duration_seconds INTEGER, -- 수행 시간 (초 단위가 계산하기 편해요)
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 관계 설정
    FOREIGN KEY (routine_id) REFERENCES Routine(id),
    FOREIGN KEY (exercise_id) REFERENCES Exercise(id)
);