# Installing LLM Guard

## Prerequisites

Supported Python versions:

- 3.10
- 3.11
- 3.12
- 3.13
- 3.14

## Using `pip`

!!! note

    Consider installing the LLM Guard python packages on a virtual environment like `venv` or `conda`.

### Base installation (security scanners)

The base installation includes all scanners that do **not** require Presidio,
such as prompt injection detection, toxicity detection, token limits, regex
matching, ban topics / code / substrings, secrets detection, and more.

```bash
pip install llm-guard
```

### PII / Anonymization support (optional)

If you need the **Anonymize** (input) or **Sensitive** (output) scanners that
rely on Presidio for PII detection and anonymization, install the `pii` extra:

```bash
pip install "llm-guard[pii]"
```

!!! info "Scanner dependency groups"

    | Dependency group | Scanners | Extra |
    |---|---|---|
    | **Base** | BanCode, BanCompetitors, BanSubstrings, BanTopics, Bias, Code, Deanonymize, EmotionDetection, FactualConsistency, Gibberish, InvisibleText, JSON, Language, LanguageSame, MaliciousURLs, NoRefusal, PromptInjection, ReadingTime, Regex, Relevance, Secrets, Sentiment, TokenLimit, Toxicity, URLReachability | *(none)* |
    | **PII / Presidio** | Anonymize, Sensitive | `pii` |
    | **ONNX Runtime** | Any scanner with `use_onnx=True` | `onnxruntime` |

If you have issue installing the package due to missing `torch`, you can try the following commands:

```bash
pip install wheel
pip install torch==2.0.1
pip install llm-guard --no-build-isolation
```

## Install from source

To install LLM Guard from source, first clone the repo:

- Using HTTPS
```bash
git clone https://github.com/protectai/llm-guard.git
```
- Using SSH
```bash
git clone git@github.com:protectai/llm-guard.git
```

We recommend to use a virtual environment like `venv` or `conda` to install the package.

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the package using `pip`:

```bash
python -m pip install ".[dev]"
```
