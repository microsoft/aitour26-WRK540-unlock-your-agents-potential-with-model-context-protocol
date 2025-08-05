이것으로 이 워크샵의 랩 부분이 모두 끝났습니다. 주요 내용과 추가 리소스를 계속 읽어보시되, 먼저 정리를 해보겠습니다.

## GitHub CodeSpaces 정리

### GitHub에 변경사항 저장

워크샵 중에 파일에 대한 모든 변경사항을 개인 GitHub 리포지토리에 포크로 저장할 수 있습니다. 이렇게 하면 사용자 정의와 함께 워크샵을 쉽게 다시 실행할 수 있고, 워크샵 콘텐츠가 항상 GitHub 계정에서 사용 가능한 상태로 유지됩니다.

* VS Code에서 왼쪽 창의 "Source Control" 도구를 클릭합니다. 세 번째 도구이거나 키보드 단축키 <kbd>Control-Shift-G</kbd>를 사용할 수 있습니다.
* "Source Control" 아래 필드에 `Agents Lab`을 입력하고 **✔️Commit**을 클릭합니다.
  * "There are no staged changes to commit." 프롬프트에 **Yes**를 클릭합니다.
* **Sync Changes**를 클릭합니다.  
  * "This action will pull and push commits from and to origin/main" 프롬프트에 **OK**를 클릭합니다.

이제 GitHub 계정에 사용자 정의가 포함된 워크샵의 고유한 사본이 있습니다.

### GitHub codespace 삭제

GitHub CodeSpace는 자동으로 종료되지만 삭제될 때까지 컴퓨팅 및 스토리지 할당량의 소량을 소비합니다. ([GitHub 결제 요약](https://github.com/settings/billing/summary)에서 사용량을 확인할 수 있습니다.) 다음과 같이 codespace를 안전하게 삭제할 수 있습니다:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} 방문
* 페이지 하단에서 활성 codespace 오른쪽의 "..." 메뉴를 클릭합니다
* **Delete**를 클릭합니다
  * "Are you sure?" 프롬프트에서 **Delete**를 클릭합니다.

## Azure 리소스 삭제

이 랩에서 생성한 대부분의 리소스는 종량제 리소스로, 사용한 만큼만 요금이 부과됩니다. 그러나 AI Foundry에서 사용하는 일부 스토리지 서비스는 소액의 지속적인 요금이 발생할 수 있습니다. 모든 리소스를 삭제하려면 다음 단계를 따르세요:

* [Azure Portal](https://portal.azure.com){:target="_blank"} 방문
* **Resource groups** 클릭
* 리소스 그룹 `rg-agent-workshop-****` 클릭
* **Delete Resource group** 클릭
* 하단의 "Enter resource group name to confirm deletion" 필드에 `rg-agent-workshop-****` 입력
* **Delete** 클릭
  * Delete Confirmation 프롬프트에서 "Delete" 클릭

*Translated using GitHub Copilot.*
