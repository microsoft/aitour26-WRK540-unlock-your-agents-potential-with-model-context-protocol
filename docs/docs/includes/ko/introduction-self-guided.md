## 자율 학습자

이 지침은 사전 구성된 랩 환경에 액세스할 수 없는 자율 학습자를 위한 것입니다. 다음 단계에 따라 환경을 설정하고 워크샵을 시작하세요.

## 소개

이 워크샵은 Azure AI 에이전트 서비스와 관련 SDK에 대해 가르치도록 설계되었습니다. Azure AI 에이전트 서비스의 특정 기능을 강조하는 여러 랩으로 구성되어 있습니다. 각 랩은 이전 랩의 지식과 작업을 기반으로 하므로 순서대로 완료해야 합니다.

## 전제 조건

1. Azure 구독에 대한 액세스. Azure 구독이 없는 경우 시작하기 전에 [무료 계정](https://azure.microsoft.com/free/){:target="_blank"}을 만드세요.
1. GitHub 계정이 필요합니다. 없는 경우 [GitHub](https://github.com/join){:target="_blank"}에서 만드세요.

## 워크샵 프로그래밍 언어 선택

워크샵은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 선호하는 언어를 선택하세요. 워크샵 중간에 언어를 바꾸지 마세요.

**선호하는 언어 탭을 선택하세요:**

=== "Python"
    워크샵의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크샵의 기본 언어는 **C#**로 설정되어 있습니다.

## 워크샵 열기

이 워크샵을 실행하는 **권장** 방법은 **GitHub Codespaces**를 사용하는 것입니다. 이 옵션은 워크샵을 완료하는 데 필요한 모든 도구와 리소스가 사전 구성된 환경을 제공합니다. 또는 Visual Studio Code Dev Container와 Docker를 사용하여 로컬로 워크샵을 열 수 있습니다. 두 옵션 모두 아래에 설명되어 있습니다.

!!! Note
    **Codespace 또는 Dev Container 빌드에는 약 5분이 걸립니다. 프로세스를 시작한 다음 빌드되는 동안 지침을 계속 읽을 수 있습니다.**

=== "GitHub Codespaces"

    **Open in GitHub Codespaces**를 선택하여 GitHub Codespaces에서 프로젝트를 엽니다.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}



=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon 사용자"
        곧 실행할 자동화된 배포 스크립트는 Apple Silicon에서 지원되지 않습니다. Dev Container 대신 Codespaces나 macOS에서 배포 스크립트를 실행하세요. -->

    또는 [Dev Containers 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}을 사용하여 로컬 VS Code 개발 환경에서 프로젝트를 열 수 있는 Visual Studio Code Dev Container를 사용하여 로컬로 프로젝트를 열 수 있습니다.

    1. Docker Desktop을 시작합니다 (아직 설치되지 않은 경우 설치)
    2. **Dev Containers Open**을 선택하여 VS Code Dev Container에서 프로젝트를 엽니다.

        [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*Translated using GitHub Copilot.*
