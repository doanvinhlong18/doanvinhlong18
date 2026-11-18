# Public-source research

Inspected on **2026-11-19**. The owner later clarified that no repository should dominate the profile; the final design gives the projects equal, compact treatment.

## Discovery

The [public account API](https://api.github.com/users/doanvinhlong18) returned 17 public repositories. The public profile had no name, biography, email, website, or LinkedIn to verify. The identity and experience in the README come from the owner's supplied brief. The [public repository list](https://api.github.com/users/doanvinhlong18/repos?per_page=100) did not include the special profile repository. This does not determine whether a private repository exists.

Seven repository trees were inspected: ShopCore, RAG-NEWS, RecommenderSystem, BigData, QuanLyNhaTroBE, BE-HQTCSDL, and BE-HQTCSDL-MYSQL. README files were read where present; manifests and selected implementation files were checked. No project was built or deployed as part of this profile task. Source inspection supports implementation descriptions, not operational guarantees.

## Evidence and boundaries

| Repository | Inspected revision | Evidence | Safe description |
| --- | --- | --- | --- |
| [ShopCore](https://github.com/doanvinhlong18/ShopCore) | `f2bc15bb656da6832dd1233add045ef023504beb` | README, parent/module POMs, Compose, `AuthService`, `RefreshTokenService`, `JwtTokenService`, and source tree | Learning microservices monorepo; implemented PostgreSQL-backed identity, RS256 JWTs, token rotation and reuse handling; several other services remain skeletons. |
| [RAG-NEWS](https://github.com/doanvinhlong18/RAG-NEWS) | `74c144da4cac521fd56b989c64bfb4ba7dd0c6d7` | README, requirements, `retrieval_pipeline.py`, `rag_inference.py`, `data_pipeline/sparse_bm25.py`, `data_pipeline/index_builder.py`, and cross-encoder model card | News retrieval research using BM25, FAISS, rank fusion, encoder reranking and LLM generation. No hallucination-free, latency, or production-readiness guarantee. |
| [RecommenderSystem](https://github.com/doanvinhlong18/RecommenderSystem) | `c70320a20a3ccb4fba08a3c9d44e519fb5076809` | README, requirements, `models/hybrid/hybrid_engine.py`, `models/hybrid/learned_hybrid.py`, `models/faiss_ann.py`, `api/routes.py`, evaluation code | Anime recommendation project with semantic/content and collaborative methods, ALS, cold-start handling, diversity logic, and a FastAPI interface. No production-scale or benchmark claims. |
| [BigData](https://github.com/doanvinhlong18/BigData) | `1917c578d648be8dcd87b5e727bf23c997262d29` | README, requirements, Compose topology, Spark Bronze/Silver/Gold code, feature builder, Prometheus configuration, feature and streaming-metric regression tests | NYC taxi streaming / MLOps project using Kafka, Spark, Delta Lake / MinIO, LightGBM, PostgreSQL, and operational telemetry. Replayed data is not described as a live commercial deployment. |

ShopCore's README has an older base-scaffold description alongside a newer authentication section. Actual authentication source confirms the identity implementation; it does not support describing the whole commerce flow as complete. Redis and RabbitMQ appear in infrastructure / dependencies, which does not prove application-level cache or consumer behavior.

RAG-NEWS and RecommenderSystem use the phrase “production-ready” in their own documentation. The profile intentionally avoids repeating that assertion. Training artifacts and source alone do not establish deployment quality, traffic, availability, or reproducible benchmark results.

The additional rental-management repositories contain Java / Spring Data JPA manifests, SQL Server drivers, entity and repository layers, and API/security source. They support the toolkit's SQL Server and relational backend entries, but were not selected for more project rows. Their academic or professional provenance is not established, so no employer or production claim is made.

## Stable source links

- [ShopCore README](https://github.com/doanvinhlong18/ShopCore/blob/f2bc15bb656da6832dd1233add045ef023504beb/README.md)
- [ShopCore refresh-token implementation](https://github.com/doanvinhlong18/ShopCore/blob/f2bc15bb656da6832dd1233add045ef023504beb/user-service/src/main/java/com/shopcore/user/service/RefreshTokenService.java)
- [RAG retrieval pipeline](https://github.com/doanvinhlong18/RAG-NEWS/blob/74c144da4cac521fd56b989c64bfb4ba7dd0c6d7/retrieval_pipeline.py)
- [Sparse BM25 implementation](https://github.com/doanvinhlong18/RAG-NEWS/blob/74c144da4cac521fd56b989c64bfb4ba7dd0c6d7/data_pipeline/sparse_bm25.py)
- [Hybrid recommendation engine](https://github.com/doanvinhlong18/RecommenderSystem/blob/c70320a20a3ccb4fba08a3c9d44e519fb5076809/models/hybrid/hybrid_engine.py)
- [BigData Gold aggregation](https://github.com/doanvinhlong18/BigData/blob/1917c578d648be8dcd87b5e727bf23c997262d29/spark/jobs/silver_to_gold.py)
- [BigData feature regression tests](https://github.com/doanvinhlong18/BigData/blob/1917c578d648be8dcd87b5e727bf23c997262d29/tests/test_feature_builder.py)

## Activity source

[GitHub's public contribution page](https://github.com/users/doanvinhlong18/contributions) was reachable with HTTP 200. The local activity assets use only the page's date and intensity attributes. They are a dated snapshot, not a fabricated calendar or a measurement of engineering ability. The initial snapshot is generated separately after the asset build.

## Missing information

Verified contact details, employer history, deployment evidence, and the precise division of professional technology experience were not available. The profile omits contacts and achievements it cannot support, and separates core background from project and research topics.
