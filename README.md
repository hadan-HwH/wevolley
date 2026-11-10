<p align="center">
  <img src="assets/hero.png" alt="WeVolley: 오늘 배구, 어디서 할까?" width="100%">
</p>

<p align="center">
  <img src="assets/icon.png" width="72" alt="WeVolley 아이콘">
</p>

<h1 align="center">WeVolley 위볼리</h1>

<p align="center">
  배구 클럽 찾기부터 게스트 참여, 클럽 운영까지.<br>
  기획 · 디자인 · 개발 · 배포 · 운영을 한 사람이 하는 멀티플랫폼 앱
</p>

<p align="center">
  <a href="https://play.google.com/store/apps/details?id=com.wevolley.app"><img src="https://img.shields.io/badge/Google_Play-17181A?style=for-the-badge&logo=googleplay&logoColor=C8F135" alt="Google Play"></a>
  <a href="https://apps.apple.com/kr/app/%EC%9C%84%EB%B3%BC%EB%A6%AC-wevolley/id6805284166"><img src="https://img.shields.io/badge/App_Store-17181A?style=for-the-badge&logo=appstore&logoColor=C8F135" alt="App Store"></a>
  <a href="https://wevolley.sub-co.com"><img src="https://img.shields.io/badge/Web-17181A?style=for-the-badge&logo=googlechrome&logoColor=C8F135" alt="Web"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Expo-SDK_55-C8F135?style=flat-square&logo=expo&logoColor=white&labelColor=17181A" alt="Expo SDK 55">
  <img src="https://img.shields.io/badge/React_Native-0.83-C8F135?style=flat-square&logo=react&logoColor=white&labelColor=17181A" alt="React Native 0.83">
  <img src="https://img.shields.io/badge/TypeScript-5.9-C8F135?style=flat-square&logo=typescript&logoColor=white&labelColor=17181A" alt="TypeScript 5.9">
  <img src="https://img.shields.io/badge/Supabase-self--hosted-C8F135?style=flat-square&logo=supabase&logoColor=white&labelColor=17181A" alt="Supabase self-hosted">
  <img src="https://img.shields.io/badge/TanStack_Query-5-C8F135?style=flat-square&logo=reactquery&logoColor=white&labelColor=17181A" alt="TanStack Query 5">
  <img src="https://img.shields.io/badge/AWS-Seoul-C8F135?style=flat-square&labelColor=17181A" alt="AWS Seoul">
</p>

> 소개용 저장소다. 앱 코드는 비공개 저장소에 있다.

<p align="center">
  <img src="assets/numbers.png" width="100%" alt="가입자 325, 클럽 · 학원 정보 309, 화면 81, 테이블 72 (2026.11)">
</p>

## 화면

<p align="center">
  <img src="assets/screens/01-home.png" width="24%" alt="홈">
  <img src="assets/screens/02-clubs-map.png" width="24%" alt="클럽 지도">
  <img src="assets/screens/03-guest.png" width="24%" alt="게스트 신청">
  <img src="assets/screens/04-manage.png" width="24%" alt="클럽 운영">
</p>

## 하는 일

- **찾기**: 지도 · 지역 · 이름으로 클럽과 게스트를 모집 중인 일정 찾기
- **게스트**: 가입 전에 게스트로 신청하고 운영진이 승인
- **클럽 운영**: 일정과 참석 투표, 회원, 회비 장부, 공지, 회칙
- **소통**: 클럽 채팅, 커뮤니티, 알림
- **기록**: 날짜마다 남기는 운동 일지
- **영상(베타)**: 경기 영상을 올려 클럽에 공유. 랠리와 내 장면 찾기는 [따로 만드는 비전 엔진](https://github.com/hadan-HwH/volleyball-vision)으로 준비 중
- **공유**: 클럽 · 일정 링크를 로그인 없이 열고, 카톡 · 슬랙에 미리보기
- **다국어**: 한국어 · 영어 · 일본어 · 중국어(간체)
- **운영 도구**: 신고 처리, 사용자 관리

## 아키텍처

<p align="center">
  <img src="assets/architecture.png" width="100%" alt="아키텍처: 모바일 앱과 웹 SPA 가 supabase-js 로 AWS 서울에서 직접 운영하는 오픈소스 Supabase(Postgres · Realtime · Edge Functions)를 쓰고, 공유 링크는 CloudFront Function 이 share-page 로 넘기며, 알림은 트리거 → send-push → Expo Push">
</p>

## 엔지니어링

### 한 코드로 Android · iOS · 웹

- Expo Router 화면 81개를 세 플랫폼이 함께 쓴다. 웹은 react-native-web 으로 그린다.
- 지도 같은 네이티브 전용 모듈은 `*.native.tsx` / `*.web.tsx` 파일로 나눈다.
- 웹에서만 확인하면 놓치는 함정을 규칙으로 만들었다. NativeWind 네이티브 런타임이 함수형 `style` 을 빈 객체로 바꿔 버린 실제 사고 뒤에는 ESLint 규칙과 테스트로 막는다. `Alert.alert` 는 웹에서 아무것도 띄우지 않아 금지하고 확인 모달과 토스트로 바꿨다.
- 화면 문구 2,200여 개를 Lingui 로 관리해 4개 언어로 낸다.

### 로그인 없이 열리는 공유 링크

- 미리보기용 OG 엔트리(`/s/{type}/{id}`)와 원본 URL(`/club/{id}` 등)을 나눴다.
- OG 엔트리는 CloudFront Function 이 주소만 바꿔 Edge Function(`share-page`)으로 넘긴다. 관리형 Supabase 를 쓸 때는 게이트웨이가 `text/html` 을 `text/plain` 으로 바꿔 보내서 서버리스 프록시가 본문을 다시 실어야 했는데, 백엔드를 직접 운영하면서 프록시를 없앴다.
- 크롤러가 아니면 원본 URL 로 보내고, 원본은 SPA 가 로그인 없이 게스트 화면으로 그린다. Android 는 `intent://` 로 앱이나 스토어를, iOS 는 유니버설 링크로 앱을 연다.
- 공유 링크 4종의 연결을 배포 직후와 매주 자동으로 점검한다(GitHub Actions, 읽기 전용).
- 클럽 · 지역 페이지는 빌드할 때 정적 HTML 로 미리 만들어 검색에 노출한다. 요청마다 도는 함수가 없어 느려지지 않는다.

### 데이터 계층 규칙을 코드로 강제

- 화면은 조합만 하고, 조회와 변경은 도메인 훅이 맡는다. 쿼리 키는 팩토리 한 곳에서만 만든다.
- 모든 쿼리는 실패했을 때를 분류한다. 화면의 주 행동을 막으면 critical(다시 시도 화면), 보조 정보면 degrade-ok(이유 주석 필수). 스크립트가 빠진 곳을 찾는다.
- 변경은 낙관적으로 먼저 반영하고 실패하면 되돌린다. 쿼리 캐시는 AsyncStorage 에 저장해 다시 열면 마지막 화면부터 보인다.

### 규칙은 Postgres 가 지킨다

- 테이블 72개 모두 RLS 를 켰고, 빠진 테이블이 있으면 통합 테스트가 실패한다. 정지된 사용자는 쓰기가 막힌다. 권한이 엮인 작업은 `SECURITY DEFINER` RPC 로 한다.
- 마이그레이션 477개. prod 에 올라간 파일은 sha256 으로 잠가서, 고치거나 사이에 새 파일을 끼우면 테스트가 실패한다.
- 함수를 다시 정의하는 마이그레이션은 직전 정의의 본문 줄과 `SECURITY DEFINER` · `SET` 이 다 남았는지 테스트가 검사한다. 일부러 뺀 줄은 이유를 남겨야 통과한다.
- 기능을 뺄 때는 화면 · 테이블 · 크론까지 같이 걷는다. 10월 뒤로 화면 112 → 81개, 테이블 91 → 72개로 줄였다.

### 알림

- `notifications` INSERT → 트리거 → Edge Function `send-push` → Expo Push.
- 저장할 필요가 없는 알림은 DB 를 거치지 않고 `pg_net` 으로 바로 보낸다. 정기 작업은 `pg_cron`.

### 백엔드를 직접 운영

- 2026년 10월에 관리형 Supabase 에서 AWS 서울의 오픈소스 Supabase(EC2 한 대, Docker Compose)로 옮겼다.
- Postgres · S3 API · Docker 같은 표준만 쓴다. API 주소를 내 도메인으로 바꿔 두어, 다음에 옮길 때는 앱 업데이트 없이 DNS 만 바꾸면 된다.
- 서버가 매일 DB 를 덤프해 S3 에 올리고, GitHub Actions 가 그 사본을 암호화해 AWS 밖에 한 벌 더 둔다. 백업이 26시간 넘게 없으면 작업이 실패해 알린다.
- 영상은 S3 에 올리고 CloudFront 서명 URL 로 본다.

### 릴리스

- 네이티브는 EAS 3채널(development · preview · production).
- JS 만 바뀐 배포는 OTA 스크립트 하나로 한다. lint · 타입 · 테스트가 빨갛거나, 네이티브 변경, prod 에 아직 안 올라간 마이그레이션, 로컬 URL 이 번들에 섞이는 경우를 감지하면 멈춘다.
- 웹은 main 에 푸시하면 GitHub Actions 가 S3 + CloudFront 에 올린다. AWS 에는 저장된 키 없이 OIDC 역할로 들어간다.

### 품질 게이트

- 커밋 전: 바뀐 파일 ESLint + 전체 타입 검사. 타입 에러가 있으면 커밋이 안 된다.
- CI: lint → typecheck → Jest(테스트 파일 278개). PR 에는 Playwright 웹 E2E 와 DB 통합 테스트가 더 돈다.
- lint 경고 총량을 19로 동결했다. 새 경고를 들이려면 기존 경고를 먼저 갚고 한도를 내린다(되돌아가지 않는 래칫).

## 기술 스택

- **앱**: Expo SDK 55 · Expo Router(typed routes) · React Native 0.83 · React 19 · TypeScript 5.9 · NativeWind 4 · Reanimated 4 · FlashList 2 · Lingui 5
- **데이터**: TanStack Query 5(AsyncStorage 캐시 영속화) · supabase-js
- **백엔드**: 오픈소스 Supabase 직접 운영: Postgres · RLS · RPC · Realtime · Storage(S3) · Edge Functions(Deno) · pg_cron · pg_net
- **인프라**: AWS 서울(EC2 · S3 · CloudFront) · Docker Compose · EAS Build · EAS Update(OTA)
- **품질**: ESLint · Prettier · Jest · Playwright · Husky + lint-staged · GitHub Actions · Sentry

## 관련

- [Volleyball Vision](https://github.com/hadan-HwH/volleyball-vision): 배구 경기 영상에서 랠리와 터치를 찾는 비전 사이드 프로젝트

<sub>숫자는 2026년 11월 기준(가입자 · 클럽 정보는 11-03 운영 DB, 나머지는 11-10 코드). 숫자 카드와 아키텍처 그림은 `tools/` 의 스크립트로 다시 그린다.</sub>
