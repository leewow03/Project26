create schema bob;
use bob;


CREATE TABLE Member(
    id INT AUTO_INCREMENT PRIMARY KEY,      -- 고유 번호 (내부 관리용)
    uid VARCHAR(50) UNIQUE NOT NULL,        -- 로그인 아이디 (중복 불가)
    password VARCHAR(255) NOT NULL,         -- 비밀번호 (암호화 대비 길게)
    name VARCHAR(50) NOT NULL,              -- 이름
    role VARCHAR(20) DEFAULT 'user',        -- 권한 (admin, user 등)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- 가입일
);

select *from Member;


