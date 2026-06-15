from __future__ import annotations

SKILL_ALIASES: dict[str, str] = {
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "reactjs": "react",
    "react.js": "react",
    "react": "react",
    "nextjs": "next.js",
    "next.js": "next.js",
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",
    "express": "express",
    "expressjs": "express",
    "mongo": "mongodb",
    "mongodb": "mongodb",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "py": "python",
    "python": "python",
    "fastapi": "fastapi",
    "django": "django",
    "flask": "flask",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "langchain": "langchain",
    "llm": "llms",
    "llms": "llms",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "aws": "aws",
    "gcp": "gcp",
    "azure": "azure",
    "terraform": "terraform",
    "ci/cd": "ci/cd",
    "cicd": "ci/cd",
    "java": "java",
    "spring": "spring boot",
    "spring boot": "spring boot",
    "sql": "sql",
    "graphql": "graphql",
    "redis": "redis",
    "tailwind": "tailwind css",
    "tailwindcss": "tailwind css",
}

CAREER_PATHS: dict[str, list[str]] = {
    "MERN Developer": [
        "mongodb", "express", "react", "node.js", "javascript",
        "typescript", "redux", "rest api", "git",
    ],
    "Full Stack Engineer": [
        "react", "node.js", "typescript", "postgresql", "rest api",
        "docker", "ci/cd", "system design", "git",
    ],
    "AI Engineer": [
        "python", "pytorch", "tensorflow", "scikit-learn", "llms",
        "langchain", "nlp", "vector databases", "fastapi",
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "aws", "terraform", "ci/cd",
        "linux", "monitoring", "bash", "python",
    ],
    "Python Developer": [
        "python", "django", "fastapi", "postgresql", "rest api",
        "celery", "redis", "pytest", "git",
    ],
    "Java Developer": [
        "java", "spring boot", "hibernate", "postgresql", "rest api",
        "maven", "microservices", "junit", "git",
    ],
}

LEARNING_RESOURCES: dict[str, list[str]] = {
    "react": ["React official docs", "Epic React by Kent C. Dodds"],
    "node.js": ["Node.js docs", "The Node.js Handbook"],
    "typescript": ["TypeScript Handbook", "Total TypeScript"],
    "docker": ["Docker Getting Started", "Docker Deep Dive (Nigel Poulton)"],
    "kubernetes": ["Kubernetes docs", "Certified Kubernetes Administrator (CKA)"],
    "aws": ["AWS Cloud Practitioner", "AWS Solutions Architect Associate"],
    "llms": ["DeepLearning.AI LLM courses", "LangChain documentation"],
    "langchain": ["LangChain docs", "LangGraph tutorials"],
    "system design": ["System Design Primer", "Designing Data-Intensive Applications"],
    "ci/cd": ["GitHub Actions docs", "GitLab CI/CD documentation"],
}

DEFAULT_RESOURCES = ["Official documentation", "Hands-on project practice"]

SALARY_BANDS: dict[str, dict[str, str]] = {
    "MERN Developer": {"junior": "$60k–$85k", "mid": "$85k–$120k", "senior": "$120k–$160k"},
    "Full Stack Engineer": {"junior": "$70k–$95k", "mid": "$95k–$135k", "senior": "$135k–$185k"},
    "AI Engineer": {"junior": "$90k–$120k", "mid": "$120k–$170k", "senior": "$170k–$230k"},
    "DevOps Engineer": {"junior": "$80k–$110k", "mid": "$110k–$150k", "senior": "$150k–$200k"},
    "Python Developer": {"junior": "$65k–$90k", "mid": "$90k–$125k", "senior": "$125k–$165k"},
    "Java Developer": {"junior": "$70k–$95k", "mid": "$95k–$130k", "senior": "$130k–$175k"},
}

ATS_KEYWORD_HINTS = [
    "achieved", "improved", "led", "built", "designed", "optimized",
    "reduced", "increased", "delivered", "scaled", "automated", "implemented",
]
