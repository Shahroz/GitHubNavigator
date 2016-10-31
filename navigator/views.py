from django.shortcuts import render
from urlparse import urlparse, parse_qs
from GitHubNavigator import settings
import urllib2
import json


def index(request):
    error_dict = {}
    if request.method == "GET":
        try:
            params = parse_qs(urlparse(request.get_full_path()).query)
            if not params:
                error_dict["error"] = "Please input any repository in search_term query string"
                return render(request, 'index.html', context=error_dict)

            search_term = params.get("search_term")[0]
            list_repo = get_repositories(search_terms=search_term)
            if not list_repo:
                context = {"search_term": search_term, "error": "No repository found for search term '{0}'".
                    format(search_term)}
                return render(request, 'index.html', context=context)
            else:
                context = {"search_term": search_term, "repositories": list_repo, "error": None}
                return render(request, 'index.html', context=context)
        except ValueError:
            error_dict["error"] = ValueError.message
            return render(request, 'index.html', context=error_dict)


def get_repositories(search_terms, sort="created", order="desc", page=1, per_page=5):
    result = []
    str_url = """{0}/search/repositories?q={1}&sort={2}&order={3}&page={4}&per_page={5}"""
    repo_url = str_url.format(settings.GIT_URL, search_terms, sort, order, page, per_page)
    serialized_data = urllib2.urlopen(repo_url).read()
    list_repo = json.loads(serialized_data)

    if list_repo.get("total_count") > 0 and len(list_repo.get("items")) > 0:
        for repo in list_repo.get("items"):
            dict = {}
            dict["respository_name"] = repo.get("name")
            dict["created_at"] = repo.get("created_at")
            dict["owner_login"] = repo.get("owner").get("login")
            dict["owner_url"] = repo.get("owner").get("url")
            dict["avatar_url"] = repo.get("owner").get("avatar_url")

            commits = get_commits(user_name=dict.get("owner_login"), repo=dict.get("respository_name"))
            if commits:
                commit = commits.get("commit")
                dict["commit_author_name"] = commit.get("author").get("name")
                dict["sha"] = commits.get("sha")
                dict["commit_message"] = commits.get("commit").get("message")
                result.append(dict)
    return result


def get_commits(user_name, repo):
    result = {}
    repo_url = """{0}/repos/{1}/{2}/commits?sort=created&order=desc&page=1&per_page=1""".format(settings.GIT_URL, user_name, repo)

    serialized_data = urllib2.urlopen(repo_url).read()
    data = json.loads(serialized_data)
    if len(data) > 0:
        result = data[0]
    return result
