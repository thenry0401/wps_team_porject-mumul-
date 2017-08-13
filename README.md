pych# 9조 물물교환

김종훈, 이철규

---

## 목차

1. 프로젝트 주제
2. 핵심기능
3. 역할분담
4. 질문사항

---

## 1. 프로젝트


![사진](http://cfile10.uf.tistory.com/attach/2075323C4D2305142E5709)
>클립으로 집을 산 남자의 이야기

![사진](http://cfile2.uf.tistory.com/image/114E5F374F39F44F2BA2F7)
>중고나라


특징 : 현금거래 없이 오직 물건대 물건으로만 교환하는 플랫폼

---

## 2. 구현해보고 싶은 것들

`?`가 붙은 것들은 배우지 않았던 미지의 분야

### 유저(user)

  1. 이메일 인증하기
  2. 회원가입 시 축하 이메일 발송(AWS SES 서비스 이용해보기)
  3. 소셜 로그인

### 아이템(item)

  1. 몇 단계를 거쳐야 내가 원하는 품목을 얻을 수 있을까
  2. 아이템 찜하기
  3. 해쉬태그

---


## 3. 역할분담

김종훈
  1. Post 모델링
이철규
  1. 유저 모델링
  2. 유저 정보를 활용한 쿼리셋 작성(지역별 매칭, 거리별 매칭)
  3. 관리자 페이지..?
      - 유저 가입 경로 통계, 거래 회수 합산, 인기 품목 조회
