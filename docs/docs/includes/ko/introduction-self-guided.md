## 자율 학습자

이 지침은 사전 구성된 랩 환경에 액세스할 수 없는 자율 학습자를 위한 것입니다. 다음 단계를 따라 환경을 설정하고 워크샵을 시작하세요.

## 소개

이 워크샵은 Azure AI 에이전트 서비스와 관련 SDK에 대해 교육하도록 설계되었습니다. 여러 랩으로 구성되어 있으며, 각 랩은 Azure AI 에이전트 서비스의 특정 기능을 강조합니다. 각 랩이 이전 랩의 지식과 작업을 기반으로 하므로 순서대로 완료해야 합니다.

## 전제 조건

1. Azure 구독에 대한 액세스. Azure 구독이 없는 경우 시작하기 전에 [무료 계정](https://azure.microsoft.com/free/){:target="_blank"}을 만드세요.
1. GitHub 계정이 필요합니다. 없는 경우 [GitHub](https://github.com/join){:target="_blank"}에서 만드세요.

## 워크샵 프로그래밍 언어 선택

워크샵은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 선호하는 언어를 선택하세요. 참고로 워크샵 중간에 언어를 변경하지 마세요.

**선호하는 언어 탭을 선택하세요:**

=== "Python"
    워크샵의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크샵의 기본 언어는 **C#**으로 설정되어 있습니다.

## 워크샵 열기

권장: 모든 필요한 도구가 포함된 사전 구성된 환경을 제공하는 **GitHub Codespaces**. 또는 Visual Studio Code **Dev Container**와 **Docker**로 로컬에서 실행할 수 있습니다. 아래 탭을 사용하여 선택하세요.

!!! Tip
    Codespaces 또는 Dev Container 빌드는 약 5분이 걸립니다. 빌드를 시작한 다음 완료되는 동안 **계속 읽으세요**.

=== "GitHub Codespaces"

    **GitHub Codespaces에서 열기**를 선택하여 GitHub Codespaces에서 프로젝트를 엽니다.

    [![GitHub Codespaces에서 열기](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon 사용자"
        곧 실행할 자동 배포 스크립트는 Apple Silicon에서 지원되지 않습니다. Dev Container 대신 Codespaces 또는 macOS에서 배포 스크립트를 실행하세요. -->

    또는 Visual Studio Code Dev Container를 사용하여 프로젝트를 로컬에서 열 수 있습니다. 이렇게 하면 [Dev Containers 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}을 사용하여 로컬 VS Code 개발 환경에서 프로젝트가 열립니다.

    1. Docker Desktop을 시작합니다(아직 설치되지 않은 경우 설치)
    2. **Dev Containers 열기**를 선택하여 VS Code Dev Container에서 프로젝트를 엽니다.

        [![Dev Containers에서 열기](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*GitHub Copilot을 사용하여 번역되었습니다.*
