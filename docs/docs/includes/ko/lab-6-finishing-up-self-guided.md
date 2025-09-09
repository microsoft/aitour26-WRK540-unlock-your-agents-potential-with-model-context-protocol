이것으로 이 워크숍의 랩 부분은 모두 끝났습니다. 주요 핵심 사항과 추가 리소스를 읽어보세요. 하지만 먼저 정리를 해보겠습니다.

## GitHub CodeSpaces 정리

### GitHub에 변경 사항 저장

워크숍 중에 파일에 만든 변경 사항을 포크로 개인 GitHub 저장소에 저장할 수 있습니다. 이렇게 하면 커스터마이징된 워크숍을 쉽게 다시 실행할 수 있고, 워크숍 콘텐츠가 항상 GitHub 계정에서 사용 가능한 상태로 유지됩니다.

* VS Code에서 왼쪽 창의 "Source Control" 도구를 클릭합니다. 세 번째 도구이거나 키보드 단축키 <kbd>Control-Shift-G</kbd>를 사용할 수 있습니다.
* "Source Control" 아래 필드에 `Agents Lab`을 입력하고 **✔️Commit**을 클릭합니다.
  * "There are no staged changes to commit." 프롬프트에 **Yes**를 클릭합니다.
* **Sync Changes**를 클릭합니다.
  * "This action will pull and push commits from and to origin/main" 프롬프트에 **OK**를 클릭합니다.

이제 GitHub 계정에 커스터마이징된 워크숍의 자체 복사본이 있습니다.

### GitHub codespace 삭제

GitHub CodeSpace는 자동으로 종료되지만 삭제될 때까지 컴퓨팅 및 스토리지 할당량의 소량을 소비합니다. ([GitHub Billing 요약](https://github.com/settings/billing/summary)에서 사용량을 확인할 수 있습니다.) 이제 다음과 같이 codespace를 안전하게 삭제할 수 있습니다:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"}를 방문합니다
* 페이지 하단에서 활성 codespace 오른쪽의 "..." 메뉴를 클릭합니다
* **Delete**를 클릭합니다
  * "Are you sure?" 프롬프트에서 **Delete**를 클릭합니다.

## Azure 리소스 삭제

이 랩에서 생성한 대부분의 리소스는 사용한 만큼만 지불하는 리소스로, 더 이상 사용하지 않으면 추가 요금이 부과되지 않습니다. 하지만 AI Foundry에서 사용하는 일부 스토리지 서비스는 소량의 지속적인 요금이 발생할 수 있습니다. 모든 리소스를 삭제하려면 다음 단계를 따르세요:

* [Azure Portal](https://portal.azure.com){:target="_blank"}을 방문합니다
* **Resource groups**을 클릭합니다
* 리소스 그룹 `rg-agent-workshop-****`을 클릭합니다
* **Delete Resource group**을 클릭합니다
* 하단의 "Enter resource group name to confirm deletion" 필드에 `rg-agent-workshop-****`을 입력합니다
* **Delete**를 클릭합니다
  * Delete Confirmation 프롬프트에서 "Delete"를 클릭합니다

*GitHub Copilot을 사용하여 번역됨.*
