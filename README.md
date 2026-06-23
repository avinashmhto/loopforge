<p align="center">
  <img src="assets/banner.png" alt="LoopForge Banner" width="100%">
</p>

# 🚀 LoopForge

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> **A true autonomous multi-agent AI framework where specialized agents collaborate to plan, architect, build, test, debug, review, and continuously improve software until the objective is achieved.**

LoopForge demonstrates how multiple AI-driven workflows can collaborate to solve complex engineering tasks with minimal human intervention. Instead of stopping after generating code, it verifies its own work, detects failures, applies fixes, and retries until the project succeeds.

---

## ✨ Features

* 🤖 True multi-agent architecture with specialized AI agents
* 🧠 Planner Agent for execution planning
* 🏗️ Architect Agent for project structure design
* 💻 Code Agent for implementation generation
* 🧪 Test Agent for automatic pytest creation
* ⚙️ Executor Agent for automated validation
* 🔧 Debugger Agent for autonomous issue resolution
* 🔍 Reviewer Agent for quality verification
* 📝 Reporter Agent for execution summaries
* 🔄 Iterative self-healing loop until success
* 📄 Automatic execution report generation
* 🚀 End-to-end software engineering from a single prompt
---

## 🔥 Multi-Agent Workflow

```text
                    ## 🏛️ Architecture

```text
                    User Goal
                         │
                         ▼
              Workflow Engine / Orchestrator
                         │
                         ▼
                  🧠 Planner Agent
                         ▼
                🏗️ Architect Agent
                         ▼
                   💻 Code Agent
                         ▼
                   🧪 Test Agent
                         ▼
                ⚙️ Executor Agent
                         │
                 ┌───────┴────────┐
                 │                │
                 ▼                ▼
          🔍 Reviewer Agent   🔧 Debugger Agent
                 │                │
                 └───────┬────────┘
                         ▼
                  📝 Reporter Agent
```

---

## 🏗️ Current Capabilities

LoopForge can currently:

* Coordinate multiple AI agents to solve engineering tasks
* Plan software development before implementation
* Design application architecture automatically
* Generate production-ready FastAPI applications
* Generate comprehensive pytest test suites
* Execute tests automatically
* Detect runtime and syntax failures
* Autonomously debug and repair generated code
* Re-run validation until successful
* Produce execution reports summarizing the entire workflow

Example prompt:

> **Create a notes application with REST endpoints and comprehensive pytest coverage.**

---

## 📂 Project Structure

```text
LoopForge/
├── agents/
├── orchestrator/
├── core/
├── memory/
├── tools/
├── assets/
├── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/loopforge.git
cd loopforge
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure your API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5.5
```

---

## ▶️ Run LoopForge

```bash
python main.py
```

You can choose between:

```
1. True Multi-Agent Engineer

```

---

## 🧪 Sample Multi-Agent Execution

Input:

```text
Create a notes application with REST endpoints and comprehensive pytest coverage.
```

Execution:

```
🧠 Planner Agent → Creates execution plan
🏗️ Architect Agent → Designs project structure
💻 Code Agent → Generates implementation
🧪 Test Agent → Produces pytest suite
⚙️ Executor Agent → Runs automated tests
🔧 Debugger Agent → Fixes detected issues
🔍 Reviewer Agent → Verifies final output
📝 Reporter Agent → Generates execution report
```

Example outcome:

```
Attempt 1:
❌ SyntaxError detected during test execution

Debugger Agent repaired the project.

Attempt 2:
✅ 28/28 tests passed

Execution report generated successfully.
```

---

## 📄 Generated Report

Each execution creates a report similar to:

```
generated_apps/multi_agent_app/loopforge_report.md
```

The report includes:

* User objective
* Execution status
* Number of attempts
* AI-generated summary
* Test results

---

## 🛣️ Roadmap

* [x] True multi-agent workflow engine
* [x] Planner Agent
* [x] Architect Agent
* [x] Code Agent
* [x] Test Agent
* [x] Executor Agent
* [x] Debugger Agent
* [x] Reviewer Agent
* [x] Reporter Agent
* [x] Autonomous self-healing execution loop
* [x] Automatic execution report generation
* [x] End-to-end software generation from natural language
* [ ] Shared agent context and memory
* [ ] Persistent execution history
* [ ] Workflow router for multiple engineering domains
* [ ] Docker sandbox for secure code execution
* [ ] Git and GitHub integration
* [ ] CI/CD pipeline generation
* [ ] Terraform and infrastructure automation
* [ ] Kubernetes deployment workflows
* [ ] Multi-language code generation
* [ ] Autonomous pull request creation and code review


---

## ⭐ Vision

LoopForge is being built as an open framework for autonomous software engineering and agentic workflows. The long-term goal is to enable AI systems that don't just generate code they plan, verify, debug, iterate, and continuously improve until the task is complete.

---

## ⚠️ Project Status

LoopForge is an actively evolving open-source project and a research prototype for autonomous software engineering. Features and workflows are continuously being improved as the framework evolves.

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome. Feel free to open an issue or submit a pull request.

## 📜 License

This project is released under the MIT License.
