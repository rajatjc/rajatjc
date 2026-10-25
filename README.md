<!-- Animated header: edit scripts/make_terminal.py, then run it to regenerate both themes. -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/terminal-dark.svg">
  <img alt="Terminal: Rajat Sharma, software developer at IBM in Toronto. Projects: loonie-ledger and lsm-kv." src="assets/terminal-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://rajatjc.github.io"><img src="https://img.shields.io/badge/Portfolio-rajatjc.github.io-FF5722?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio"></a>
  <a href="https://linkedin.com/in/rajatjc"><img src="https://img.shields.io/badge/LinkedIn-rajatjc-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:rajat.jc@gmail.com"><img src="https://img.shields.io/badge/Email-rajat.jc@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <img src="https://komarev.com/ghpvc/?username=rajatjc&label=profile%20views&color=0e75b6&style=for-the-badge" alt="Profile views">
</p>

<p align="center">
  <a href="#projects"><b>Projects</b></a> ·
  <a href="#about"><b>About</b></a> ·
  <a href="#experience"><b>Experience</b></a> ·
  <a href="#skills"><b>Skills</b></a> ·
  <a href="#stats"><b>Stats</b></a>
</p>

<a id="projects"></a>

## 🔭 Featured projects

<table>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/rajatjc/loonie-ledger">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/pin/?username=rajatjc&repo=loonie-ledger&theme=github_dark&hide_border=true">
  <img alt="loonie-ledger" src="https://github-readme-stats.vercel.app/api/pin/?username=rajatjc&repo=loonie-ledger&hide_border=true">
</picture>
</a>

A demo Canadian neobank: Java payments, Python fraud scoring and Node.js compliance, talking only through
**Redis Streams**. Money moves only when both checks pass, and an ops console gives you a real `kubectl`
shell on Kubernetes.

</td>
<td width="50%" valign="top">

<a href="https://github.com/rajatjc/lsm-kv">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/pin/?username=rajatjc&repo=lsm-kv&theme=github_dark&hide_border=true">
  <img alt="lsm-kv" src="https://github-readme-stats.vercel.app/api/pin/?username=rajatjc&repo=lsm-kv&hide_border=true">
</picture>
</a>

A storage engine from scratch in Java 21, the design behind Cassandra and RocksDB: write-ahead log,
SSTables, Bloom filters and compaction. **[Try the live demo](https://lsm-kv.onrender.com)** and
watch it flush and compact.

</td>
</tr>
</table>

<details>
<summary><b>🍁 How Loonie Ledger works</b> (click to expand)</summary>
<br>

```mermaid
flowchart TB
  U([Customer]) --> G["Gateway · Node.js + React"]
  G --> P["Payments · Java + Spring Boot<br/>holds the funds"]
  P --> DB[("Postgres<br/>double-entry ledger")]
  P -- "TransferRequested (via outbox)" --> T[("Redis stream: transfers")]
  T --> F["Fraud · Python<br/>risk score + reasons"]
  T --> C["Compliance · Node.js<br/>$10K + 24h checks, audit log"]
  F -- "PASS / HOLD" --> D[("Redis streams: decisions")]
  C -- "CLEAR / REVIEW" --> D
  D -- "settles only if both pass" --> P
```

- **No money moves unchecked.** Payments settles a transfer only after both the fraud and the compliance verdicts arrive. If either service is down, the transfer waits with the funds held.
- **No lost or doubled events.** A transactional outbox, consumer groups that acknowledge only after the work is done, and handlers that ignore repeats.
- **Tamper-evident audit log.** Each entry stores the hash of the one before it, so editing history is detectable.
- **Ops console.** On Kubernetes, the website includes a real terminal (`kubectl`, `redis-cli`, `psql`) limited by RBAC to its own namespace.

</details>

<details>
<summary><b>🗄️ How lsm-kv works</b> (click to expand)</summary>
<br>

```mermaid
flowchart LR
  W([PUT / DELETE]) --> WAL["Write-ahead log<br/>CRC-checked"] --> M["Memtable<br/>sorted, in memory"]
  M -- "full: flush" --> S["SSTables<br/>sparse index + Bloom filter"]
  S -- "4 tables: compact" --> K["K-way merge<br/>drops tombstones"] --> S
  R([GET]) --> M
  M -. "not found" .-> S
```

- **Crash-safe writes.** Every write hits a CRC-checked write-ahead log first, and replay stops cleanly at a half-written record.
- **Fast misses.** Each SSTable has a sparse index and a Bloom filter, so looking up a missing key is about **17x** cheaper than a hit.
- **One merge for everything.** Range scans and compaction share a heap-based k-way merge where the newest version of each key wins.
- **Measured with JMH.** About **3 µs** per write and **2.4 µs** per read.

</details>

Both have interactive playgrounds on my portfolio, **[rajatjc.github.io](https://rajatjc.github.io)**.

<a id="about"></a>

## 👋 About me

<details open>
<summary><b>What I'm doing now</b></summary>
<br>

- At **IBM**, building Maximo Manage as a multi-tenant SaaS: tenant provisioning and migration, an SRE dashboard, and GitOps deployments across AWS and IBM Cloud.

</details>

<details>
<summary><b>Ask me about</b></summary>
<br>

Event-driven systems with Kafka and Redis Streams · Cassandra data modeling · Kubernetes, OpenShift and GitOps with Argo CD ·
Spring Boot microservices · how storage engines work under the hood

</details>

<a id="experience"></a>

## 💼 Experience

<details>
<summary><b>IBM</b> · Software Developer, Maximo SaaS · <i>2026 – present</i></summary>
<br>

Building a multi-tenant Maximo Manage-as-a-Service platform on Kubernetes and OpenShift.

- Re-keyed tenant identifiers so tenants can migrate between tenant groups, and automated Db2 setup on Amazon RDS.
- Built the SRE dashboard (Next.js, TypeScript) and a Go API that shows every tenant's lifecycle state.
- Wrote Terraform for AWS accounts with Atlantis plan and apply on pull requests, and run GitOps deploys with Argo CD.
- Hardened services by removing SQL injection vectors, adding secret scanning, and patching Go CVEs.

</details>

<details>
<summary><b>IBM</b> · Software Developer, Envizi · <i>2024 – 2026</i></summary>
<br>

Java and Spring Boot microservices for ESG reporting, on Kafka, Cassandra and Kubernetes.

- Designed a denormalized Cassandra schema that cut lookup latency by **65%** across 4 production clusters.
- Built a Kafka monitoring service for **30+ topics** and **500K+ events a day**, cutting alert fatigue by **90%**.
- Cut XBRL taxonomy load time from **5 s to 1 s**, and ranked 10,000+ ESRS concepts by relevance.
- Deployed services across **10+ Kubernetes clusters** in three regions with Argo CD GitOps.

</details>

<details>
<summary><b>Earlier</b> · Konnect, Concordia University, Tejas Networks, Verbose Techlabs</summary>
<br>

- **Konnect:** Spring microservices on Kubernetes; deployments **40%** faster with multi-stage Docker builds.
- **Concordia University:** deployment tooling that cut developer effort by **44%**, and a Golden Key Scholarship for automation that saved 100+ hours a week.
- **Tejas Networks:** led a team of 3 migrating from ActiveMQ to Kafka, with **20%** faster processing.
- **Verbose Techlabs:** cut product search API latency from **550 ms to 200 ms**.

</details>

<details>
<summary><b>Education and achievements</b></summary>
<br>

- Master of Applied Computer Science, **Concordia University**, Montréal
- B.Tech in Information Technology, **Guru Gobind Singh Indraprastha University**, New Delhi
- **LeetCode** Knight (2018) · **CodeChef** 4★ (1848) · **HackerEarth** 1676
- Udacity Deep Learning Nanodegree

</details>

<a id="skills"></a>

## 🛠️ What I work with

**Languages**
<br>
<img src="https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white" alt="Java">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Go-00ADD8?style=flat&logo=go&logoColor=white" alt="Go">
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" alt="JavaScript">
<img src="https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white" alt="C++">

**Backend and data**
<br>
<img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat&logo=springboot&logoColor=white" alt="Spring Boot">
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Node.js-5FA04E?style=flat&logo=nodedotjs&logoColor=white" alt="Node.js">
<img src="https://img.shields.io/badge/Kafka-231F20?style=flat&logo=apachekafka&logoColor=white" alt="Kafka">
<img src="https://img.shields.io/badge/Redis-FF4438?style=flat&logo=redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Cassandra-1287B1?style=flat&logo=apachecassandra&logoColor=white" alt="Cassandra">
<img src="https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white" alt="MongoDB">

**Cloud and DevOps**
<br>
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white" alt="Kubernetes">
<img src="https://img.shields.io/badge/OpenShift-EE0000?style=flat&logo=redhatopenshift&logoColor=white" alt="OpenShift">
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Helm-0F1689?style=flat&logo=helm&logoColor=white" alt="Helm">
<img src="https://img.shields.io/badge/Argo_CD-EF7B4D?style=flat&logo=argo&logoColor=white" alt="Argo CD">
<img src="https://img.shields.io/badge/Tekton-FD495C?style=flat&logo=tekton&logoColor=white" alt="Tekton">
<img src="https://img.shields.io/badge/Terraform-844FBA?style=flat&logo=terraform&logoColor=white" alt="Terraform">
<img src="https://img.shields.io/badge/AWS-232F3E?style=flat" alt="AWS">
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white" alt="GitHub Actions">
<img src="https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white" alt="Grafana">

<a id="stats"></a>

## 📊 GitHub stats

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=rajatjc&show_icons=true&count_private=true&hide_border=true&theme=github_dark">
    <img alt="GitHub stats" height="165" src="https://github-readme-stats.vercel.app/api?username=rajatjc&show_icons=true&count_private=true&hide_border=true">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=rajatjc&layout=compact&langs_count=8&hide_border=true&theme=github_dark">
    <img alt="Top languages" height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=rajatjc&layout=compact&langs_count=8&hide_border=true">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=rajatjc&hide_border=true&theme=dark">
    <img alt="Contribution streak" src="https://streak-stats.demolab.com/?user=rajatjc&hide_border=true">
  </picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rajatjc/rajatjc/output/github-snake-dark.svg">
  <img alt="A snake eating my contribution graph" src="https://raw.githubusercontent.com/rajatjc/rajatjc/output/github-snake.svg">
</picture>

<details>
<summary>⚡ <b>Recent activity</b> (updated every 6 hours)</summary>

<!--START:recent-->
### 📁 Recent Repositories
- **[DreamShops](https://github.com/rajatjc/DreamShops)** — None
  - Last updated: 2026-10-24
- **[loonie-ledger](https://github.com/rajatjc/loonie-ledger)** — A demo Canadian neobank: Java, Python and Node.js services c...
  - Last updated: 2026-10-24
- **[rajatjc](https://github.com/rajatjc/rajatjc)** — None
  - Last updated: 2026-10-24

### 🔥 Recent Activity
- 🚀 **Pushed** to [rajatjc/CareerLinkup](https://github.com/rajatjc/CareerLinkup) — 2026-10-24
- 🚀 **Pushed** to [rajatjc/DreamShops](https://github.com/rajatjc/DreamShops) — 2026-10-24
- 🚀 **Pushed** to [rajatjc/GraphColoring](https://github.com/rajatjc/GraphColoring) — 2026-10-23

---
*Last updated: 2026-10-25 02:08 UTC*
<!--END:recent-->

</details>

## 🍁 Fun fact

> **Loonie Ledger** is named after the *loonie*, Canada's $1 coin, which got its nickname from the loon on one side.
> Try sending 10,000 of them in one go and my bank's compliance service puts the transfer on hold for review.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" alt="" width="100%">
