<h1>Hidden-Channel-Monitoring</h1>
javascript와 django를 이용한 딥러닝 기반 히든채널 사이버 범죄 모니터링 시스템입니다.<hr/>

<h2>초기화면</h2>
접속시 초기화면입니다.
<img width="782" alt="1" src="https://user-images.githubusercontent.com/62545246/149612053-1a7f8725-f669-43bd-9578-3ddd4482c55d.PNG">
<h2>플랫폼 및 범죄유형 선택</h2>
밑으로 내리면 플랫폼과 범죄유형을 선택해 검색할 수 있습니다.
<img width="782" alt="2" src="https://user-images.githubusercontent.com/62545246/149612056-2d529f3c-0a83-45c2-be80-5e93195d640a.PNG">
<h2>검색결과화면</h2>
예시로 텔레그램과 마약을 선택했을 때 총 채널의 수, 총 메시지 수, 총 유저 수가 출력되고 채널당 ID, 유저 수, 고위험 유저 수가 출력됩니다.
<img width="774" alt="5" src="https://user-images.githubusercontent.com/62545246/149612061-c41e2c07-0e73-4f6f-9a28-101938d0aeb9.PNG">
채널 ID를 클릭하면 총 유저의 수, 고위험 유저 수, 총 메시지 수가 출력되고 유저당 ID, 메시지 수, 위험도가 출력됩니다.
<img width="771" alt="6" src="https://user-images.githubusercontent.com/62545246/149612063-f6ad8450-522e-4b1e-bd4c-c483ac5eba98.PNG">
이 때 고위험 유저만 볼 수 있게 필터를 걸 수 있습니다.
<img width="775" alt="7" src="https://user-images.githubusercontent.com/62545246/149612064-4d7b8ad2-8760-404b-9307-10a8b9e31791.PNG">
유저 ID를 클릭하면 유저가 쓴 모든 메시지의 워드클라우드와 메시지와 시간이 출력됩니다.
<img width="773" alt="8" src="https://user-images.githubusercontent.com/62545246/149612066-aa3ddaf5-f798-44a9-9fe8-180124444fb5.PNG"><hr/>
<h1>플랫폼 별 검색결과</h1>
트위터 : 유저ID->유저가 쓴 메시지<br>
텔레그램 : 채널ID->유저ID->유저가 쓴 메시지<br>
디스코드 : 채널ID->유저ID->유저가 쓴 메시지<br>
