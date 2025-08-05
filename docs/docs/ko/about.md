## Azure AI Foundry 프로젝트

## Zava DIY에 필요한 모델

## Zava DIY를 위한 합성 데이터 생성

Zava DIY는 개발자가 테스트 및 개발 목적으로 합성 데이터를 생성할 수 있도록 도와주는 도구입니다. 사용자가 다양한 애플리케이션에서 사용할 수 있는 현실적인 데이터셋을 생성할 수 있게 하여, 개인정보나 보안을 손상시키지 않으면서도 특정 요구사항을 충족하는 데이터를 확보할 수 있습니다.

데이터베이스에는 다음이 포함되어 있습니다:

- **워싱턴 주 전역에 걸친 8개 매장**, 각각 고유한 재고 및 판매 데이터 보유
- **워싱턴 주 및 온라인 전역의 50,000개 이상의 고객 기록**
- **도구, 야외 장비, 주택 개선용품을 포함한 400개 이상의 DIY 제품**
- **이미지 기반 검색을 위해 데이터베이스에 연결된 400개 이상의 제품 이미지**
- **자세한 판매 내역이 포함된 200,000개 이상의 주문 거래**
- **여러 매장에 걸친 3,000개 이상의 재고 품목**
- **AI 기반 유사성 검색이 가능한 제품 이미지용 이미지 임베딩** ([openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"}를 사용하여 인코딩)
- **검색 및 추천 기능을 향상시키는 제품 설명용 텍스트 임베딩** [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

데이터베이스는 복잡한 쿼리와 분석을 지원하여 판매, 재고, 고객 데이터에 효율적으로 액세스할 수 있습니다. PostgreSQL Row Level Security (RLS)는 에이전트가 할당된 매장의 데이터에만 액세스하도록 제한하여 보안과 개인정보 보호를 보장합니다.

*Translated using GitHub Copilot.*
