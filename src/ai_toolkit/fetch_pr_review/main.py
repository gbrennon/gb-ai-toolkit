import sys

from ai_toolkit.forge.api import (
    fj_api_url,
    fj_get,
    gh_run,
    gh_run_single,
    is_github,
    parse_remote_ref,
)


def fj_fetch_pr(host: str, owner: str, repo: str, number: str) -> dict:
    url = fj_api_url(host, f"{owner}/{repo}/pulls/{number}")
    data = fj_get(url)
    if isinstance(data, list):
        print(f"Unexpected array from {url}", file=sys.stderr)
        sys.exit(1)
    return {
        "title": data.get("title", ""),
        "state": data.get("state", ""),
        "body": data.get("body", ""),
        "user": data.get("user", {}).get("login", ""),
    }


def fj_fetch_reviews(host: str, owner: str, repo: str, number: str) -> list[dict]:
    url = fj_api_url(host, f"{owner}/{repo}/pulls/{number}/reviews")
    data = fj_get(url)
    if not isinstance(data, list):
        return []
    return [
        {
            "id": r.get("id"),
            "user": r.get("user", {}).get("login", ""),
            "state": r.get("state", ""),
            "body": r.get("body", ""),
            "submitted_at": r.get("submitted_at", ""),
        }
        for r in data
    ]


def fj_fetch_comments(host: str, owner: str, repo: str, number: str) -> list[dict]:
    url = fj_api_url(host, f"{owner}/{repo}/pulls/{number}/comments")
    data = fj_get(url)
    if not isinstance(data, list):
        return []
    return [
        {
            "id": c.get("id"),
            "user": c.get("user", {}).get("login", ""),
            "path": c.get("path", ""),
            "line": c.get("line", ""),
            "body": c.get("body", ""),
            "commit_id": c.get("commit_id", ""),
        }
        for c in data
    ]


def gh_fetch_pr(owner: str, repo: str, number: str) -> dict:
    return gh_run_single(
        [
            "api",
            f"/repos/{owner}/{repo}/pulls/{number}",
            "--jq",
            "{title, state, body, user: .user.login}",
        ]
    )


def gh_fetch_reviews(owner: str, repo: str, number: str) -> list[dict]:
    return gh_run(
        [
            "api",
            f"/repos/{owner}/{repo}/pulls/{number}/reviews",
            "--jq",
            ".[] | {id, user: .user.login, state, body, submitted_at}",
            "--paginate",
        ]
    )


def gh_fetch_comments(owner: str, repo: str, number: str) -> list[dict]:
    return gh_run(
        [
            "api",
            f"/repos/{owner}/{repo}/pulls/{number}/comments",
            "--jq",
            ".[] | {id, user: .user.login, path, line, body, commit_id}",
            "--paginate",
        ]
    )


def render(pr: dict, reviews: list[dict], comments: list[dict]) -> None:
    print(f"# PR Review: {pr['title']}")
    print(f"**State:** {pr['state']}  ")
    print(f"**Author:** {pr['user']}  ")
    print()

    body = pr.get("body", "").strip()
    if body:
        print("## PR Description")
        print(body)
        print()

    print("## Review Summaries")
    found = False
    for r in reviews:
        body = r.get("body", "").strip()
        if body:
            print(f"### {r['user']} ({r['state']})")
            print(body)
            print()
            found = True
    if not found:
        print("_No review summaries found._")
        print()

    print("## Inline Comments")
    found = False
    for c in comments:
        body = c.get("body", "").strip()
        if not body:
            continue
        path = c.get("path", "")
        line = c.get("line", "")
        loc = f"{path}:{line}" if line else path
        print(f"### {c['user']} at `{loc}`")
        print(body)
        print()
        found = True
    if not found:
        print("_No inline comments found._")
        print()

    print("---")
    print(
        f"_Fetched {len(reviews)} review(s) and {len(comments)} inline comment(s)."
        f" Total findings: {len(reviews) + len(comments)}_"
    )


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: uv run fetch-pr-review <PR-URL | owner/repo/number>",
            file=sys.stderr,
        )
        sys.exit(1)

    host, owner, repo, number = parse_remote_ref(sys.argv[1], kinds=("pull", "pulls"))

    if is_github(host):
        pr = gh_fetch_pr(owner, repo, number)
        reviews = gh_fetch_reviews(owner, repo, number)
        comments = gh_fetch_comments(owner, repo, number)
    else:
        if not host:
            print(
                "Could not detect remote host. Use a full PR URL or run from a git repo.",
                file=sys.stderr,
            )
            sys.exit(1)
        pr = fj_fetch_pr(host, owner, repo, number)
        reviews = fj_fetch_reviews(host, owner, repo, number)
        comments = fj_fetch_comments(host, owner, repo, number)

    render(pr, reviews, comments)
