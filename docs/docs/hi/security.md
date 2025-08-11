यह workshop application education और adaptation के लिए डिज़ाइन किया गया है, और out-of-the-box production use के लिए intended नहीं है। फिर भी, यह security के लिए कुछ best practices का demonstration करता है।

## Malicious SQL Attacks

LLM-generated SQL के साथ injection या harmful queries का जोखिम एक common concern है। ये जोखिम database permissions को limit करके कम किए जाते हैं।

यह app PostgreSQL का उपयोग करता है जिसमें agent के लिए restricted privileges हैं और secure environment में चलता है। Row-Level Security (RLS) सुनिश्चित करती है कि agents केवल अपने assigned stores के लिए data तक पहुंच सकें।

Enterprise settings में, data को typically read-only database या warehouse में simplified schema के साथ extract किया जाता है। यह agent के लिए secure, performant, और read-only access सुनिश्चित करता है।

## Sandboxing

यह demand पर code create और run करने के लिए [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} का उपयोग करता है। Code sandboxed execution environment में run होता है ताकि code को agent के scope से beyond actions लेने से रोका जा सके।

*GitHub Copilot का उपयोग करके अनुवादित।*
