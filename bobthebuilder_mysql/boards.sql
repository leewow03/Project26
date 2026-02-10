SELECT * FROM bob.member;
CREATE TABLE boards (
    id INT AUTO_INCREMENT PRIMARY KEY,    -- 고유 번호 (PK)
    title VARCHAR(255) NOT NULL,          -- 글 제목
    content TEXT NOT NULL,                -- 글 내용
    member_id INT NOT NULL,               -- 작성자 고유 번호 (FK: Member.id)
    active TINYINT(1) DEFAULT 1,          -- 삭제 여부 (1: 활성, 0: 삭제됨)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 작성일
    
    -- 이 아래 줄이 핵심입니다!
    CONSTRAINT fk_board_member FOREIGN KEY (member_id) REFERENCES Member(id) ON DELETE CASCADE
);


