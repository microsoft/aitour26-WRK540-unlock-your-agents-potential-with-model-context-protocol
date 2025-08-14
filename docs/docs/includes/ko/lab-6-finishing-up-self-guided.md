이 워크샵의 랩 부분은 여기까지입니다. 주요 학습 내용과 추가 리소스를 읽어보세요. 하지만 먼저 정리를 해보겠습니다.

## GitHub CodeSpaces 정리

### GitHub에 변경 사항 저장

워크샵 중에 파일에 만든 변경 사항을 포크로 개인 GitHub 저장소에 저장할 수 있습니다. 이렇게 하면 사용자 정의로 워크샵을 쉽게 다시 실행할 수 있고, 워크샵 내용이 항상 GitHub 계정에 남아있게 됩니다.

* VS Code에서 왼쪽 창의 "Source Control" 도구를 클릭합니다. 세 번째 도구이거나 키보드 단축키 <kbd>Control-Shift-G</kbd>를 사용할 수 있습니다.
* "Source Control" 아래 필드에 `Agents Lab`을 입력하고 **✔️Commit**을 클릭합니다.
  * "커밋할 스테이징된 변경 사항이 없습니다." 프롬프트에 **예**를 클릭합니다.
* **Sync Changes**를 클릭합니다.
  * "이 작업은 origin/main에서 커밋을 가져오고 푸시합니다" 프롬프트에 **확인**을 클릭합니다.

이제 GitHub 계정에 사용자 정의가 포함된 워크샵의 자체 사본이 있습니다.

### GitHub codespace 삭제

GitHub CodeSpace는 자동으로 종료되지만 삭제될 때까지 컴퓨팅 및 스토리지 할당량을 소량 소비합니다. ([GitHub 청구 요약](https://github.com/settings/billing/summary)에서 사용량을 확인할 수 있습니다.) 이제 다음과 같이 codespace를 안전하게 삭제할 수 있습니다:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} 방문
* 페이지 하단에서 활성 codespace 오른쪽의 "..." 메뉴를 클릭합니다
* **Delete** 클릭
  * "정말로 삭제하시겠습니까?" 프롬프트에서 **Delete**를 클릭합니다.

## Azure 리소스 삭제

이 랩에서 생성한 대부분의 리소스는 사용한 만큼 지불하는 리소스이므로 더 이상 사용 요금이 청구되지 않습니다. 그러나 AI Foundry에서 사용하는 일부 스토리지 서비스는 지속적인 소액 요금이 발생할 수 있습니다. 모든 리소스를 삭제하려면 다음 단계를 따르세요:

* [Azure Portal](https://portal.azure.com){:target="_blank"} 방문
* **Resource groups** 클릭
* 리소스 그룹 `rg-agent-workshop-****` 클릭
* **Delete Resource group** 클릭
* 하단의 "삭제 확인을 위해 리소스 그룹 이름 입력" 필드에 `rg-agent-workshop-****` 입력
* **Delete** 클릭
  * 삭제 확인 프롬프트에서 "Delete" 클릭

*GitHub Copilot을 사용하여 번역되었습니다.*
